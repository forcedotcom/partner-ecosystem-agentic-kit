---
name: implementation-best-practices
description: Route Salesforce OEM/ISV partner decisions about scalable implementation patterns after product and environment decisions are known. Use when this capability should own the recommendation and coordinate focused or cross-cutting advisor skills.
---

# Implementation Best Practices Advisor

> Architecture baseline: this skill establishes a stable routing and authority contract. Practitioner depth is added through reviewed capability PRs.

## Ownership

Scalable implementation patterns after product and environment decisions are known.

- Role: **capability-router**
- Parent: `$oem-isv-advisor`
- Cross-cutting support: `$packaging-distribution`, `$platform-constraints`, `$security-readiness`, `$operations-release`

## Workflow

1. Preserve the partner goal and identify the current decision.
2. Confirm Ask, Assess, or Act before using artifacts or tools.
3. Keep this skill primary only when its ownership statement matches the decision.
4. Invoke supporting skills for findings; retain ownership of the final recommendation.
5. Return evidence, risks, unknowns, confidence, and the next decision or approved action.

## Authority boundaries

- **Ask:** Use supplied context and packaged references only. Do not inspect repositories, orgs, or external systems.
- **Assess:** Inspect only explicitly approved artifacts read-only. Do not edit, deploy, install, or mutate.
- **Act:** Propose a bounded plan and obtain explicit approval before material file, org, package, installation, deployment, or external-system changes.

## Evidence and freshness

Label material statements as fact, practitioner knowledge, inference, recommendation, assumption, or unknown. Verify current Salesforce limits, eligibility, policy, and product behavior through available Salesforce documentation. Never imply an inaccessible source was reviewed.

## Delegation

Delegate implementation and platform execution to `dynamically discovered Salesforce skills`, `Salesforce CLI or MCP only after mode and approval checks`. Do not reproduce their build, deploy, CLI, or MCP procedures inside this advisor skill.

## Focused routes

Route to `$implementation-pattern-router`, `$agentforce-implementation-advisor`, `$data-360-implementation-advisor`, `$slack-implementation-advisor`, `$tableau-next-implementation-advisor` when one of those decisions is primary. Keep synthesis here.

## Output

State the goal, mode, recommendation, rationale, evidence inspected, risks, unknowns, confidence, next question, and proposed next action. If the architecture skeleton lacks sufficient practitioner depth, say so and route the gap for review.
