---
name: packaging-strategy
description: Use when a partner asks whether to package, which packaging model to use, where package boundaries belong, or how packaging affects distribution and upgrades. Owns Whether, what, and how to package; managed 2GP, migration, package boundaries, and distribution model.
---

# Packaging Strategy

Own the partner decision described in the frontmatter. Keep the parent
capability concise and route here only when this bounded decision is active.

## Operating contract

- Route by the partner's decision, not by document title or keyword alone.
- Preserve the partner's goal across turns. Ask only questions that materially
  change the recommendation, test target, authority, or next action.
- Label every material statement as fact, practitioner knowledge, inference,
  recommendation, assumption, or unknown.
- Read `references/practitioner-knowledge.md` when the decision needs the
  supplied tribal process, failure modes, or decision rules.
- Read `references/source-refresh.md` before stating time-sensitive Salesforce
  limits, eligibility, packageability, CLI syntax, product enablement, or
  policy.
- Prefer practitioner knowledge first. Use current documentation and live
  evidence to corroborate, qualify, or expose conflict; documentation silence
  does not invalidate an explicitly labeled practitioner rule.
- Read `references/agent-script-package-boundary.md` when an Agent Script
  artifact affects the package boundary.

## Authority modes

- **Ask:** answer from supplied context and loaded references. Do not inspect a
  repository or org and do not execute tools that change state.
- **Assess:** inspect approved project, artifact, documentation, CLI, or org
  evidence read-only. Report exact observations, missing evidence, and risks.
  Do not edit files or mutate an org.
- **Act:** this skill does not own execution. Produce the decision and hand off to the bounded Act owner or approved execution library without granting mutation authority.

## Decision workflow

1. Establish the product, subscriber model, namespace/ownership, upgrade
   control, and distribution evidence; keep any missing decision inputs
   explicit.
2. Choose package versus unpackaged delivery only after those inputs are
   sufficient; a new DX project or source directory does not select a package
   model.
3. Define package boundaries and dependencies from declared configuration and
   supported metadata. Treat direct metadata outside `packageDirectories` as a
   separate, unresolved boundary until its intent is established, except where
   the partner has explicitly identified its purpose.
4. Compare managed 2GP, unlocked, migration, and hybrid choices.
5. Identify distribution, upgrade, and off-platform implications.

## Interview-validated package-boundary rules

Apply these **Practitioner rules** when the partner has supplied the described
intent; otherwise retain the boundary and ownership as unknown.

- In the partner's stated project convention, metadata under the declared
  `force-app` package directory is package content. For managed 2GP, the
  namespaced package surface is partner-controlled; non-namespaced metadata is
  customer-owned.
- A `my-unpackaged-directory` explicitly identified by the partner is
  partner-maintained, non-distribution metadata. Its contents can be
  nonpackageable or test-only; do not add it to the package merely because it
  is present in the repository.
- If that directory is configured as `unpackagedMetadata` for package-version
  creation, confirm that every included item is intentionally installed in the
  build scratch org for testing. Refresh the current documented behavior before
  describing its exact platform effect.
- When the solution uses Named Credentials, separate the package's reusable
  definition from subscriber-specific principals, authentication, and secret
  values. Consult the Named Credentials packaging, population, target-org
  testing, OAuth, and managed-upgrade documentation before recommending what
  belongs in the package or in post-install setup.
- When non-distributed metadata is needed in a customer production org, the
  partner must choose and perform a separate deployment or configuration path.
  Do not default that work to the customer.
- Before a managed 2GP handoff, verify that the intended partner Salesforce
  org is the Dev Hub, the namespace is registered and linked there, and the
  same namespace is recorded in `sfdx-project.json`.

## Execution delegation

Advisory ownership remains here. Delegate implementation to: forcedotcom/sf-skills.
Do not reproduce generic Salesforce build, deploy, or CLI skills. Dynamically
discover approved skill libraries. Ask once before installing a library and
reuse that approval while repository identity, origin, trust, license, and
authority remain unchanged. Never treat installation approval as approval for
an org or repository mutation.

## Cross-cutting checks

Invoke Platform Constraints, Security & Readiness, and Operations & Release
when they materially affect this decision. This skill owns the final synthesis
and must include their findings rather than returning disconnected answers.

## Required output

Return:

1. Partner goal and current decision point.
2. Recommendation and alternatives considered.
3. Evidence ledger with explicit labels and source identity.
4. Unknowns, conflicts, risks, and time-sensitive claims requiring refresh.
5. Questions still required to reach the goal.
6. Proposed next action and whether approval is required.
7. For Assess, artifacts actually inspected and read-only validation performed.
8. For Act, proposed plan, captured approval scope, execution evidence,
   validation, actual changes, and cleanup.

## Boundaries

This skill does not own:

- creating package records
- creating package versions
- promoting versions
