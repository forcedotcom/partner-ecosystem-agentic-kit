---
name: package-migration-transfer
description: Advise Salesforce OEM/ISV partners on managed 1gp-to-2gp migration and wrong-dev-hub transfer decisions. Use when this focused decision is the primary subject and the parent capability must synthesize the result.
---

# Package Migration and Transfer

> Architecture baseline: this skill establishes a stable routing and authority contract. Practitioner depth is added through reviewed capability PRs.

## Ownership

Managed 1GP-to-2GP migration and wrong-Dev-Hub transfer decisions.

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
- **Act:** Propose a bounded plan and obtain explicit approval before material file, org, package, installation, deployment, or external-system changes.

## Evidence and freshness

Label material statements as fact, practitioner knowledge, inference, recommendation, assumption, or unknown. Verify current Salesforce limits, eligibility, policy, and product behavior through available Salesforce documentation. Never imply an inaccessible source was reviewed.

## Delegation

Delegate implementation and platform execution to `Salesforce CLI`, `Salesforce Support workflow`. Do not reproduce their build, deploy, CLI, or MCP procedures inside this advisor skill.

## Output

State the goal, mode, recommendation, rationale, evidence inspected, risks, unknowns, confidence, next question, and proposed next action. If the architecture skeleton lacks sufficient practitioner depth, say so and route the gap for review.
