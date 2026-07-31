# Harness setup

Read only the section for the active harness.

## Codex

- Prefer a declared MCP dependency in `agents/openai.yaml` when Salesforce
  publishes a verified documentation MCP URL or marketplace identity.
- If Codex offers a missing-dependency installation prompt, show the identity
  and ask the customer before accepting it.
- Store project-scoped MCP configuration in `.codex/config.toml` only in a
  trusted project. Do not edit user-global configuration without separate
  approval.
- Use native web search restricted to the policy's exact domains for web
  fallback. Do not use shell fetches to bypass the host network policy.

## Claude Code

- A project may provide `.mcp.json`, but Claude Code must ask the customer to
  approve a project-scoped MCP server before using it.
- Add exact `WebFetch(domain:...)` entries to
  `.claude/settings.local.json` only after project-level approval.
- Do not use `--dangerously-skip-permissions`.

## Cursor and other harnesses

- Use the harness's native MCP and domain-permission flow.
- Require the same server identity and exact-domain review.
- If durable approval is unsupported, keep prompting at the host boundary or
  use MCP only. Do not claim that advisor consent changed host policy.

## Verified-installation requirement

A Salesforce Docs MCP installation candidate must include:

- stable server or marketplace identity;
- streamable HTTP URL or exact local command;
- publisher and source;
- authentication requirements;
- expected read-only documentation tools.

Until Salesforce publishes or administrators provide that metadata, recommend
the managed catalog/admin route and use approved web fallback. Salesforce
Hosted MCP org/data servers are not documentation MCP substitutes.
