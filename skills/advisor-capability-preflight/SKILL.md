---
name: advisor-capability-preflight
description: Check and configure documentation capabilities before an OEM/ISV Advisor interaction. Use when the advisor starts, when Salesforce Docs MCP or official-documentation access may be missing, when a customer asks to install or approve documentation tools, or when the active harness changes.
---

# Advisor capability preflight

Establish documentation capability without touching a Salesforce org. Keep this
setup separate from the partner's advisory decision.

## Preflight

1. Read `references/documentation-policy.json`.
2. Inspect only the tools exposed by the current harness. Do not probe an org,
   Salesforce CLI, credentials, or unrelated MCP servers.
3. Treat Salesforce Docs MCP as connected only when an exposed tool name matches
   the policy patterns. Never infer connection from a file, product name, or
   remembered installation.
4. Read `.advisor/capabilities.json` when it exists. Treat it as the customer's
   recorded preference, not proof that the harness granted access.
5. If MCP is missing, offer exactly these choices:
   - install or connect Salesforce Docs MCP when the harness exposes a verified
     installation candidate;
   - continue with approved official Salesforce web documentation;
   - continue without external documentation.
6. Before installation, show the server identity, transport, URL or marketplace
   source, requested permissions, and whether authentication is required. Ask
   for explicit approval. One approval covers only that verified identity.
7. If no verified installation source is available, say so. Recommend the
   Salesforce-managed marketplace or workspace-admin route; do not invent an
   endpoint and do not substitute an org/data MCP.
8. Ask once whether the exact documentation domains in the policy may be used
   read-only for this project. After approval, request the harness's durable
   project permission. Host or enterprise policy always wins.
9. Record an approved or declined choice only after the customer answers. Run
   `scripts/record_preference.py` to save the decision without secrets.
10. Continue in degraded mode when the customer declines or configuration is
    blocked. Label unsupported current claims as unknown.

Run `scripts/check_preflight.py --harness <active-harness>` when deterministic
status output is useful. Pass each known exposed tool as `--tool <name>`; do not
run the script without identifying the harness.
Read `references/harness-setup.md` only for the active harness.

## Source order

1. Practitioner knowledge supplied by the owning advisor skill.
2. Connected Salesforce Docs MCP.
3. Machine-readable content on an approved official domain.
4. Public HTML on an approved official domain.
5. Unknown with the missing source identified.

Documentation may corroborate or conflict with practitioner knowledge; silence
does not invalidate explicitly labeled practitioner knowledge.

## Output

Return a compact capability receipt containing:

- harness;
- Salesforce Docs MCP status: `connected`, `not_connected`, or `unavailable`;
- approved-web status;
- consent still required;
- configuration action performed or blocked;
- fallback mode;
- evidence labels and exact source identities.

Do not repeatedly display the receipt after readiness is established unless the
harness, policy version, MCP identity, or customer preference changes.
