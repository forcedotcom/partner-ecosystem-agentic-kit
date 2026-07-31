#!/usr/bin/env python3
"""Evaluate advisor documentation readiness without probing external systems."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_POLICY = HERE.parent / "references" / "documentation-policy.json"


def load_json(path: Path, default: dict | None = None) -> dict:
    if not path.exists():
        return {} if default is None else default
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def evaluate(
    policy: dict,
    harness: str,
    tools: list[str],
    preferences: dict,
    runtime_candidates: list[dict] | None = None,
) -> dict:
    mcp = policy["salesforce_docs_mcp"]
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in mcp["tool_name_patterns"]]
    matching_tools = sorted({tool for tool in tools if any(p.search(tool) for p in patterns)})
    mcp_status = "connected" if matching_tools else ("not_connected" if tools else "unavailable")
    declared_candidates = list(mcp.get("install_candidates", [])) + list(runtime_candidates or [])
    candidates = [
        candidate
        for candidate in declared_candidates
        if candidate.get("verified") is True
        and harness in candidate.get("harnesses", [])
        and candidate.get("publisher")
        and candidate.get("source")
        and (candidate.get("url") or candidate.get("marketplace_identity"))
    ]
    docs_choice = preferences.get("approved_documentation_domains")
    mcp_choice = preferences.get("salesforce_docs_mcp_install")
    needs = []
    if mcp_status != "connected" and mcp_choice not in {"declined", "deferred"}:
        needs.append("mcp_install_consent" if candidates else "mcp_install_source")
    if docs_choice not in {"approved", "declined"}:
        needs.append("documentation_domain_consent")

    if mcp_status == "connected":
        fallback = "salesforce_docs_mcp"
    elif docs_choice == "approved":
        fallback = "approved_official_web"
    else:
        fallback = "packaged_knowledge_only"

    return {
        "schema_version": 1,
        "harness": harness,
        "salesforce_docs_mcp": {
            "status": mcp_status,
            "matching_tools": matching_tools,
            "verified_install_candidates": candidates,
        },
        "approved_documentation_domains": docs_choice or "not_decided",
        "consent_required": needs,
        "fallback": fallback,
        "ready": not needs,
        "host_security_override": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness", required=True)
    parser.add_argument("--tool", action="append", default=[])
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--preferences", type=Path)
    parser.add_argument(
        "--install-candidate-json",
        action="append",
        default=[],
        help="Verified candidate metadata surfaced by the active harness",
    )
    args = parser.parse_args()
    policy = load_json(args.policy)
    preferences = load_json(args.preferences) if args.preferences else {}
    candidates = [json.loads(value) for value in args.install_candidate_json]
    print(
        json.dumps(
            evaluate(policy, args.harness, args.tool, preferences, candidates),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
