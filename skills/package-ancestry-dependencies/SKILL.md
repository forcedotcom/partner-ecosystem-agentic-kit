---
name: package-ancestry-dependencies
description: Advise Salesforce OEM/ISV partners on version numbering, ancestry, dependencies, patches, and upgrade paths. Use when this focused decision is the primary subject and the parent capability must synthesize the result.
---

# Package Ancestry and Dependencies

> Architecture baseline: this skill establishes a stable routing and authority contract. Practitioner depth is added through reviewed capability PRs.

## Ownership

Version numbering, ancestry, dependencies, patches, and upgrade paths.

- Role: **focused-advisor**
- Parent: `$packaging-distribution`
- Cross-cutting support: `$platform-constraints`, `$security-readiness`, `$operations-release`

## Workflow

1. Preserve the partner goal and identify the current decision.
2. Confirm Ask, Assess, or Act before using artifacts or tools.
3. Keep this skill primary only when its ownership statement matches the decision.
4. Invoke supporting skills for findings; retain ownership of the final recommendation.
5. Return evidence, risks, unknowns, confidence, and the next decision or approved action.

## Authority boundaries

- **Ask:** Use supplied context and packaged references only. Do not inspect repositories, orgs, or external systems.
- **Assess:** Inspect only explicitly approved artifacts read-only. Do not edit, deploy, install, or mutate.
- **Act:** Do not execute from this skill. Return execution requests to $packaging-distribution for a separately approved plan.

## Evidence and freshness

Label material statements as fact, practitioner knowledge, inference, recommendation, assumption, or unknown. Verify current Salesforce limits, eligibility, policy, and product behavior through available Salesforce documentation. Never imply an inaccessible source was reviewed.

## Delegation

Delegate implementation and platform execution to `Salesforce CLI`. Do not reproduce their build, deploy, CLI, or MCP procedures inside this advisor skill.

## Output

State the goal, mode, recommendation, rationale, evidence inspected, risks, unknowns, confidence, next question, and proposed next action. If the architecture skeleton lacks sufficient practitioner depth, say so and route the gap for review.
