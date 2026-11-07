"""Check SemVer tag/manifests without publishing or changing installed plugins."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/isv-partner-advisor/scripts"))
from check_skill_contracts import SEMVER


def validate(root: Path, tag: str | None = None) -> str:
    version = (root / "VERSION").read_text().strip()
    if not SEMVER.fullmatch(version):
        raise ValueError("VERSION must be SemVer without a leading v.")
    for name in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        manifest = json.loads((root / name).read_text())
        if manifest["name"] != "isv-partner-advisor" or manifest["version"] != version:
            raise ValueError(f"{name} must retain plugin identity and match VERSION.")
    market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    if market["name"] != "partner-ecosystem-agentic-kit" or market["plugins"][0]["name"] != "isv-partner-advisor" or market["plugins"][0]["version"] != version:
        raise ValueError("Marketplace identity/version must match the plugin release.")
    if tag is not None and tag != f"v{version}":
        raise ValueError("Release tag must be v followed by the exact VERSION.")
    return version


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag")
    args = parser.parse_args()
    print(validate(ROOT, args.tag))
