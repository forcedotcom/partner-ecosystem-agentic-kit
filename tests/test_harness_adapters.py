import copy
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("prepare_harness", ROOT / "scripts/prepare_harness.py")
ADAPTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADAPTER)


class HarnessAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)

    def test_all_targets_preserve_identical_skill_content(self):
        hashes = set()
        for target in ("codex-local", "claude-code", "claude-plugin", "cursor-local", "claude-app", "generic-files"):
            path = self.output / f"{target}.zip"
            manifest = ADAPTER.build(ROOT, target, path)
            hashes.add(manifest["payload_sha256"])
            self.assertEqual(27, len(manifest["skill_versions"]))
            self.assertIn(manifest["library_release"], (None, "v" + (ROOT / "VERSION").read_text().strip()))
            with zipfile.ZipFile(path) as bundle:
                record = json.loads(bundle.read("session-record.json"))
                self.assertEqual("review_required", ADAPTER.inspect_record(record, manifest)["status"])
                self.assertEqual("not_tested", manifest["behavioral_status"])
                self.assertFalse(any("tests/" in name or "transcript" in name for name in bundle.namelist()))
                restored = {}
                if target == "claude-app":
                    self.assertEqual(27, len([p for p in bundle.namelist() if p.endswith(".zip")]))
                    for name in manifest["skill_versions"]:
                        with zipfile.ZipFile(io.BytesIO(bundle.read(f"skill-zips/{name}.zip"))) as skill_zip:
                            for member in skill_zip.namelist():
                                restored[f"skills/{member}"] = ADAPTER.digest(skill_zip.read(member))
                else:
                    prefix = manifest["profile"]["skills_prefix"] + "/"
                    for member in bundle.namelist():
                        if member.startswith(prefix):
                            restored["skills/" + member.removeprefix(prefix)] = ADAPTER.digest(bundle.read(member))
                self.assertEqual(manifest["file_sha256"], restored)
        self.assertEqual(1, len(hashes))

    def complete_record(self):
        path = self.output / "record.zip"
        manifest = ADAPTER.build(ROOT, "claude-code", path)
        with zipfile.ZipFile(path) as bundle:
            record = json.loads(bundle.read("session-record.json"))
        record.update(surface="terminal", app_version="test-fixture", model="test-fixture", tested_at="2026-11-04T12:00:00Z", installation_method="disposable-test-fixture", reviewer="unit-test", tool_catalog_status="unavailable", documentation_mcp="unavailable")
        for check in record["checks"].values():
            check.update(status="pass", evidence="Unit-test fixture only; not actual harness evidence.")
        record["loaded_skills"] = [{"id": "oem-isv-advisor", "base_directory": "/unit-test/skills/oem-isv-advisor", "version": manifest["skill_versions"]["oem-isv-advisor"], "skill_md_sha256": manifest["file_sha256"]["skills/oem-isv-advisor/SKILL.md"]}]
        record["visible_skill_sources"] = ["unit-test-fixture-only"]
        record["upgrade"] = {"from_version": "0.1.0", "to_version": "0.2.0-rc.1", "delivery_path": "unit-test", "evidence": "Fixture only, not real host evidence."}
        return record, manifest

    def test_complete_record_is_self_reported_not_certified(self):
        record, manifest = self.complete_record()
        report = ADAPTER.inspect_record(record, manifest)
        self.assertEqual("reported_pass", report["status"])
        self.assertIn("not independent", report["verification"])

    def test_changed_payload_profile_or_missing_evidence_needs_review(self):
        record, manifest = self.complete_record()
        for key in ("payload_sha256", "profile_sha256", "target", "library_head_sha"):
            changed = copy.deepcopy(record)
            changed[key] = "different"
            self.assertEqual("review_required", ADAPTER.inspect_record(changed, manifest)["status"])
        record["checks"]["contract_read"]["evidence"] = None
        self.assertEqual("review_required", ADAPTER.inspect_record(record, manifest)["status"])

    def test_cannot_overwrite_or_export_installation_directory(self):
        target = self.output / "existing.zip"
        target.write_bytes(b"preserve")
        with self.assertRaises(ValueError):
            ADAPTER.build(ROOT, "cursor-local", target)
        self.assertEqual(b"preserve", target.read_bytes())
        with self.assertRaises(ValueError):
            ADAPTER.build(ROOT, "cursor-local", self.output / ".cursor/skills")

    def test_invalid_time_or_unobserved_connection_needs_review(self):
        record, manifest = self.complete_record()
        for value in ("2026-11-04", "2026-99-04T12:00:00Z", "2026-11-04T12:00:00"):
            changed = copy.deepcopy(record)
            changed["tested_at"] = value
            self.assertEqual("review_required", ADAPTER.inspect_record(changed, manifest)["status"])
        record["documentation_mcp"] = "connected"
        self.assertEqual("review_required", ADAPTER.inspect_record(record, manifest)["status"])

    def test_changed_manifest_inventory_is_detected(self):
        record, manifest = self.complete_record()
        manifest["file_sha256"]["skills/oem-isv-advisor/SKILL.md"] = "changed"
        self.assertEqual("review_required", ADAPTER.inspect_record(record, manifest)["status"])

    def test_symlinks_and_hidden_payloads_are_rejected(self):
        root = self.output / "library"
        shutil.copytree(ROOT / "skills", root / "skills", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "adapters", root / "adapters")
        hidden = root / "skills/oem-isv-advisor/references/.env"
        hidden.write_text("benign-test")
        with self.assertRaisesRegex(ValueError, "Hidden"):
            ADAPTER.build(root, "cursor-local", self.output / "hidden.zip")
        hidden.unlink()
        link = hidden.with_name("escape.md")
        link.symlink_to(ROOT / "README.md")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            ADAPTER.build(root, "cursor-local", self.output / "linked.zip")

    def test_missing_contract_reference_stops_packaging(self):
        root = self.output / "library"
        shutil.copytree(ROOT / "skills", root / "skills", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "adapters", root / "adapters")
        (root / "skills/development-environment/references/skill-contract.json").unlink()
        with self.assertRaisesRegex(ValueError, "contract/catalog"):
            ADAPTER.build(root, "cursor-local", self.output / "missing.zip")


if __name__ == "__main__":
    unittest.main()
