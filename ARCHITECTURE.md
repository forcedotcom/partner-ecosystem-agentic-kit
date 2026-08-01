# OEM/ISV Advisor architecture

This repository is the partner-facing skill library. Its baseline defines the
whole advisor before individual skills gain practitioner depth, so every skill
pull request has a stable place, owner, and routing relationship.

## Baseline contract

The baseline contains **26 skill folders**:

- 2 foundation skills: entry routing and documentation/tool preflight.
- 7 capability routers: one for each stage of the partner journey.
- 17 focused advisors currently assigned to Capabilities 2, 3, and 4.

A skeleton is not a production-readiness claim. It establishes the stable skill
ID, triggering boundary, capability ownership, supported modes, evidence rules,
and execution delegation. Detailed references and tested procedures arrive in
focused draft pull requests.

## Capability map

| # | Capability router | Decision ownership | Focused skills |
|---|---|---|---:|
| 1 | `solution-discovery` | Product fit, target user, product boundary, Salesforce fit, and viable direction | 0 |
| 2 | `packaging-distribution` | Packaging, package lifecycle, upgrades, listings, and distribution | 7 |
| 3 | `development-environment` | Development, test, demo, trial, customer-test, and packaging environments | 5 |
| 4 | `implementation-best-practices` | Scalable implementation patterns after product and environment decisions | 5 |
| 5 | `platform-constraints` | Limits, metadata support, guardrails, capability gaps, and workarounds | 0 |
| 6 | `security-readiness` | Secure architecture, review preparation, evidence, and remediation readiness | 0 |
| 7 | `operations-release` | Testing, CI/CD, release, rollback, monitoring, support, and lifecycle operations | 0 |

## Complete skill inventory

### Foundation

- `oem-isv-advisor` — partner goal owner and entry router.
- `advisor-capability-preflight` — documentation, source, and tool preflight.

### Capability 1 — Solution Discovery

- `solution-discovery` — capability router.

### Capability 2 — Packaging and Distribution

- `packaging-distribution` — capability router.
- `packaging-strategy`
- `packageability-assessment`
- `managed-2gp-foundation`
- `package-version-validation`
- `package-ancestry-dependencies`
- `package-release-promotion`
- `package-migration-transfer`

### Capability 3 — Development Environment

- `development-environment` — capability router.
- `pbo-dev-hub-foundation`
- `namespace-access-governance`
- `scratch-org-shape`
- `environment-portfolio`
- `org-provisioning-diagnostics`

### Capability 4 — Implementation Best Practices

- `implementation-best-practices` — capability router.
- `implementation-pattern-router`
- `agentforce-implementation-advisor`
- `data-360-implementation-advisor`
- `slack-implementation-advisor`
- `tableau-next-implementation-advisor`

### Capability 5 — Platform Constraints

- `platform-constraints` — capability router.

### Capability 6 — Security and Readiness

- `security-readiness` — capability router.

### Capability 7 — Operations and Release

- `operations-release` — capability router.

The machine-readable ownership, modes, dependencies, maturity, and primary or
supporting relationships live in
`skills/oem-isv-advisor/references/capability-catalog.json`.

## Pull-request layering

1. The architecture-baseline PR owns the complete skeleton and foundation.
2. Capability-router PRs deepen the seven parent routers against that baseline.
3. Focused-skill PRs deepen one coherent capability without redefining other
   capabilities.
4. Testing evidence remains attached to the exact skill snapshot used by the
   harness.
5. A draft PR may iterate, but only normal human review can merge it.

Adding a skill outside this map requires an architecture change first. Improving
an existing skill should modify its stable folder and update its catalog entry
only when ownership, dependencies, modes, or maturity changed.

## Runtime rules

- Route by the partner decision, not by document title or product keyword.
- The primary skill owns the final recommendation and includes supporting
  findings.
- Ask is context-only; Assess is read-only inspection; Act requires a bounded
  plan and explicit approval before material changes.
- Label evidence and uncertainty. Never claim an inaccessible source was
  reviewed or state current limits and policy from memory.
- Delegate build, deploy, Salesforce CLI, and MCP execution to approved tool
  libraries rather than reproducing them in advisory skills.
