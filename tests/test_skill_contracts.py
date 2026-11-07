import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("library_contracts", ROOT / "skills/isv-partner-advisor/scripts/check_skill_contracts.py")
CONTRACTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTRACTS)


class SkillContractTests(unittest.TestCase):
    def test_entire_library_declares_consistent_contracts(self):
        skills = sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file())
        report = CONTRACTS.inspect_contracts(skills)
        self.assertEqual(27, len(report["skills"]))
        self.assertTrue(all(r["status"] == "ready" for r in report["skills"]), report["findings"])

    def test_catalog_is_reproducible_from_contracts(self):
        actual = json.loads((ROOT / "skills/isv-partner-advisor/references/capability-catalog.json").read_text())
        self.assertEqual(actual, CONTRACTS.generate_catalog(ROOT))

    def test_every_skill_has_its_own_version_in_header_and_catalog(self):
        catalog = CONTRACTS.generate_catalog(ROOT)
        entries = list(catalog["foundation_skills"])
        for capability in catalog["capabilities"]:
            entries.append(capability)
            entries.extend(capability["focused_skills"])
        self.assertEqual(27, len(entries))
        for entry in entries:
            report = CONTRACTS.inspect_contract(ROOT / "skills" / entry["id"])
            updated = {"solution-discovery", "headless-mcp-advisor",
                       "package-version-validation", "environment-portfolio",
                       "scratch-org-shape"}
            expected = ("2.0.1" if entry["id"] == "isv-partner-advisor"
                        else "1.0.2" if entry["id"] in updated else "1.0.1")
            self.assertEqual(expected, report["skill_version"])
            self.assertEqual(report["skill_version"], entry["version"])

    def test_readonly_advisors_do_not_own_act(self):
        for name in ("packaging-strategy", "packageability-assessment", "package-ancestry-dependencies", "environment-portfolio", "implementation-pattern-router"):
            contract = CONTRACTS.inspect_contract(ROOT / "skills" / name)["contract"]
            self.assertEqual(["ask", "assess"], contract["authority"]["supported_modes"])
            self.assertEqual("delegate", contract["authority"]["act_behavior"])

    def test_preflight_act_is_configuration_only(self):
        contract = CONTRACTS.inspect_contract(ROOT / "skills/advisor-capability-preflight")["contract"]
        self.assertEqual("configuration-only", contract["authority"]["act_behavior"])
        act = [op for op in contract["authority"]["operations"] if op["mode"] == "act"]
        self.assertEqual(["session-configuration"], [op["target"] for op in act])

    def test_no_external_provider_is_a_blanket_ask_prerequisite(self):
        for folder in (ROOT / "skills").iterdir():
            for dep in CONTRACTS.inspect_contract(folder)["contract"]["dependencies"]:
                self.assertFalse("ask" in dep["modes"] and dep["requirement"] == "required")


if __name__ == "__main__":
    unittest.main()
