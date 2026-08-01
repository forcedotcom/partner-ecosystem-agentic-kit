import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "advisor-capability-preflight"
CHECK = SKILL / "scripts" / "check_preflight.py"
RECORD = SKILL / "scripts" / "record_preference.py"
POLICY = SKILL / "references" / "documentation-policy.json"
CATALOG = ROOT / "skills" / "oem-isv-advisor" / "references" / "capability-catalog.json"


def load_check_module():
    spec = importlib.util.spec_from_file_location("check_preflight", CHECK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.module = load_check_module()
        self.policy = json.loads(POLICY.read_text(encoding="utf-8"))

    def test_connected_mcp_is_detected_from_exposed_tools_only(self):
        result = self.module.evaluate(
            self.policy,
            "codex",
            ["mcp__salesforce_docs__search", "unrelated_tool"],
            {"approved_documentation_domains": "approved"},
        )
        self.assertEqual("connected", result["salesforce_docs_mcp"]["status"])
        self.assertEqual("salesforce_docs_mcp", result["fallback"])
        self.assertTrue(result["ready"])

    def test_missing_mcp_offers_verified_salesforce_install(self):
        result = self.module.evaluate(self.policy, "claude-code", [], {})
        self.assertEqual("unavailable", result["salesforce_docs_mcp"]["status"])
        candidates = result["salesforce_docs_mcp"]["verified_install_candidates"]
        self.assertEqual("salesforce-docs", candidates[0]["id"])
        self.assertEqual(
            "https://salesforce-docs-76258744c9d7.herokuapp.com/api/mcp",
            candidates[0]["url"],
        )
        self.assertEqual(
            ["salesforce_docs_search", "salesforce_docs_fetch"],
            candidates[0]["expected_tools"],
        )
        self.assertEqual("2025-06-18", candidates[0]["protocol_version"])
        self.assertEqual("mcp-semantic-search", candidates[0]["server_info"]["name"])
        self.assertNotIn("mcp_install_consent", result["consent_required"])
        self.assertIn("offer_salesforce_docs_mcp", result["recommended_actions"])
        self.assertEqual("optional-highly-recommended", result["salesforce_docs_mcp"]["requirement"])
        self.assertFalse(result["host_security_override"])

    def test_runtime_catalog_candidate_must_be_verified_and_identified(self):
        candidate = {
            "verified": True,
            "harnesses": ["test-harness"],
            "publisher": "Salesforce",
            "source": "Salesforce-managed catalog",
            "marketplace_identity": "salesforce-docs",
            "authentication": "declared by catalog",
        }
        result = self.module.evaluate(self.policy, "test-harness", [], {}, [candidate])
        self.assertEqual([candidate], result["salesforce_docs_mcp"]["verified_install_candidates"])
        self.assertIn("offer_salesforce_docs_mcp", result["recommended_actions"])

    def test_declined_mcp_and_approved_domains_use_web_fallback(self):
        result = self.module.evaluate(
            self.policy,
            "codex",
            ["web_search"],
            {
                "approved_documentation_domains": "approved",
                "salesforce_docs_mcp_install": "declined",
            },
        )
        self.assertEqual("approved_official_web", result["fallback"])
        self.assertEqual([], result["consent_required"])
        self.assertTrue(result["ready"])

    def test_preference_recorder_writes_no_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / ".advisor" / "capabilities.json"
            subprocess.run(
                [
                    sys.executable,
                    str(RECORD),
                    "--output",
                    str(output),
                    "--harness",
                    "codex",
                    "--documentation-domains",
                    "approved",
                    "--mcp-install",
                    "deferred",
                    "--policy-version",
                    "2026-07-31",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            value = json.loads(output.read_text(encoding="utf-8"))
            self.assertFalse(value["contains_credentials"])
            self.assertEqual("approved", value["approved_documentation_domains"])

    def test_policy_uses_exact_salesforce_hosts(self):
        hosts = self.policy["approved_documentation"]["exact_hosts"]
        self.assertIn("developer.salesforce.com", hosts)
        self.assertNotIn("salesforce.com", hosts)
        self.assertFalse(self.policy["approved_documentation"]["host_security_override"])

    def test_plugin_manifests_package_both_entry_skills(self):
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("oem-isv-advisor", codex["name"])
        self.assertEqual(codex["version"], claude["version"])
        self.assertTrue((ROOT / "skills" / "oem-isv-advisor" / "SKILL.md").exists())
        self.assertTrue((ROOT / "skills" / "advisor-capability-preflight" / "SKILL.md").exists())
        self.assertEqual("./.mcp.json", codex["mcpServers"])
        mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
        self.assertEqual(
            "https://salesforce-docs-76258744c9d7.herokuapp.com/api/mcp",
            mcp["mcpServers"]["salesforce-docs"]["url"],
        )

    def test_openai_metadata_does_not_make_docs_mcp_a_hard_dependency(self):
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertNotIn("dependencies:", metadata)
        self.assertNotIn('value: "salesforce-docs"', metadata)

    def test_entry_skill_requires_preflight_without_copying_domain_knowledge(self):
        entry = (ROOT / "skills" / "oem-isv-advisor" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("$advisor-capability-preflight", entry)
        self.assertIn("references/routing.md", entry)
        self.assertLess(len(entry.splitlines()), 90)

    def test_capability_catalog_has_26_stable_unique_skill_ids(self):
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        ids = [item["id"] for item in catalog["foundation_skills"]]
        ids.extend(capability["id"] for capability in catalog["capabilities"])
        ids.extend(
            skill["id"]
            for capability in catalog["capabilities"]
            for skill in capability["focused_skills"]
        )
        self.assertEqual(26, len(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(list(range(1, 8)), [item["number"] for item in catalog["capabilities"]])
        self.assertEqual(
            4,
            sum(
                skill["maturity"] == "candidate-needs-specialist-depth"
                for capability in catalog["capabilities"]
                for skill in capability["focused_skills"]
            ),
        )


if __name__ == "__main__":
    unittest.main()
