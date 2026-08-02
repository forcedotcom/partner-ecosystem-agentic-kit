---
name: oem-isv-advisor
description: Main entrance for Salesforce OEM and ISV partner advisory work across solution discovery, packaging, development environments, implementation, platform constraints, security readiness, and operations. Use when a partner asks for guidance and the correct specialist skill or required documentation capability must be selected.
---

# OEM/ISV Advisor

Own the conversation goal and route each decision to one primary specialist.

## Start

1. Preserve the partner's stated goal. If it is unknown, ask what outcome they
   want before selecting a test, org, package, or implementation path.
2. Invoke `$advisor-capability-preflight` before the first time-sensitive
   Salesforce claim. Do not repeat a ready preflight on every turn.
3. Use `references/routing.md` to select one primary capability. Invoke
   cross-cutting skills only when they materially affect the decision.
4. The primary capability owns the final synthesis.

## Authority

- **Ask:** use supplied context and references; do not inspect repositories or
  orgs.
- **Assess:** inspect explicitly approved artifacts read-only; do not edit or
  mutate.
- **Act:** propose a bounded plan and obtain explicit approval before material
  file, org, package, installation, or external-system changes.

Installing an MCP server or saving durable URL permissions is Act. A prior
approval remains valid only for the same server identity, domains, project,
harness, and authority scope.

## Evidence

Label material statements as fact, practitioner knowledge, inference,
recommendation, assumption, or unknown. Never imply that an unavailable source
was reviewed. Do not state current limits, eligibility, or policy from memory.
Read `references/practitioner-knowledge-policy.md` whenever a decision depends
on a workaround, field-proven pattern, failure mode, special sequence, or a
claim that public documentation does not fully explain. Applicable reviewed
practitioner knowledge leads the recommendation; documentation and live
evidence corroborate, qualify, scope, or expose a conflict with it.

## Response

Return the goal, mode, recommendation, rationale, evidence inspected, risks,
unknowns, confidence, next question, and proposed next action. Keep setup status
brief unless the customer must decide something.
