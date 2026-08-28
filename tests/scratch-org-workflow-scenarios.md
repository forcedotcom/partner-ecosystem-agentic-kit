# Scratch Org Workflow Scenarios

These scenarios are review artifacts for the scratch-org guidance journey.
They define expected advisory behavior; they do not authorize a repository or
org mutation.

## Scenario 1 — Minimal build-ready definition

**Partner context:** An ISV needs a reproducible daily-development scratch org
and package-build shape. It provides its target edition, source requirements,
and package context but no approved repository or org access.

**Expected outcome:** `scratch-org-shape` remains the primary advisor. It
collects the development purpose, edition, package/build context, required
capabilities, and constraints; returns a minimal proposed JSON structure and
capability-to-feature/setting mapping; labels unverified current catalog values
as unknown; and explains that the result addresses package-build readiness, not
subscriber/customer-compatibility testing.

## Scenario 2 — Feature and companion-setting dependency

**Partner context:** An approved repository assessment shows metadata that
requires a capability whose current documentation specifies both a scratch-org
feature and a companion setting.

**Expected outcome:** `scratch-org-shape` inspects the approved definition,
`sfdx-project.json`, package-directory configuration, and relevant metadata.
It identifies the effective build definition, refreshes the current source
before naming values, maps the capability to the feature and setting, and
proposes only the minimal documented addition. It does not claim that a valid
feature name bypasses a missing entitlement.

## Scenario 3 — Misleading existing definition

**Partner context:** A package build fails although developers can deploy to a
richer, manually configured org. The repository contains multiple definitions,
a package-directory `definitionFile`, and an optional CLI override.

**Expected outcome:** `scratch-org-shape` identifies the effective build
definition before recommending a change. It flags over-provisioning and manual
configuration as risks, preserves the separation between build readiness and
customer compatibility, and returns a proposed patch only after labeling its
evidence and unknowns. If approved evidence instead shows a provisioning,
entitlement, capacity, expiration, or cleanup failure, it hands off to
`org-provisioning-diagnostics`.

## Approval-gated manual smoke test

After a partner approves a bounded Act plan, run this only against a
non-production Dev Hub:

1. Create a scratch org from the proposed definition.
2. Deploy or install the relevant source and run the relevant tests.
3. Record the result as execution evidence for the partner; do not treat the
   submission as success before terminal validation.
4. Delete the test org and recreate it from the same definition to confirm
   reproducibility.

Do not commit credentials, aliases, org IDs, or live results.
