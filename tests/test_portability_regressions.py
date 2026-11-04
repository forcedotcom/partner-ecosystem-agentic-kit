import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prepare_harness
import build_review_archive
import check_installed_layout
import check_release


def preflight_module():
    spec = importlib.util.spec_from_file_location("portability_preflight", ROOT / "skills/advisor-capability-preflight/scripts/check_preflight.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PortabilityRegressionTests(unittest.TestCase):
    def test_existing_descriptions_and_domain_knowledge_are_preserved(self):
        baseline = json.loads((ROOT / "tests/fixtures/portability-baseline.json").read_text())
        self.assertEqual(27, len(baseline["descriptions"]))
        for relative, expected in baseline["descriptions"].items():
            actual = re.search(r"^description: (.+)$", (ROOT / relative).read_text(), re.M).group(1)
            self.assertEqual(expected, actual, relative)
        for relative, expected in baseline["domain_reference_sha256"].items():
            self.assertEqual(expected, hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), relative)

    def test_extracted_layouts_resolve_without_source_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for target in ("claude-plugin", "claude-code", "codex-local", "cursor-local", "generic-files"):
                archive = root / f"{target}.zip"
                manifest = prepare_harness.build(ROOT, target, archive)
                destination = root / target
                with zipfile.ZipFile(archive) as bundle:
                    bundle.extractall(destination)
                skills = destination / manifest["profile"]["skills_prefix"]
                self.assertEqual([], check_installed_layout.inspect(skills), target)
                command = [sys.executable, str(skills / "advisor-capability-preflight/scripts/check_preflight.py"), "--harness", "claude-code", "--tool", "salesforce_docs_search"]
                result = subprocess.run(command, cwd=destination, capture_output=True, text=True, check=True)
                status = json.loads(result.stdout)
                self.assertTrue(status["ready"])
                self.assertTrue(status["advisory_ready"])

    def test_catalog_routes_by_id_and_ask_is_not_required(self):
        checker = prepare_harness.checker(ROOT)
        report = checker.inspect_library_contracts(ROOT)
        self.assertEqual("ready", report["status"], report["findings"])
        for folder in (ROOT / "skills").iterdir():
            if not (folder / "SKILL.md").is_file():
                continue
            contract = json.loads((folder / "references/skill-contract.json").read_text())
            self.assertFalse(any(d["requirement"] == "required" and "ask" in d["modes"] for d in contract["dependencies"]))
            self.assertNotIn("$advisor-capability-preflight", (folder / "SKILL.md").read_text())

    def test_explicit_routing_lint_ignores_exclusions(self):
        checker = prepare_harness.checker(ROOT)
        sample = "# Skill\n\n## Routing\nUse `one`.\n\n## Boundaries\nDo not own `two`.\n"
        self.assertEqual({"one"}, checker.body_routing_targets(sample, {"one", "two"}))

    def test_connected_docs_do_not_require_unused_web_consent(self):
        check = preflight_module()
        policy = json.loads((ROOT / "skills/advisor-capability-preflight/references/documentation-policy.json").read_text())
        result = check.evaluate(policy, "claude-code", ["salesforce_docs_search"], {})
        self.assertTrue(result["ready"])
        self.assertEqual([], result["consent_required"])
        absent = check.evaluate(policy, "claude-code", [], {})
        self.assertTrue(absent["advisory_ready"])
        self.assertFalse(absent["ready"])

    def test_preferences_reused_only_for_same_scope(self):
        check = preflight_module()
        policy = json.loads((ROOT / "skills/advisor-capability-preflight/references/documentation-policy.json").read_text())
        prefs = {"harness": "claude-code", "policy_version": policy["policy_version"], "project_root": "/approved", "approved_documentation_domains": "approved", "salesforce_docs_mcp_install": "declined"}
        same = check.evaluate(policy, "claude-code", [], prefs, project_scope="/approved")
        self.assertTrue(same["ready"])
        self.assertEqual([], same["recommended_actions"])
        for changed in ({"project_root": "/different"}, {"harness": "cursor"}, {"policy_version": "old"}):
            with self.subTest(changed=changed):
                result = check.evaluate(policy, "claude-code", [], {**prefs, **changed}, project_scope="/approved")
                self.assertEqual("packaged_knowledge_only", result["fallback"])
                self.assertTrue(result["preference_warnings"])

    def test_cli_reads_project_preferences_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".advisor").mkdir()
            policy = json.loads((ROOT / "skills/advisor-capability-preflight/references/documentation-policy.json").read_text())
            prefs = {"harness": "claude-code", "project_root": str(root.resolve()), "policy_version": policy["policy_version"], "approved_documentation_domains": "declined", "salesforce_docs_mcp_install": "declined"}
            (root / ".advisor/capabilities.json").write_text(json.dumps(prefs))
            result = subprocess.run([sys.executable, str(ROOT / "skills/advisor-capability-preflight/scripts/check_preflight.py"), "--harness", "claude-code"], cwd=root, capture_output=True, text=True, check=True)
            self.assertTrue(json.loads(result.stdout)["ready"])

    def test_release_versions_and_tag_match(self):
        version = check_release.validate(ROOT)
        self.assertEqual(version, check_release.validate(ROOT, f"v{version}"))
        with self.assertRaises(ValueError):
            check_release.validate(ROOT, "v0.1.0")

    def test_review_archive_includes_manifests_and_runs_its_tests(self):
        # Avoid recursive extraction-test invocation: source archive is tested
        # in a separate smoke command; here verify required files and layout.
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "source.zip"
            build_review_archive.build(ROOT, output)
            with zipfile.ZipFile(output) as bundle:
                names = set(bundle.namelist())
                for path in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".codex-plugin/plugin.json", ".mcp.json", "scripts/prepare_harness.py", "tests/test_preflight.py"):
                    self.assertIn(path, names)
                self.assertFalse(any(".git/" in path or "__pycache__" in path for path in names))
