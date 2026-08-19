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
            self.assertTrue(
                "delegat" in content.lower() or "rout" in content.lower(),
                folder.name,
            )

    def test_human_architecture_document_names_every_skill(self):
        document = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
        for folder in (ROOT / "skills").iterdir():
            if (folder / "SKILL.md").is_file():
                self.assertIn(f"`{folder.name}`", document, folder.name)

    def test_plugin_manifests_present_one_isv_oem_advisor_product(self):
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual("oem-isv-advisor", codex["name"])
        self.assertEqual("ISV/OEM Advisor", codex["interface"]["displayName"])
        self.assertEqual("ISV/OEM Advisor", claude["displayName"])
        self.assertEqual("oem-isv-advisor", marketplace["plugins"][0]["name"])
        self.assertEqual("./skills/", codex["skills"])
        self.assertEqual("./skills/", claude["skills"])
        self.assertNotIn("PEAK", (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8"))

    def test_agent_script_packaging_pattern_is_productized(self):
        skill = ROOT / "skills/agentforce-implementation-advisor"
        skill_text = (skill / "SKILL.md").read_text(encoding="utf-8")
        reference = skill / "references/agent-script-packaging-pattern.md"
        self.assertTrue(reference.is_file())
        self.assertIn("Read `references/agent-script-packaging-pattern.md`", skill_text)
        pattern = reference.read_text(encoding="utf-8")
        for phrase in (
            "two-layer pattern",
            "LWC data module",
            "Static resource",
            "Custom metadata",
            "customer-owned agent",
            "Do not stop at \"Agent Script is not packageable.\"",
        ):
            self.assertIn(phrase, pattern)

    def test_practitioner_knowledge_is_a_product_wide_versioned_policy(self):
        entry = (ROOT / "skills/oem-isv-advisor/SKILL.md").read_text(encoding="utf-8")
        policy_path = ROOT / "skills/oem-isv-advisor/references/practitioner-knowledge-policy.md"
        self.assertIn("Read `references/practitioner-knowledge-policy.md`", entry)
        self.assertTrue(policy_path.is_file())
        policy = policy_path.read_text(encoding="utf-8")
        for phrase in (
            "documentation silence",
            "special ordering constraints",
            "stable claim identity",
            "supersession lineage",
            "replacement skill snapshot",
        ):
            self.assertIn(phrase, policy)


if __name__ == "__main__":
    unittest.main()
