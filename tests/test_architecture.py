import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CATALOG = ROOT / "skills/oem-isv-advisor/references/capability-catalog.json"


class AdvisorArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_catalog_and_filesystem_contain_the_same_26_skills(self):
        expected = {item["id"] for item in self.catalog["foundation_skills"]}
        for capability in self.catalog["capabilities"]:
            expected.add(capability["id"])
            expected.update(item["id"] for item in capability.get("focused_skills", []))
        actual = {path.name for path in (ROOT / "skills").iterdir() if (path / "SKILL.md").is_file()}
        self.assertEqual(26, len(expected))
        self.assertEqual(expected, actual)
        self.assertEqual(7, len(self.catalog["capabilities"]))
        self.assertEqual(26, self.catalog["baseline"]["skill_count"])

    def test_every_skill_has_minimal_frontmatter_and_agent_metadata(self):
        for folder in sorted((ROOT / "skills").iterdir()):
            skill = folder / "SKILL.md"
            if not skill.is_file():
                continue
            lines = skill.read_text(encoding="utf-8").splitlines()
            self.assertEqual("---", lines[0], folder.name)
            closing = lines.index("---", 1)
            keys = {line.split(":", 1)[0] for line in lines[1:closing] if ":" in line}
            self.assertEqual({"name", "description"}, keys, folder.name)
            agent = folder / "agents/openai.yaml"
            self.assertTrue(agent.is_file(), folder.name)
            self.assertIn(f"${folder.name}", agent.read_text(encoding="utf-8"), folder.name)

    def test_domain_skills_define_authority_evidence_and_delegation(self):
        foundation = {"oem-isv-advisor", "advisor-capability-preflight"}
        for folder in sorted((ROOT / "skills").iterdir()):
            if folder.name in foundation or not (folder / "SKILL.md").is_file():
                continue
            content = (folder / "SKILL.md").read_text(encoding="utf-8")
            for required in ("**Ask:**", "**Assess:**", "**Act:**", "fact", "unknown"):
                self.assertIn(required, content, f"{folder.name}: {required}")
            self.assertIn("approv", content.lower(), folder.name)
            self.assertIn("delegat", content.lower(), folder.name)

    def test_human_architecture_document_names_every_skill(self):
        document = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        for folder in (ROOT / "skills").iterdir():
            if (folder / "SKILL.md").is_file():
                self.assertIn(f"`{folder.name}`", document, folder.name)


if __name__ == "__main__":
    unittest.main()
