"""Synthetic settings/native-command tests; never repair an actual installation."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import repair_update_source as repair
import migrate_advisor as migration


class UpdateSourceRepairTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.project, self.profile = self.root / "project", self.root / "profile"
        self.plugin, self.backup = self.root / "plugin", self.root / "backup"
        (self.project / ".claude").mkdir(parents=True)
        (self.profile / "plugins").mkdir(parents=True)
        self.copy_plugin()
        self.project_settings = self.project / ".claude/settings.json"
        self.profile_settings = self.profile / "settings.json"
        self.known = self.profile / "plugins/known_marketplaces.json"
        self.inventory = self.profile / "plugins/installed_plugins.json"
        self.write(self.project_settings, {"enabledPlugins": {migration.NEW_KEY: True, migration.OLD_KEY: False,
                    "unrelated@example": True}, "permissions": {"deny": ["SyntheticTool"]},
                    "extraKnownMarketplaces": {migration.MARKET: self.entry()}})
        self.write(self.profile_settings, {"env": {"SYNTHETIC_GATEWAY": "preserve"},
                    "apiKeyHelper": "synthetic-helper-not-run", "hooks": {"SyntheticEvent": []},
                    "extraKnownMarketplaces": {"other-market": {"source": {"source": "github", "repo": "example/other"}}}})
        self.write(self.known, {migration.MARKET: self.entry(), "other-market": {"preserve": 1}})
        self.write(self.inventory, {"version": 2, "plugins": {migration.NEW_KEY: [{
                    "scope": "project", "projectPath": str(self.project), "installPath": str(self.plugin),
                    "version": (ROOT / "VERSION").read_text().strip()}], "unrelated@example": [{"preserve": True}]}})
        self.calls = []

    def copy_plugin(self):
        if self.plugin.exists():
            shutil.rmtree(self.plugin)
        shutil.copytree(ROOT / "skills", self.plugin / "skills", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (self.plugin / ".claude-plugin").mkdir()
        shutil.copyfile(ROOT / ".claude-plugin/plugin.json", self.plugin / ".claude-plugin/plugin.json")
        shutil.copyfile(ROOT / ".mcp.json", self.plugin / ".mcp.json")

    def entry(self, ref=repair.STALE_REF):
        return {"source": {"source": "github", "repo": migration.REPO, "ref": ref}}

    def write(self, path, value):
        path.write_text(json.dumps(value))

    def read(self, path):
        return json.loads(path.read_text())

    def before(self):
        return repair.inspect(self.project, self.profile)

    def native(self, project, profile, args):
        self.assertEqual(self.project, project)
        self.assertEqual(self.profile, profile)
        self.calls.append(args)
        if args[:2] == ["marketplace", "add"]:
            self.assertEqual(f"{migration.REPO}#main", args[2])
            for path in (self.project_settings, self.profile_settings):
                entry = self.read(path).get("extraKnownMarketplaces", {}).get(migration.MARKET)
                if entry:
                    self.assertEqual("main", entry["source"]["ref"])
            known = self.read(self.known)
            known[migration.MARKET]["source"]["ref"] = "main"
            self.write(self.known, known)
        elif args[0] == "update":
            self.assertEqual(["update", migration.NEW_KEY, "--scope", "project"], args)
            self.copy_plugin()

    def test_preview_has_no_writes_backups_or_native_commands(self):
        paths = [self.project_settings, self.profile_settings, self.known, self.inventory]
        before = {p: p.read_bytes() for p in paths}
        result = repair.preview(self.before())
        self.assertEqual("preview_only", result["status"])
        self.assertEqual(before, {p: p.read_bytes() for p in paths})
        self.assertFalse(self.backup.exists())
        self.assertEqual([], self.calls)

    def test_project_only_repair_preserves_scope_settings_and_payload_backup(self):
        original_profile = self.profile_settings.read_bytes()
        original_project = self.read(self.project_settings)
        original_payload = migration.payload_hash(self.plugin)
        result = repair.apply(self.before(), self.backup, self.native)
        self.assertEqual("repaired_updated_restart_required", result["status"])
        self.assertEqual("project", self.calls[0][-1])
        self.assertEqual(original_profile, self.profile_settings.read_bytes())
        original_project["extraKnownMarketplaces"][migration.MARKET]["source"]["ref"] = "main"
        self.assertEqual(original_project, self.read(self.project_settings))
        self.assertEqual(original_payload, migration.payload_hash(self.backup / "installed-plugin"))
        self.assertEqual("complete", self.read(self.backup / "source-repair.json")["phase"])
        self.assertEqual(0o700, self.backup.stat().st_mode & 0o777)
        self.assertEqual(0o600, (self.backup / "source-repair.json").stat().st_mode & 0o777)
        self.assertFalse(any(c[0] in {"install", "uninstall", "enable", "disable"} for c in self.calls))

    def test_profile_only_source_keeps_existing_user_declaration(self):
        project = self.read(self.project_settings)
        del project["extraKnownMarketplaces"]
        self.write(self.project_settings, project)
        profile = self.read(self.profile_settings)
        profile["extraKnownMarketplaces"][migration.MARKET] = self.entry()
        self.write(self.profile_settings, profile)
        repair.apply(self.before(), self.backup, self.native)
        self.assertEqual("user", self.calls[0][-1])
        self.assertNotIn("extraKnownMarketplaces", self.read(self.project_settings))
        self.assertEqual("preserve", self.read(self.profile_settings)["env"]["SYNTHETIC_GATEWAY"])

    def test_both_declarations_align_without_changing_other_settings(self):
        profile = self.read(self.profile_settings)
        profile["extraKnownMarketplaces"][migration.MARKET] = self.entry("main")
        self.write(self.profile_settings, profile)
        repair.apply(self.before(), self.backup, self.native)
        self.assertEqual(profile, self.read(self.profile_settings))
        self.assertEqual("main", self.read(self.project_settings)["extraKnownMarketplaces"][migration.MARKET]["source"]["ref"])

    def test_repeat_run_is_noop(self):
        repair.apply(self.before(), self.backup, self.native)
        count = len(self.calls)
        result = repair.apply(self.before(), self.root / "unused", self.native)
        self.assertEqual("already_tracking_main", result["status"])
        self.assertEqual(count, len(self.calls))
        self.assertFalse((self.root / "unused").exists())

    def test_changed_preview_stops_before_backup_or_commands(self):
        before = self.before()
        profile = self.read(self.profile_settings)
        profile["new_preference"] = True
        self.write(self.profile_settings, profile)
        with self.assertRaisesRegex(ValueError, "changed after preview"):
            repair.apply(before, self.backup, self.native)
        self.assertFalse(self.backup.exists())
        self.assertEqual([], self.calls)

    def test_custom_tags_other_repositories_and_recovery_sources_are_refused(self):
        original = self.read(self.project_settings)
        sources = [{"source": "github", "repo": migration.REPO, "ref": "v0.2.0"},
                   {"source": "github", "repo": "example/other", "ref": repair.STALE_REF},
                   {"source": "directory", "path": "/synthetic/recovery"}]
        for source in sources:
            with self.subTest(source=source):
                changed = copy.deepcopy(original)
                changed["extraKnownMarketplaces"][migration.MARKET]["source"] = source
                self.write(self.project_settings, changed)
                with self.assertRaises(ValueError):
                    self.before()
        self.assertEqual([], self.calls)

    def test_other_project_install_and_user_scope_are_refused(self):
        original = self.read(self.inventory)
        for field, value in (("projectPath", str(self.root / "other-project")), ("scope", "user")):
            changed = copy.deepcopy(original)
            changed["plugins"][migration.NEW_KEY][0][field] = value
            self.write(self.inventory, changed)
            with self.assertRaises(ValueError):
                self.before()

    def test_local_declaration_and_enabled_old_plugin_are_refused(self):
        local = self.project / ".claude/settings.local.json"
        self.write(local, {"extraKnownMarketplaces": {migration.MARKET: self.entry()}})
        with self.assertRaisesRegex(ValueError, "Local-scope"):
            self.before()
        local.unlink()
        project = self.read(self.project_settings)
        project["enabledPlugins"][migration.OLD_KEY] = True
        self.write(self.project_settings, project)
        with self.assertRaisesRegex(ValueError, "already be enabled"):
            self.before()

    def test_shared_inventory_and_missing_declaration_are_refused(self):
        original = self.read(self.inventory)
        changed = copy.deepcopy(original)
        changed["plugins"][migration.NEW_KEY].append({"scope": "project", "projectPath": str(self.root / "other")})
        self.write(self.inventory, changed)
        with self.assertRaises(ValueError):
            self.before()
        self.write(self.inventory, original)
        project = self.read(self.project_settings)
        del project["extraKnownMarketplaces"]
        self.write(self.project_settings, project)
        with self.assertRaisesRegex(ValueError, "No existing"):
            self.before()

    def test_backup_inside_runtime_or_existing_backup_is_refused(self):
        for backup in (self.project / "backup", self.profile / "backup", self.plugin,
                       self.root / ".agents" / "backup"):
            if backup.parent.name == ".agents":
                backup.parent.mkdir(exist_ok=True)
            with self.assertRaises(ValueError):
                repair.apply(self.before(), backup, self.native)
        self.assertEqual([], self.calls)

    def test_failure_is_private_and_retains_backup_for_review(self):
        def fail(project, profile, args):
            if args[:2] == ["marketplace", "update"]:
                raise RuntimeError("synthetic refresh failed")
            self.native(project, profile, args)
        before = self.before()
        with self.assertRaisesRegex(RuntimeError, "synthetic refresh"):
            repair.apply(before, self.backup, fail)
        state = self.read(self.backup / "source-repair.json")
        self.assertEqual("needs_review", state["phase"])
        self.assertEqual(before["installed_payload"], migration.payload_hash(self.backup / "installed-plugin"))
        self.assertFalse((self.profile / "advisor-rename.lock").exists())

    def test_unrelated_settings_change_prevents_plugin_update(self):
        def tamper(project, profile, args):
            self.native(project, profile, args)
            if args[:2] == ["marketplace", "update"]:
                value = self.read(self.profile_settings)
                value["env"]["SYNTHETIC_GATEWAY"] = "changed"
                self.write(self.profile_settings, value)
        with self.assertRaisesRegex(ValueError, "Unrelated settings"):
            repair.apply(self.before(), self.backup, tamper)
        self.assertFalse(any(c[0] == "update" for c in self.calls))

    def test_wrong_updated_payload_is_not_success(self):
        def tamper(project, profile, args):
            self.native(project, profile, args)
            if args[0] == "update":
                (self.plugin / f"skills/{migration.NEW}/SKILL.md").write_text("unexpected payload")
        with self.assertRaisesRegex(ValueError, "hashes differ"):
            repair.apply(self.before(), self.backup, tamper)
        self.assertEqual("needs_review", self.read(self.backup / "source-repair.json")["phase"])

    def test_cli_decline_and_apply_without_backup_make_no_changes(self):
        args = ["repair_update_source.py", "--project", str(self.project),
                "--claude-config-dir", str(self.profile), "--apply"]
        before = self.project_settings.read_bytes()
        with patch.object(sys, "argv", args), patch("builtins.print"):
            self.assertEqual(1, repair.main())
        with patch.object(sys, "argv", args + ["--backup-dir", str(self.backup)]), \
                patch("builtins.input", return_value="decline"), patch("builtins.print"):
            self.assertEqual(1, repair.main())
        self.assertEqual(before, self.project_settings.read_bytes())
        self.assertFalse(self.backup.exists())

    def test_mcp_change_and_symlinked_settings_are_refused(self):
        self.write(self.plugin / ".mcp.json", {"mcpServers": {"unexpected": {}}})
        with self.assertRaisesRegex(ValueError, "MCP configuration"):
            self.before()
        shutil.copyfile(ROOT / ".mcp.json", self.plugin / ".mcp.json")
        renamed = self.project_settings.with_suffix(".original")
        self.project_settings.rename(renamed)
        self.project_settings.symlink_to(renamed)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            self.before()


if __name__ == "__main__":
    unittest.main()
