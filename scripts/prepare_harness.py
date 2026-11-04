"""Build review-only skill bundles and inspect self-reported compatibility.

No installs, extraction, app launches, network calls, or configuration edits.
This maintainer utility is not a sandbox and never certifies harness behavior.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ("discovery", "contract_read", "related_skill_resolution", "routing_and_synthesis",
          "missing_tool_fallback", "assess_boundary", "act_approval_boundary", "context_recovery",
          "candidate_isolation")
IGNORED_DIRS = {"__pycache__", ".git"}
ALLOWED_DIRS = {"references", "scripts", "assets", "agents"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def profile_for(root: Path, target: str) -> dict:
    profiles = json.loads((root / "adapters/profiles.json").read_text())["profiles"]
    return next(p for p in profiles if p["id"] == target)


def checker(root: Path):
    path = root / "skills/oem-isv-advisor/scripts/check_skill_contracts.py"
    spec = importlib.util.spec_from_file_location("advisor_contract_checker", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def payload(root: Path) -> tuple[dict[str, bytes], dict[str, str]]:
    report = checker(root).inspect_library_contracts(root)
    if report["status"] != "ready":
        raise ValueError("Fix contract/catalog blockers before exporting a harness bundle.")
    files, versions = {}, {}
    for skill in report["skills"]:
        name = skill["skill"]
        if not skill["skill_version"]:
            raise ValueError(f"Declare an individual version before packaging {name}.")
        versions[name] = skill["skill_version"]
        folder = root / "skills" / name
        if folder.is_symlink():
            raise ValueError(f"Symlinked skill cannot be packaged: {name}")
        for path in sorted(folder.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symlink cannot be packaged: {name}/{path.relative_to(folder)}")
            relative = path.relative_to(folder)
            if any("\\" in part or ":" in part for part in relative.parts):
                raise ValueError(f"Nonportable payload path: {name}/{relative}")
            if any(part in IGNORED_DIRS for part in relative.parts) or path.suffix == ".pyc":
                continue
            if not path.is_file():
                continue
            if any(part.startswith(".") for part in relative.parts):
                raise ValueError(f"Hidden file cannot be packaged: {name}/{relative}")
            if str(relative) != "SKILL.md" and relative.parts[0] not in ALLOWED_DIRS:
                raise ValueError(f"Unexpected skill payload file: {name}/{relative}")
            files[f"skills/{name}/{relative.as_posix()}"] = path.read_bytes()
    return files, versions


def archive(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data)
    return stream.getvalue()


def git_head(root: Path) -> str | None:
    result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def build(root: Path, target: str, output: Path) -> dict:
    root, output = root.resolve(), output.expanduser().absolute()
    if output.suffix != ".zip":
        raise ValueError("Output must be a review ZIP, not an installation directory.")
    if output.exists() or output.is_symlink():
        raise ValueError("Refusing to overwrite an existing output.")
    if output.resolve().is_relative_to(root / "skills"):
        raise ValueError("Do not write generated bundles into runtime skills.")
    profile = profile_for(root, target)
    files, versions = payload(root)
    hashes = {name: digest(data) for name, data in sorted(files.items())}
    manifest = {"schema_version": 1, "target": target, "profile": profile,
                "library_head_sha": git_head(root), "library_release": None,
                "source_state": "local-content-not-a-release", "skill_versions": versions,
                "file_sha256": hashes, "payload_sha256": digest(canonical(hashes)),
                "profile_sha256": digest(canonical(profile)), "behavioral_status": "not_tested"}
    record = {"schema_version": 1, "target": target, "surface": None, "app_version": None,
              "model": None, "tested_at": None, "payload_sha256": manifest["payload_sha256"],
              "profile_sha256": manifest["profile_sha256"], "library_head_sha": manifest["library_head_sha"],
              "library_release": None, "requested_mode": "ask", "installation_method": None,
              "tool_catalog_status": "unknown", "exposed_tools": [], "documentation_mcp": "unknown",
              "checks": {key: {"status": "not_run", "evidence": None} for key in CHECKS},
              "limitations": [], "reviewer": None}
    exported = {}
    if profile["layout"] == "individual-zips":
        for name in sorted(versions):
            nested = {p.removeprefix("skills/"): data for p, data in files.items() if p.startswith(f"skills/{name}/")}
            exported[f"skill-zips/{name}.zip"] = archive(nested)
    else:
        exported.update({f"{profile['skills_prefix']}/{p.removeprefix('skills/')}": data for p, data in files.items()})
    exported["bundle-manifest.json"] = json.dumps(manifest, indent=2).encode()
    exported["session-record.json"] = json.dumps(record, indent=2).encode()
    exported["START-HERE.md"] = (
        f"# {target}: local compatibility review\n\n{profile['invocation']}\n\n{profile['notes']}\n\n"
        "This archive does not install or launch anything. Use a disposable test context,\n"
        "not your normal project or global skill folders. Native loading can expose\n"
        "skills to every session using that project/account; extraction is NOT isolation.\n"
        "Disable unrelated skills/plugins/sync or use a separate OS account/container\n"
        "where available. Verify actual loaded paths and tool scopes before testing.\n\n"
        "For individual-zips, upload each inner ZIP separately; the outer ZIP is not\n"
        "one native skill. Enable the entire advisor library, then verify cross-skill\n"
        "resolution. Native upload compatibility is not yet behaviorally verified.\n\n"
        "Inspect the entry skill, linked contract, and required references. Record\n"
        "app version, model, surface, exposed capabilities, and check evidence in\n"
        "session-record.json. Keep transcripts sanitized and outside runtime skills.\n"
        "The compatibility test procedure lives in docs/harness-compatibility.md\n"
        "in the source checkout. No evaluator expectations are in the skill payload.\n"
    ).encode()
    # Exclusive creation protects existing deliveries; no extraction or installer runs.
    with output.open("xb") as destination:
        destination.write(archive(exported))
    return manifest


def inspect_record(record: dict, manifest: dict) -> dict:
    """Validate review completeness only. A human-authored pass is not proof."""
    findings = []
    if digest(canonical(manifest["file_sha256"])) != manifest.get("payload_sha256"):
        findings.append("Manifest payload hash does not match its file inventory.")
    if digest(canonical(manifest["profile"])) != manifest.get("profile_sha256"):
        findings.append("Manifest profile hash does not match its profile.")
    for key in ("payload_sha256", "profile_sha256", "target", "library_head_sha"):
        if record.get(key) != manifest.get(key):
            findings.append(f"Record does not match bundle {key}.")
    if record.get("schema_version") != 1:
        findings.append("Unsupported session record schema.")
    for key in ("surface", "app_version", "model", "tested_at", "installation_method", "reviewer"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            findings.append(f"Record the actual {key}.")
    if record.get("surface") not in manifest["profile"]["surfaces"]:
        findings.append("Surface is not covered by this profile; review it separately.")
    timestamp = record.get("tested_at")
    try:
        if not isinstance(timestamp, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", timestamp):
            raise ValueError("Invalid timestamp")
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        findings.append("tested_at must be a real RFC 3339 timestamp with timezone.")
    if record.get("requested_mode") not in {"ask", "assess", "act"}:
        findings.append("Record a recognized requested_mode.")
    if record.get("tool_catalog_status") not in {"exposed", "unavailable"}:
        findings.append("Record whether the current session exposes a tool catalog.")
    if record.get("documentation_mcp") not in {"connected", "not_connected", "unavailable"}:
        findings.append("Record actual documentation MCP availability; do not probe orgs.")
    tools = record.get("exposed_tools")
    if not isinstance(tools, list) or not all(isinstance(t, str) and t.strip() for t in tools):
        findings.append("exposed_tools must list observed tool names, without credentials.")
    if record.get("documentation_mcp") == "connected" and (not tools or record.get("tool_catalog_status") != "exposed"):
        findings.append("Connected MCP requires exposed tool names as evidence.")
    for key in CHECKS:
        check = record.get("checks", {}).get(key, {})
        if check.get("status") != "pass" or not isinstance(check.get("evidence"), str) or not check["evidence"].strip():
            findings.append(f"{key}: supply observed passing evidence or keep compatibility incomplete.")
    return {"status": "review_required" if findings else "reported_pass",
            "verification": "self-reported; not independent harness certification",
            "findings": findings, "payload_sha256": manifest["payload_sha256"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    export = sub.add_parser("bundle")
    export.add_argument("--target", required=True, choices=[p["id"] for p in json.loads((ROOT / "adapters/profiles.json").read_text())["profiles"]])
    export.add_argument("--output", required=True, type=Path)
    review = sub.add_parser("check-record")
    review.add_argument("--record", required=True, type=Path)
    review.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.operation == "bundle":
            manifest = build(ROOT, args.target, args.output)
            print(json.dumps({"output": str(args.output), "target": args.target, "skill_count": len(manifest["skill_versions"]), "payload_sha256": manifest["payload_sha256"], "behavioral_status": "not_tested"}, indent=2))
            return 0
        report = inspect_record(json.loads(args.record.read_text()), json.loads(args.manifest.read_text()))
        print(json.dumps(report, indent=2))
        return 0 if report["status"] == "reported_pass" else 1
    except (OSError, ValueError, KeyError, StopIteration, TypeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
