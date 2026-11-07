"""Preview/migrate one Claude Code project plugin; never purge skills or caches.

Uses only documented native Claude plugin commands for installation changes.
Requires an explicitly selected, non-default Claude configuration directory.
No model/session launch, org access, credential handling, or automatic updates.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPO = "forcedotcom/partner-ecosystem-agentic-kit"
MARKET = "partner-ecosystem-agentic-kit"
OLD = "oem-isv-advisor"
NEW = "isv-partner-advisor"
OLD_KEY = f"{OLD}@{MARKET}"
NEW_KEY = f"{NEW}@{MARKET}"
DEFAULT_REF = "main"


def read_json(path: Path) -> dict:
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):
        raise ValueError(f"Refusing a symlinked configuration path: {path}")
    if not path.exists():
        return {}
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def private_json(path: Path, data: dict) -> None:
    # Backups can contain private configuration. Never publish this directory.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")


def payload_hash(root: Path) -> str:
    hashes = {}
    if not (root / "skills").is_dir():
        raise ValueError("Plugin has no complete skills directory.")
    for path in sorted((root / "skills").rglob("*")):
        if path.is_symlink():
            raise ValueError("Refusing symlinked plugin skills; review manually.")
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.is_file():
            hashes[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not hashes:
        raise ValueError("Empty plugin payload.")
    return hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()


def metadata_hashes(root: Path) -> dict:
    result = {}
    for name in (".claude-plugin/plugin.json", ".mcp.json"):
        path = root / name
        read_json(path)  # Apply the same symlink/JSON checks as other metadata.
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    return result


def installation(config: Path, key: str, project: Path) -> dict | None:
    inventory = read_json(config / "plugins/installed_plugins.json")
    if inventory.get("version") != 2 or not isinstance(inventory.get("plugins"), dict):
        raise ValueError("Unrecognized Claude plugin inventory; migrate manually.")
    match = []
    for plugin_key, records in inventory["plugins"].items():
        if not plugin_key.endswith(f"@{MARKET}"):
            continue
        if not isinstance(records, list):
            raise ValueError("Unrecognized installation record.")
        for record in records:
            if (record.get("scope") != "project" or
                    not record.get("projectPath") or
                    Path(record["projectPath"]).resolve() != project):
                raise ValueError("This marketplace is shared with another scope/project. Use a dedicated test profile.")
            if plugin_key == key:
                match.append(record)
    if len(match) > 1:
        raise ValueError("Duplicate installation records need manual review.")
    return match[0] if match else None


def settings_paths(project: Path, config: Path) -> list[Path]:
    return [project / ".claude/settings.json", project / ".claude/settings.local.json",
            config / "settings.json"]


def unrelated_settings(value: dict) -> dict:
    result = json.loads(json.dumps(value))
    for field, keys in (("enabledPlugins", (OLD_KEY, NEW_KEY)),
                        ("extraKnownMarketplaces", (MARKET,))):
        entries = result.get(field, {})
        if not isinstance(entries, dict):
            raise ValueError(f"Unrecognized {field} settings.")
        for key in keys:
            entries.pop(key, None)
        if not entries:
            result.pop(field, None)
    return result


def source_before(config: Path) -> str:
    market = read_json(config / "plugins/known_marketplaces.json").get(MARKET, {})
    source = market.get("source", {})
    if source.get("source") != "github" or source.get("repo") != REPO:
        raise ValueError("Expected the GitHub-backed advisor marketplace. Directory/copy installs need manual migration.")
    raw_location = market.get("installLocation")
    if not isinstance(raw_location, str) or not Path(raw_location).is_absolute() or not Path(raw_location).is_dir():
        raise ValueError("Marketplace has no recognized cached checkout; rollback source cannot be pinned.")
    location = Path(raw_location)
    remote = subprocess.run(["git", "-C", str(location), "config", "--get", "remote.origin.url"],
                            capture_output=True, text=True, check=True, timeout=30).stdout.strip()
    if remote not in (f"https://github.com/{REPO}", f"https://github.com/{REPO}.git", f"git@github.com:{REPO}.git"):
        raise ValueError("Cached marketplace origin does not match the advisor repository.")
    result = subprocess.run(["git", "-C", str(location), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True, timeout=30)
    revision = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", revision):
        raise ValueError("Cannot pin the previous marketplace revision for rollback.")
    return f"{REPO}#{revision}"


def source_declaration(config: Path) -> dict:
    value = read_json(config / "settings.json")
    entry = value.get("extraKnownMarketplaces", {}).get(MARKET, {})
    source = entry.get("source", {})
    if source.get("source") != "github" or source.get("repo") != REPO:
        raise ValueError("Expected this marketplace's GitHub declaration in the selected test profile. Other/managed declarations need manual review.")
    return value


def declare_ref(config: Path, ref: str) -> None:
    # Claude enforces declaration/source agreement before native repointing.
    # Change only our entry in the explicitly selected non-default profile.
    path = config / "settings.json"
    original = path.read_bytes()
    value = source_declaration(config)
    value["extraKnownMarketplaces"][MARKET]["source"]["ref"] = ref
    replace_settings(path, original, value)


def replace_settings(path: Path, original: bytes, value: dict) -> None:
    config = path.parent
    fd, name = tempfile.mkstemp(prefix=".advisor-source-", dir=config)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        if path.read_bytes() != original:
            raise ValueError("Profile settings changed during source update; stop and preview again.")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def declare_recovery_source(config: Path, recovery: Path) -> None:
    path = config / "settings.json"
    original = path.read_bytes()
    value = read_json(path)
    entry = value.get("extraKnownMarketplaces", {}).get(MARKET, {})
    source = entry.get("source", {})
    github = source.get("source") == "github" and source.get("repo") == REPO
    same_recovery = source == {"source": "directory", "path": str(recovery)}
    if not (github or same_recovery):
        raise ValueError("Marketplace declaration changed outside this migration; review recovery manually.")
    entry["source"] = {"source": "directory", "path": str(recovery)}
    replace_settings(path, original, value)


def inspect(project: Path, config: Path, align_project_source: bool = False) -> dict:
    project, config = project.resolve(strict=True), config.resolve(strict=True)
    if not project.is_dir() or not config.is_dir():
        raise ValueError("Project and Claude config must be existing directories.")
    if config == (Path.home() / ".claude").resolve():
        raise ValueError("Do not use your default Claude profile for this candidate test.")
    if project.is_relative_to(config) or config.is_relative_to(project):
        raise ValueError("Keep the test project and config profile separate.")
    paths = settings_paths(project, config)
    settings = {str(path): read_json(path) for path in paths}
    profile_source = MARKET in settings[str(paths[2])].get("extraKnownMarketplaces", {})
    if profile_source:
        source_declaration(config)
    project_source = MARKET in settings[str(paths[0])].get("extraKnownMarketplaces", {})
    if MARKET in settings[str(paths[1])].get("extraKnownMarketplaces", {}):
        raise ValueError("Local marketplace declaration requires manual source alignment.")
    if project_source:
        if not align_project_source:
            raise ValueError("Project marketplace pin found. Preview with --align-project-source to explicitly include only this project's advisor source declaration.")
        source_declaration(project / ".claude")
    if not profile_source and not project_source:
        raise ValueError("No matching marketplace declaration in the selected project/profile; review source manually.")
    for path in paths[1:]:
        enabled = settings[str(path)].get("enabledPlugins", {})
        if OLD_KEY in enabled or NEW_KEY in enabled:
            raise ValueError("Advisor is configured at local/user scope; this helper supports project scope only.")
    # Refuse competing copied entries. Never delete another install method.
    roots = [project, *project.parents, Path.home(), config]
    for root in roots:
        for prefix in (".claude/skills", ".agents/skills", ".cursor/skills", ".opencode/skills", ".codex/skills"):
            for name in (OLD, NEW):
                path = root / prefix / name
                if path.exists() or path.is_symlink():
                    raise ValueError(f"Competing copied skill needs manual review: {path}")
    old = installation(config, OLD_KEY, project)
    new = installation(config, NEW_KEY, project)
    enabled = settings[str(paths[0])].get("enabledPlugins", {})
    if not old or not old.get("installPath"):
        raise ValueError("No recognized old project plugin installation; nothing will be removed.")
    old_root = Path(old["installPath"]).resolve(strict=True)
    if read_json(old_root / ".claude-plugin/plugin.json").get("name") != OLD:
        raise ValueError("Old installation identity does not match its manifest.")
    if new and not (enabled.get(NEW_KEY) is True and enabled.get(OLD_KEY) is False):
        raise ValueError("A partial/competing new install already exists. Review it or roll back before retrying.")
    if not new and enabled.get(OLD_KEY) is not True:
        raise ValueError("The old project plugin is not explicitly enabled.")
    return {"project": str(project), "config": str(config), "settings": settings,
            "align_project_source": project_source,
            "profile_source": profile_source,
            "old_install": old, "old_payload": payload_hash(old_root), "old_metadata": metadata_hashes(old_root),
            "new_install": new, "original_source": source_before(config)}


def native(project: Path, config: Path, args: list[str]) -> None:
    env = {**os.environ, "CLAUDE_CONFIG_DIR": str(config)}
    result = subprocess.run(["claude", "plugin", *args], cwd=project, env=env,
                            capture_output=True, text=True, timeout=240)
    if result.returncode:
        # Do not dump host configuration or potentially sensitive CLI output.
        raise RuntimeError(f"Native plugin command failed: {' '.join(args[:2])} (exit {result.returncode}). Stop and review the private backup.")


def verify_new(project: Path, config: Path) -> None:
    record = installation(config, NEW_KEY, project)
    if not record or not record.get("installPath"):
        raise ValueError("New plugin is missing from the native installation registry.")
    root = Path(record["installPath"]).resolve(strict=True)
    manifest = read_json(root / ".claude-plugin/plugin.json")
    if manifest.get("name") != NEW or manifest.get("version") != (ROOT / "VERSION").read_text().strip():
        raise ValueError("New plugin name/version does not match this reviewed checkout.")
    if not (root / f"skills/{NEW}/SKILL.md").is_file() or (root / f"skills/{OLD}").exists():
        raise ValueError("The renamed entry skill was not installed cleanly.")
    if payload_hash(root) != payload_hash(ROOT):
        raise ValueError("Installed skill hashes differ from this checkout. Do not disable the old plugin.")
    if metadata_hashes(root) != metadata_hashes(ROOT):
        raise ValueError("Installed plugin/MCP metadata differs from this checkout. Do not disable the old plugin.")
    if read_json(project / ".claude/settings.json").get("enabledPlugins", {}).get(NEW_KEY) is not True:
        raise ValueError("New plugin is not enabled in project scope.")


def preserve_unrelated(before: dict) -> None:
    for name, value in before["settings"].items():
        if unrelated_settings(read_json(Path(name))) != unrelated_settings(value):
            raise ValueError("Unrelated settings changed; stop and review the backup before proceeding.")


@contextmanager
def profile_lock(config: Path):
    lock = config / "advisor-rename.lock"
    fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()


def migrate(before: dict, backup: Path, ref: str, runner=native) -> dict:
    project, config = Path(before["project"]), Path(before["config"])
    if before["new_install"]:
        verify_new(project, config)
        return {"status": "already_migrated", "project": str(project)}
    backup = backup.absolute()
    parent = backup.parent.resolve(strict=True)
    backup = parent / backup.name
    if backup.exists() or backup.is_symlink() or any(backup.is_relative_to(p) or p.is_relative_to(backup) for p in (project, config)):
        raise ValueError("Choose a NEW backup directory outside the project and Claude config.")
    with profile_lock(config):
        if inspect(project, config, before["align_project_source"]) != before:
            raise ValueError("Installation changed after preview; inspect again.")
        backup.mkdir(mode=0o700)
        state = {"schema_version": 1, "phase": "backed_up", **before, "candidate_ref": ref}
        private_json(backup / "migration.json", state)
        for index, path in enumerate(settings_paths(project, config) + [config / "plugins/installed_plugins.json", config / "plugins/known_marketplaces.json"]):
            if path.exists():
                shutil.copyfile(path, backup / f"config-{index}.json")
                (backup / f"config-{index}.json").chmod(0o600)
        # Disabled, not uninstalled: preserve the native old payload for rollback.
        # Native inventory may use an OS alias such as /tmp -> /private/tmp.
        # Resolve the install root, then still reject symlinks inside payloads.
        old_root = Path(before["old_install"]["installPath"]).resolve(strict=True)
        try:
            if read_json(ROOT / ".mcp.json") != read_json(old_root / ".mcp.json"):
                raise ValueError("MCP configuration differs. This identity-only migration needs manual review.")
            # Keep a private recovery copy too; rollback normally uses the
            # retained native cache, never overwrites a subsequently edited one.
            recovery = backup / "old-plugin"
            recovery.mkdir(mode=0o700)
            shutil.copytree(old_root / "skills", recovery / "skills",
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (recovery / ".claude-plugin").mkdir()
            shutil.copyfile(old_root / ".claude-plugin/plugin.json", recovery / ".claude-plugin/plugin.json")
            private_json(recovery / ".claude-plugin/marketplace.json", {
                "name": MARKET, "owner": {"name": "Salesforce"}, "plugins": [
                    {"name": OLD, "source": "./", "version": before["old_install"].get("version")} ]})
            if (old_root / ".mcp.json").exists():
                shutil.copyfile(old_root / ".mcp.json", recovery / ".mcp.json")
            if before["profile_source"]:
                declare_ref(config, ref)
            if before["align_project_source"]:
                declare_ref(project / ".claude", ref)
            source_scope = ["--scope", "project"] if before["align_project_source"] else []
            runner(project, config, ["marketplace", "add", f"{REPO}#{ref}", *source_scope])
            state["phase"] = "marketplace_repointed"
            private_json(backup / "migration.json", state)
            runner(project, config, ["install", NEW_KEY, "--scope", "project"])
            verify_new(project, config)
            preserve_unrelated(before)
            if payload_hash(old_root) != before["old_payload"] or metadata_hashes(old_root) != before["old_metadata"]:
                raise ValueError("The old payload changed; stop and review before disabling it.")
            runner(project, config, ["disable", OLD_KEY, "--scope", "project"])
            enabled = read_json(project / ".claude/settings.json").get("enabledPlugins", {})
            if enabled.get(OLD_KEY) is not False:
                raise ValueError("Old project plugin was not disabled.")
            preserve_unrelated(before)
            state["phase"] = "complete"
        except Exception:
            state["phase"] = "needs_review"
            private_json(backup / "migration.json", state)
            raise
        private_json(backup / "migration.json", state)
    return {"status": "migrated_restart_required", "backup": str(backup),
            "old_plugin": "disabled; payload retained", "new_command": f"/{NEW}:{NEW}"}


def rollback(backup: Path, project: Path, config: Path, runner=native) -> dict:
    state = read_json(backup / "migration.json")
    if (state.get("schema_version") != 1 or state.get("project") != str(project) or
            state.get("config") != str(config) or not re.fullmatch(re.escape(REPO) + r"#[0-9a-f]{40,64}", state.get("original_source", ""))):
        raise ValueError("Backup binding/source does not match the selected project/profile.")
    if state.get("phase") == "rolled_back":
        return {"status": "already_rolled_back"}
    old = installation(config, OLD_KEY, project)
    if (not old or any(old.get(k) != state["old_install"].get(k) for k in ("scope", "projectPath", "installPath", "version"))
            or payload_hash(Path(old["installPath"])) != state["old_payload"]
            or metadata_hashes(Path(old["installPath"]).resolve(strict=True)) != state["old_metadata"]):
        raise ValueError("Old native payload is no longer unchanged; manual recovery required.")
    recovery = backup / "old-plugin"
    if (payload_hash(recovery) != state["old_payload"] or metadata_hashes(recovery) != state["old_metadata"] or
            read_json(recovery / ".claude-plugin/plugin.json").get("name") != OLD):
        raise ValueError("Recovery payload does not match the backed-up old plugin.")
    catalog = {"name": MARKET, "owner": {"name": "Salesforce"}, "plugins": [
        {"name": OLD, "source": "./", "version": state["old_install"].get("version")} ]}
    catalog_path = recovery / ".claude-plugin/marketplace.json"
    if catalog_path.exists():
        if read_json(catalog_path) != catalog:
            raise ValueError("Recovery catalog changed; review manually.")
    else:
        private_json(catalog_path, catalog)
    with profile_lock(config):
        if state.get("profile_source", True):
            declare_recovery_source(config, recovery)
        if state.get("align_project_source"):
            declare_recovery_source(project / ".claude", recovery)
        source_scope = ["--scope", "project"] if state.get("align_project_source") else []
        runner(project, config, ["marketplace", "add", str(recovery), *source_scope])
        runner(project, config, ["enable", OLD_KEY, "--scope", "project"])
        if installation(config, NEW_KEY, project):
            runner(project, config, ["disable", NEW_KEY, "--scope", "project"])
        enabled = read_json(project / ".claude/settings.json").get("enabledPlugins", {})
        if enabled.get(OLD_KEY) is not True or enabled.get(NEW_KEY) is True:
            raise ValueError("Rollback settings did not verify; stop and inspect manually.")
        state["phase"] = "rolled_back"
        private_json(backup / "migration.json", state)
    return {"status": "rolled_back_restart_required", "marketplace": "private recovery directory; retain backup until source is changed explicitly", "candidate": "disabled or absent; not deleted"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--claude-config-dir", required=True, type=Path)
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--align-project-source", action="store_true",
                        help="Explicitly include this project's existing advisor marketplace source pin; leave unrelated entries unchanged.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--apply", action="store_true")
    group.add_argument("--rollback", type=Path, metavar="BACKUP")
    args = parser.parse_args()
    try:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", args.ref) or ".." in args.ref:
            raise ValueError("Use an explicit branch or tag in the advisor repository.")
        if re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", args.ref):
            raise ValueError("This Claude CLI clones a branch or tag, not a raw commit. Use a reviewed branch/tag and payload verification.")
        project, config = args.project.expanduser().resolve(strict=True), args.claude_config_dir.expanduser().resolve(strict=True)
        if config == (Path.home() / ".claude").resolve():
            raise ValueError("Select a dedicated non-default test profile, not ~/.claude.")
        if args.rollback:
            if input("Close Claude sessions. Type ROLLBACK to restore this project's old plugin: ") != "ROLLBACK":
                return 1
            print(json.dumps(rollback(args.rollback.expanduser().resolve(strict=True), project, config), indent=2))
            return 0
        before = inspect(project, config, args.align_project_source)
        print(json.dumps({"status": "preview_only", "project": str(project), "claude_config_dir": str(config),
                          "source": f"{REPO}#{args.ref}", "from": OLD_KEY, "to": NEW_KEY,
                          "already_migrated": bool(before["new_install"]),
                          "align_project_source": before["align_project_source"],
                          "profile_source_declaration": before["profile_source"],
                          "steps": ["Back up private configuration", "Align only this marketplace's existing source declaration(s) shown above", "Repoint this test profile's marketplace", "Install and hash-verify new project plugin", "Disable old project plugin; retain its payload"],
                          "scope": "Selected project; marketplace source changes for this entire test profile.",
                          "not_supported": "User/local/managed scopes, copied skills, directory-backed marketplaces, other harnesses, active-session verification"}, indent=2))
        if not args.apply:
            return 0
        if not args.backup_dir:
            raise ValueError("--apply requires --backup-dir outside the project/profile.")
        if input("Close all Claude sessions in this test profile. Type MIGRATE to approve this plan: ") != "MIGRATE":
            return 1
        print(json.dumps(migrate(before, args.backup_dir.expanduser(), args.ref), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError, EOFError) as exc:
        print(f"Stopped safely: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
