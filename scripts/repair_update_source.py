"""Preview a narrowly scoped repair of the deleted advisor marketplace pin.

No default-profile repair, uninstall, global cleanup, model launch, or org call.
Apply requires a private backup and typed confirmation. Native update commands
run only after this advisor's existing source declarations have been aligned.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import migrate_advisor as migration

ROOT = Path(__file__).resolve().parents[1]
STALE_REF = "codex/isv-partner-advisor-migration"
TARGET_REF = "main"


def check_source(source: dict) -> None:
    if (not isinstance(source, dict) or source.get("source") != "github" or source.get("repo") != migration.REPO
            or source.get("ref") not in (None, TARGET_REF, STALE_REF)):
        raise ValueError("Only this advisor's deleted rename pin can be repaired; custom sources/tags need manual review.")


def file_state(path: Path) -> dict:
    value = migration.read_json(path)
    return {"value": value, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()
            if path.exists() else None}


def inspect(project: Path, config: Path) -> dict:
    project, config = project.resolve(strict=True), config.resolve(strict=True)
    if not project.is_dir() or not config.is_dir():
        raise ValueError("Select existing project/profile directories.")
    if config == (Path.home() / ".claude").resolve():
        raise ValueError("Select the existing dedicated non-default test profile, not ~/.claude.")
    if project.is_relative_to(config) or config.is_relative_to(project):
        raise ValueError("Keep project and profile separate.")
    paths = migration.settings_paths(project, config)
    settings = {str(p): file_state(p) for p in paths}
    scopes, stale = {}, False
    for path, scope in zip(paths, ("project", "local", "user")):
        value = settings[str(path)]["value"]
        if not isinstance(value.get("extraKnownMarketplaces", {}), dict):
            raise ValueError("Unrecognized marketplace declaration.")
        entry = value.get("extraKnownMarketplaces", {}).get(migration.MARKET)
        if entry is not None:
            if not isinstance(entry, dict):
                raise ValueError("Unrecognized advisor marketplace declaration.")
            if scope == "local":
                raise ValueError("Local-scope source declaration needs manual review.")
            check_source(entry.get("source", {}))
            scopes[str(path)] = scope
            stale |= entry["source"].get("ref") == STALE_REF
        enabled = value.get("enabledPlugins", {})
        if not isinstance(enabled, dict):
            raise ValueError("Unrecognized plugin settings.")
        if scope != "project" and any(k in enabled for k in (migration.NEW_KEY, migration.OLD_KEY)):
            raise ValueError("Only a project-scoped advisor in a dedicated profile is supported.")
    if not scopes:
        raise ValueError("No existing advisor source declaration; refusing to create one.")
    project_enabled = settings[str(paths[0])]["value"].get("enabledPlugins", {})
    if project_enabled.get(migration.NEW_KEY) is not True or project_enabled.get(migration.OLD_KEY) is True:
        raise ValueError("The renamed advisor must already be enabled and the old advisor disabled; use migration otherwise.")
    record = migration.installation(config, migration.NEW_KEY, project)
    if not record or not record.get("installPath"):
        raise ValueError("No existing renamed project plugin; this helper never installs another copy.")
    root = Path(record["installPath"]).resolve(strict=True)
    manifest = migration.read_json(root / ".claude-plugin/plugin.json")
    if manifest.get("name") != migration.NEW or manifest.get("version") != record.get("version"):
        raise ValueError("Installed identity/version does not match its native record.")
    if not (root / f"skills/{migration.NEW}/SKILL.md").is_file():
        raise ValueError("Installed renamed entry is missing.")
    # Source repair must not silently introduce a new integration configuration.
    if migration.read_json(root / ".mcp.json") != migration.read_json(ROOT / ".mcp.json"):
        raise ValueError("Reviewed MCP configuration differs; stop for a separate update review.")
    known_path = config / "plugins/known_marketplaces.json"
    known = file_state(known_path)
    registered = known["value"].get(migration.MARKET, {})
    if not isinstance(registered, dict):
        raise ValueError("Unrecognized native marketplace registration.")
    check_source(registered.get("source", {}))
    stale |= registered["source"].get("ref") == STALE_REF
    inventory_path = config / "plugins/installed_plugins.json"
    return {"project": str(project), "config": str(config), "settings": settings,
            "source_scopes": scopes, "known": known,
            "inventory": file_state(inventory_path), "installed": record,
            "installed_payload": migration.payload_hash(root),
            "installed_metadata": migration.metadata_hashes(root),
            "target_payload": migration.payload_hash(ROOT),
            "target_metadata": migration.metadata_hashes(ROOT),
            "needs_repair": bool(stale)}


def preview(before: dict) -> dict:
    return {"status": "preview_only" if before["needs_repair"] else "already_tracking_main",
            "project": before["project"], "claude_config_dir": before["config"],
            "from_ref": STALE_REF if before["needs_repair"] else TARGET_REF,
            "to_ref": TARGET_REF, "existing_source_scopes": before["source_scopes"],
            "installed_version": before["installed"]["version"],
            "reviewed_version": (ROOT / "VERSION").read_text().strip(),
            "target_payload_sha256": before["target_payload"],
            "steps": ["Back up private settings and the currently installed plugin",
                      "Align only existing advisor source declarations to main",
                      "Re-register the same marketplace at its existing scope",
                      "Refresh marketplace and update the same project plugin",
                      "Verify reviewed payload and unchanged unrelated settings"],
            "limitations": "Dedicated profile, one project-scoped renamed plugin only. Close all sessions using it. No model or org verification."}


def without_source_ref(value: dict) -> dict:
    result = json.loads(json.dumps(value))
    source = result.get("extraKnownMarketplaces", {}).get(migration.MARKET, {}).get("source", {})
    source.pop("ref", None)
    return result


def verify_unchanged(before: dict) -> None:
    for name, state in before["settings"].items():
        current = migration.read_json(Path(name))
        if without_source_ref(current) != without_source_ref(state["value"]):
            raise ValueError("Unrelated settings or plugin enablement changed; stop and inspect the private backup.")
        if name in before["source_scopes"]:
            source = current["extraKnownMarketplaces"][migration.MARKET]["source"]
            if source.get("ref") != TARGET_REF:
                raise ValueError("Saved source did not verify as main.")
    config = Path(before["config"])
    known = migration.read_json(config / "plugins/known_marketplaces.json")
    source = known.get(migration.MARKET, {}).get("source", {})
    check_source(source)
    if source.get("ref") != TARGET_REF:
        raise ValueError("Native marketplace registry did not verify as main.")
    for key, value in before["known"]["value"].items():
        if key != migration.MARKET and known.get(key) != value:
            raise ValueError("Another marketplace changed; manual review required.")
    if set(known) != set(before["known"]["value"]):
        raise ValueError("Marketplace inventory changed unexpectedly.")
    old_inventory = before["inventory"]["value"]
    inventory = migration.read_json(config / "plugins/installed_plugins.json")
    prior = json.loads(json.dumps(old_inventory))
    after = json.loads(json.dumps(inventory))
    prior["plugins"].pop(migration.NEW_KEY, None)
    after["plugins"].pop(migration.NEW_KEY, None)
    if prior != after:
        raise ValueError("Another plugin's inventory changed; manual review required.")


def apply(before: dict, backup: Path, runner=migration.native) -> dict:
    project, config = Path(before["project"]), Path(before["config"])
    if not before["needs_repair"]:
        if inspect(project, config) != before:
            raise ValueError("State changed after preview; preview again.")
        return {"status": "already_tracking_main", "update": "Use ordinary same-ID updates; no repair ran."}
    backup = backup.expanduser().absolute()
    parent = backup.parent.resolve(strict=True)
    backup = parent / backup.name
    if (backup.exists() or backup.is_symlink() or
            any(backup.is_relative_to(p) or p.is_relative_to(backup) for p in (project, config, ROOT)) or
            any(p in {".claude", ".agents", ".cursor", ".opencode", ".codex"} for p in backup.parts)):
        raise ValueError("Choose a NEW private backup outside project, profile, checkout, and skill-discovery folders.")
    with migration.profile_lock(config):
        if inspect(project, config) != before:
            raise ValueError("Installation/configuration changed after preview; preview again.")
        backup.mkdir(mode=0o700)
        state = {"schema_version": 1, "phase": "backed_up", "before": before}
        migration.private_json(backup / "source-repair.json", state)
        originals = [*migration.settings_paths(project, config),
                     config / "plugins/installed_plugins.json", config / "plugins/known_marketplaces.json"]
        for i, path in enumerate(originals):
            if path.exists():
                destination = backup / f"config-{i}.json"
                shutil.copyfile(path, destination)
                destination.chmod(0o600)
        installed = Path(before["installed"]["installPath"]).resolve(strict=True)
        recovery = backup / "installed-plugin"
        recovery.mkdir(mode=0o700)
        shutil.copytree(installed / "skills", recovery / "skills", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (recovery / ".claude-plugin").mkdir()
        shutil.copyfile(installed / ".claude-plugin/plugin.json", recovery / ".claude-plugin/plugin.json")
        if (installed / ".mcp.json").exists():
            shutil.copyfile(installed / ".mcp.json", recovery / ".mcp.json")
        if (migration.payload_hash(recovery) != before["installed_payload"] or
                migration.metadata_hashes(recovery) != before["installed_metadata"]):
            raise ValueError("Backup payload did not verify; no source change attempted.")
        try:
            for name in before["source_scopes"]:
                path = Path(name)
                current = file_state(path)
                if current != before["settings"][name]:
                    raise ValueError("Settings changed during backup; preview again.")
                updated = current["value"]
                updated["extraKnownMarketplaces"][migration.MARKET]["source"]["ref"] = TARGET_REF
                migration.replace_settings(path, path.read_bytes(), updated)
            state["phase"] = "declarations_aligned"
            migration.private_json(backup / "source-repair.json", state)
            scope = "project" if "project" in before["source_scopes"].values() else "user"
            runner(project, config, ["marketplace", "add", f"{migration.REPO}#{TARGET_REF}", "--scope", scope])
            runner(project, config, ["marketplace", "update", migration.MARKET])
            state["phase"] = "source_repaired"
            migration.private_json(backup / "source-repair.json", state)
            verify_unchanged(before)
            runner(project, config, ["update", migration.NEW_KEY, "--scope", "project"])
            migration.verify_new(project, config)
            verify_unchanged(before)
            state["phase"] = "complete"
        except Exception:
            state["failed_after"] = state["phase"]
            state["phase"] = "needs_review"
            migration.private_json(backup / "source-repair.json", state)
            raise
        migration.private_json(backup / "source-repair.json", state)
    return {"status": "repaired_updated_restart_required", "backup": str(backup),
            "source_ref": TARGET_REF, "plugin": migration.NEW_KEY,
            "installed_version": (ROOT / "VERSION").read_text().strip(),
            "verification": "Native inventory and reviewed payload; start a fresh session to verify actual loading."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--claude-config-dir", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-dir", type=Path)
    args = parser.parse_args()
    try:
        before = inspect(args.project.expanduser(), args.claude_config_dir.expanduser())
        print(json.dumps(preview(before), indent=2))
        if not args.apply or not before["needs_repair"]:
            return 0
        if not args.backup_dir:
            raise ValueError("--apply requires --backup-dir; no changes were made.")
        if input("Close all sessions using this profile. Type REPAIR to approve the preview: ") != "REPAIR":
            return 1
        print(json.dumps(apply(before, args.backup_dir), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError, EOFError) as exc:
        # Native output/configuration may contain secrets; do not echo it.
        print(f"Stopped safely: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
