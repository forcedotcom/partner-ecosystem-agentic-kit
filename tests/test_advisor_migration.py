"""Synthetic native-command tests: no actual user install is changed."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import migrate_advisor as migration


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.project = self.root / "project"
        self.config = self.root / "test-profile"
        self.old = self.root / "old-plugin"
        self.new = self.root / "new-plugin"
        self.backup = self.root / "private-backup"
        (self.project / ".claude").mkdir(parents=True)
        (self.config / "plugins").mkdir(parents=True)
        (self.old / ".claude-plugin").mkdir(parents=True)
        (self.old / f"skills/{migration.OLD}").mkdir(parents=True)
        (self.old / f"skills/{migration.OLD}/SKILL.md").write_text("Old synthetic entry; OEM licensing knowledge stays.\n")
        self.write(self.old / ".claude-plugin/plugin.json", {"name": migration.OLD, "version": "0.2.0"})
        shutil.copyfile(ROOT / ".mcp.json", self.old / ".mcp.json")
        self.settings = self.project / ".claude/settings.json"
        self.write(self.settings, {"enabledPlugins": {migration.OLD_KEY: True, "other@other": True},
                                   "permissions": {"deny": ["SyntheticUnrelatedTool"]}})
        self.write(self.config / "settings.json", {"unrelated": "preserve"})
        self.inventory = self.config / "plugins/installed_plugins.json"
        self.write(self.inventory, {"version": 2, "plugins": {migration.OLD_KEY: [
            {"scope": "project", "projectPath": str(self.project), "installPath": str(self.old), "version": "0.2.0"}]}})
        self.write(self.config / "plugins/known_marketplaces.json", {
            migration.MARKET: {"source": {"source": "github", "repo": migration.REPO}}})
        self.source_patch = patch.object(migration, "source_before", return_value=migration.REPO + "#" + "a" * 40)
        self.source_patch.start()
        self.addCleanup(self.source_patch.stop)
        self.calls = []

    def write(self, path, value):
        path.write_text(json.dumps(value))

    def native(self, project, config, args):
        self.assertEqual(self.project, project)
        self.assertEqual(self.config, config)
        self.calls.append(args)
        if args[:2] == ["marketplace", "add"]:
            return
        if args[0] == "install":
            shutil.copytree(ROOT / "skills", self.new / "skills", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree(ROOT / ".claude-plugin", self.new / ".claude-plugin")
            inventory = migration.read_json(self.inventory)
            inventory["plugins"][migration.NEW_KEY] = [{"scope": "project", "projectPath": str(project),
                "installPath": str(self.new), "version": (ROOT / "VERSION").read_text().strip()}]
            self.write(self.inventory, inventory)
        settings = migration.read_json(self.settings)
        settings["enabledPlugins"][args[1]] = args[0] != "disable"
        self.write(self.settings, settings)

    def before(self):
        return migration.inspect(self.project, self.config)

    def apply(self, runner=None):
        return migration.migrate(self.before(), self.backup, migration.DEFAULT_REF, runner or self.native)

    def test_preview_is_read_only(self):
        paths = [self.settings, self.inventory, self.config / "settings.json"]
        before = {str(p): p.read_bytes() for p in paths}
        result = self.before()
        self.assertIsNone(result["new_install"])
        self.assertEqual(before, {str(p): p.read_bytes() for p in paths})
        self.assertFalse(self.backup.exists())
        self.assertEqual([], self.calls)

    def test_success_verifies_before_disabling_old_and_is_idempotent(self):
        old_hash = migration.payload_hash(self.old)
        result = self.apply()
        self.assertEqual("migrated_restart_required", result["status"])
        self.assertEqual(["disable", migration.OLD_KEY, "--scope", "project"], self.calls[-1])
        self.assertEqual(old_hash, migration.payload_hash(self.old))
        self.assertEqual(old_hash, migration.payload_hash(self.backup / "old-plugin"))
        self.assertEqual(0o700, self.backup.stat().st_mode & 0o777)
        self.assertEqual(0o600, (self.backup / "migration.json").stat().st_mode & 0o777)
        count = len(self.calls)
        self.assertEqual("already_migrated", migration.migrate(self.before(), self.backup, migration.DEFAULT_REF, self.native)["status"])
        self.assertEqual(count, len(self.calls))

    def test_failed_install_preserves_old_and_records_recovery(self):
        def fail(project, config, args):
            if args[0] == "install":
                raise RuntimeError("synthetic native failure")
            self.native(project, config, args)
        with self.assertRaises(RuntimeError):
            self.apply(fail)
        self.assertTrue(migration.read_json(self.settings)["enabledPlugins"][migration.OLD_KEY])
        self.assertEqual("needs_review", migration.read_json(self.backup / "migration.json")["phase"])
        self.assertFalse((self.config / "advisor-rename.lock").exists())

    def test_wrong_candidate_hash_does_not_disable_old(self):
        def tamper(project, config, args):
            self.native(project, config, args)
            if args[0] == "install":
                (self.new / f"skills/{migration.NEW}/SKILL.md").write_text("different build")
        with self.assertRaisesRegex(ValueError, "hashes differ"):
            self.apply(tamper)
        self.assertTrue(migration.read_json(self.settings)["enabledPlugins"][migration.OLD_KEY])

    def test_unrelated_setting_change_stops_before_disabling(self):
        def tamper(project, config, args):
            self.native(project, config, args)
            if args[0] == "install":
                settings = migration.read_json(self.settings)
                settings["permissions"] = {"allow": ["unexpected"]}
                self.write(self.settings, settings)
        with self.assertRaisesRegex(ValueError, "Unrelated settings"):
            self.apply(tamper)
        self.assertTrue(migration.read_json(self.settings)["enabledPlugins"][migration.OLD_KEY])

    def test_rollback_preserves_later_unrelated_settings(self):
        self.apply()
        settings = migration.read_json(self.settings)
        settings["a_later_user_preference"] = 42
        self.write(self.settings, settings)
        result = migration.rollback(self.backup, self.project, self.config, self.native)
        self.assertEqual("rolled_back_restart_required", result["status"])
        settings = migration.read_json(self.settings)
        self.assertEqual(42, settings["a_later_user_preference"])
        self.assertTrue(settings["enabledPlugins"][migration.OLD_KEY])
        self.assertFalse(settings["enabledPlugins"][migration.NEW_KEY])
        self.assertEqual(migration.REPO + "#" + "a" * 40, self.calls[-3][2])

    def test_rollback_refuses_edited_old_payload_or_wrong_binding(self):
        self.apply()
        with self.assertRaisesRegex(ValueError, "binding"):
            migration.rollback(self.backup, self.root, self.config, self.native)
        (self.old / f"skills/{migration.OLD}/SKILL.md").write_text("local edits")
        count = len(self.calls)
        with self.assertRaisesRegex(ValueError, "unchanged"):
            migration.rollback(self.backup, self.project, self.config, self.native)
        self.assertEqual(count, len(self.calls))

    def test_cross_project_or_user_scope_marketplace_is_blocked(self):
        for scope, project in (("user", None), ("project", str(self.root / "other-project"))):
            with self.subTest(scope=scope):
                inventory = migration.read_json(self.inventory)
                inventory["plugins"][migration.NEW_KEY] = [{"scope": scope, "projectPath": project}]
                self.write(self.inventory, inventory)
                with self.assertRaisesRegex(ValueError, "shared"):
                    self.before()

    def test_local_scope_and_copied_entries_are_blocked(self):
        local = self.project / ".claude/settings.local.json"
        self.write(local, {"enabledPlugins": {migration.OLD_KEY: False}})
        with self.assertRaisesRegex(ValueError, "local/user scope"):
            self.before()
        local.unlink()
        (self.project / f".claude/skills/{migration.OLD}").mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "Competing copied skill"):
            self.before()

    def test_backup_inside_project_or_existing_path_is_refused(self):
        for backup in (self.project / "backup", self.config / "backup", self.root):
            with self.subTest(backup=backup):
                with self.assertRaises(ValueError):
                    migration.migrate(self.before(), backup, migration.DEFAULT_REF, self.native)
        self.assertFalse(self.calls)

    def test_symlink_config_and_skill_payloads_are_refused(self):
        other = self.root / "other.json"
        other.write_text("{}")
        target = self.project / ".claude/settings.local.json"
        target.symlink_to(other)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.before()
        target.unlink()
        (self.old / "skills/linked.md").symlink_to(other)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.before()

    def test_real_source_reader_pins_github_and_rejects_directory_sources(self):
        self.source_patch.stop()
        known = self.config / "plugins/known_marketplaces.json"
        self.write(known, {migration.MARKET: {"source": {"source": "directory", "path": str(self.old)}}})
        with self.assertRaisesRegex(ValueError, "GitHub-backed"):
            migration.source_before(self.config)
        self.write(known, {migration.MARKET: {"source": {"source": "github", "repo": migration.REPO},
                                           "installLocation": str(self.old)}})
        with patch.object(migration.subprocess, "run") as run:
            from types import SimpleNamespace
            run.side_effect = [SimpleNamespace(stdout=f"https://github.com/{migration.REPO}.git\n"),
                               SimpleNamespace(stdout="b" * 40 + "\n")]
            self.assertEqual(migration.REPO + "#" + "b" * 40, migration.source_before(self.config))

    def test_changed_preview_stops_without_native_commands(self):
        before = self.before()
        settings = migration.read_json(self.settings)
        settings["new_user_preference"] = "preserve me"
        self.write(self.settings, settings)
        with self.assertRaisesRegex(ValueError, "changed after preview"):
            migration.migrate(before, self.backup, migration.DEFAULT_REF, self.native)
        self.assertFalse(self.backup.exists())
        self.assertFalse(self.calls)

    def test_native_command_is_bound_to_explicit_project_profile(self):
        from types import SimpleNamespace
        with patch.object(migration.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as run:
            migration.native(self.project, self.config, ["disable", migration.OLD_KEY, "--scope", "project"])
        args, kwargs = run.call_args
        self.assertEqual(["claude", "plugin", "disable", migration.OLD_KEY, "--scope", "project"], args[0])
        self.assertEqual(str(self.config), kwargs["env"]["CLAUDE_CONFIG_DIR"])
        self.assertEqual(self.project, kwargs["cwd"])
        self.assertNotIn("shell", kwargs)


if __name__ == "__main__":
    unittest.main()
