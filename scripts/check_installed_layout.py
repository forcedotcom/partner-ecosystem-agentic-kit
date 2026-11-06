"""Check extracted skill-local references without launching a model or touching an org."""
import json
from pathlib import Path
import re


def inspect(skills: Path) -> list[str]:
    folders = {p.name: p for p in skills.iterdir() if (p / "SKILL.md").is_file()}
    errors = []
    for name, folder in folders.items():
        for document in folder.rglob("*.md"):
            text = document.read_text()
            relative_paths = set(re.findall(r"(?:references|scripts)/[A-Za-z0-9_./-]+\.(?:md|json|py|yaml)", text))
            for relative in relative_paths:
                if not (folder / relative).is_file():
                    errors.append(f"{name}: missing skill-local {relative} from {document.name}")
        contract = json.loads((folder / "references/skill-contract.json").read_text())
        for key in ("practitioner_knowledge", "source_refresh"):
            value = contract["evidence"][key]
            if value and not (folder / value).is_file():
                errors.append(f"{name}: missing contract evidence {value}")
        for relation in contract["relationships"]:
            if relation["target"] not in folders:
                errors.append(f"{name}: unresolved catalog skill ID {relation['target']}")
    catalog = json.loads((skills / "isv-partner-advisor/references/capability-catalog.json").read_text())
    entries = list(catalog["foundation_skills"])
    for cap in catalog["capabilities"]:
        entries.append(cap)
        entries.extend(cap["focused_skills"])
    if {e["id"] for e in entries} != set(folders):
        errors.append("Catalog IDs differ from installed skills.")
    if any("contract" in entry for entry in entries):
        errors.append("Catalog must route by skill ID, not cross-skill contract paths.")
    return errors


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", type=Path)
    args = parser.parse_args()
    errors = inspect(args.skills)
    print(json.dumps({"status": "blocked" if errors else "ready", "findings": errors}, indent=2))
    raise SystemExit(bool(errors))
