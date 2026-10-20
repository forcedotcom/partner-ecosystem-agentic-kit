---
name: headless-mcp-advisor
description: Advise Salesforce partners on Headless Toolkit and MCP client/server choices, managed-package boundaries, HXL output, and delivery to Agentforce, Slackbot, Claude, or ChatGPT. Use for architecture decisions or Salesforce DX assessments; route builds to global sf-skills.
---

# Headless MCP Advisor

Enter through `oem-isv-advisor` → `implementation-best-practices`. Own the
Headless and MCP architecture decision; coordinate with `agentforce-implementation-advisor`
for Agentforce behavior, `slack-implementation-advisor` for Slack integration,
and Packaging & Distribution, Platform Constraints, and Security & Readiness
for their respective boundaries. Read `references/decision-guide.md` for the
partner interview, `references/sfdx-assessment.md` when assessing a partner
Salesforce DX project, `references/channel-rollout.md` for Slackbot, Claude,
or ChatGPT delivery, and `references/source-refresh.md` before current platform
or packageability claims. Run `advisor-capability-preflight` first.

## Authority and evidence

- **Ask:** advise from supplied context and packaged references only; label
  facts, practitioner knowledge, inference, recommendation, assumption, and
  unknown. Refresh current claims through the preflight-approved documentation
  path without inspecting an org or repository.
- **Assess:** inspect approved designs, source, metadata, and org evidence
  read-only; report exactly what was inspected and what remains unknown.
- **Act:** present a bounded plan, exact files or org targets, side effects,
  rollback, and validation; obtain explicit approval before material changes
  under this advisor's runtime contract, then delegate execution. Approval to
  install a skill library is separate from approval to change an org.

## Decision workflow

1. Ask where the MCP server runs, who the MCP client is, where the user works,
   and which side initiates each tool call. Use the partner's MCP In/Out labels
   from `references/decision-guide.md`; also name the actual client and server
   to avoid ambiguity. Do not assume every headless integration needs MCP.
2. Distinguish a builder workflow from a runtime integration. Identify the
   engagement layer: Agentforce, Slackbot, Claude, ChatGPT, or another client.
   Check that the specific client, authentication method, and desired output
   format are supported for the chosen server.
3. In Assess, locate `sfdx-project.json`, inspect its package directories, and
   inventory Apex classes, Lightning types, HXL widgets, and MCP server
   definitions. Check `unpackagedMetadata`, `.forceignore`, and source-control
   state. Trace action output through its renderer, widget, and server tool.
   Separate 2GP package candidates from customer-owned setup and source-only
   examples; do not infer deployment from local files.
4. For Salesforce hosted delivery, compare a standard server's existing tools
   with a focused custom server. Choose the smallest tool set that meets the
   persona's job. Inspect existing Apex, Agentforce agents, Flows, Prompt
   Templates, Apex REST, `@AuraEnabled` methods, and API Catalog endpoints
   before proposing new Apex. Treat Apex Actions as a strong option for
   deterministic, multi-step business logic, not a universal default.
5. For a packaged Apex Action, inspect the invocable method's visibility,
   input/output contract, namespace, permissions, and managed-package boundary.
   Do not apply `@JsonAccess` indiscriminately: check the selected Lightning
   type or serialization path and its current requirements. Distinguish the
   packageable action from subscriber-owned server configuration.
6. If rich output is required, select the HXL path for the actual surface and
   tool output. Confirm widget bundle, schema, Lightning type, and MCP server
   resource wiring before proposing deployment. HXL is optional and currently
   documented as Beta; a working tool can return ordinary structured output.
7. Plan each supported engagement layer's connection, permissions, and test
   separately. Reuse the same eligible server-side logic and widget where the
   channel supports them; never equate one build with automatic client access.
8. Return a recommendation, alternatives, the client/server data-flow map,
   SFDX inventory and package boundary when assessed, customer setup
   ownership, evidence ledger, unknowns, and the exact global skill handoff.

## Execution handoff

Use the installed, global `forcedotcom/sf-skills` source of truth. Do not copy
its build instructions or create project-local copies.

- Apex implementation: `platform-apex-generate`; Apex test authoring:
  `platform-apex-test-generate`.
- Standalone HXL widget: `platform-widget-generate`.
- Apex-invocable-backed MCP tool output rendered as a widget:
  `platform-mcp-tool-widget-coordinate`.
- Apex-backed Agentforce action output with a custom Lightning type and widget:
  `platform-lightning-type-widget-coordinate`.

These skills have different triggers and validation gates. Discover the current
installed skill instructions at handoff, and pass the selected server, action,
output schema, target client, package namespace, project API version, and
approval scope. Check the selected skill's current minimum API version before
handoff. Never use an org/data MCP as a substitute for Salesforce documentation.
