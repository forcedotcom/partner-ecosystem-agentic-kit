# Security Review Readiness design

## Intent

Mature `security-readiness` into the single owner of a stage-gated
AgentExchange Security Review interview, including requests that use the
AppExchange name. The lifecycle covers managed packages, Salesforce API
solutions, and connected integrations and returns a portable readiness dossier.
It does not certify approval or submit anything implicitly.

## Design

PEAK's lifecycle has seven gates: documentation preflight; scope, eligibility,
and listing readiness; follow-the-data trust boundaries; architecture-specific
materials and evidence; remediation and retest; submission readiness; reviewer
response and release handoff. Each gate is `ready`, `blocked`,
`not-applicable`, or `unknown`. They map to, but remain distinct from,
Salesforce's five stages of submission, verification, queueing, testing, and
results.

`security-readiness` owns interview progression, dossier synthesis, and the
submission-readiness decision. Packaging, PBO, package version, ancestry,
promotion, access governance, implementation, platform, and operations skills
provide only evidence in their respective domains. Product-specific Agentforce,
Data 360, Slack, and Tableau security checklists remain out of scope.

## Evidence and authority

The dossier records the exact package candidate, gate ledger, evidence
identity/freshness, trust boundaries, findings and dispositions, owners,
blockers, policy unknowns, and next approval-gated action. Its materials matrix
varies by native package, external service, API-only, mobile, extension-package,
and Marketing Cloud scope. It retains report identities and secure credential
delivery status, never credential values. Current claims use Salesforce Docs
MCP first and the approved official-web fallback second; inaccessible Partner
Community content is `unknown`.

Code Analyzer, Checkmarx, DAST, and manual testing remain distinct evidence
types. Installed sf-skills may execute Code Analyzer work, but Security &
Readiness retains the current rule-selector, output, source/package alignment,
and dossier contract.

The Partner Console wizard is part of the lifecycle, not merely a submission
button. The skill distinguishes draft, submitted, Returned verification, queue,
testing, result, false-positive-only resubmission, and expired states. It
records the state-specific action without treating a Returned submission as a
failed review or an expired approval as a code finding.

False-positive evidence is per finding: location, security explanation, and
supporting evidence. It remains distinct from remediation. A managed-package
code fix creates a successor candidate handoff with new version, release, test,
and scan evidence; evidence for the failed candidate cannot establish the
successor's readiness.

Ask gathers supplied context only. Assess reads explicitly approved evidence.
Act requires a bounded plan and explicit approval before remediation,
configuration, analyzer changes, or submission.

## Validation

Contract scenarios cover an eligible package, a blocked PBO/package path,
inherited listing readiness, API-only and package-plus-external architectures,
false-positive/retest, required scanner combinations, portal escalation, a
not-approved result, and unavailable current policy. Tests verify lifecycle
coverage, evidence handoffs, authority boundaries, and the non-certification
rule.

## Implemented refinements

The completed design adds an evidence-first Assess path: with bounded read-only
authorization, inspect supplied SFDX source, package metadata, org facts, and
scan reports before asking the partner for only intent, ownership, runtime, or
configuration facts that evidence cannot establish.

For Agentforce, the dossier records safe per-action and per-prompt control
evidence, while partner source, prompt text, configuration values, and customer
data remain in partner-controlled locations. The partner supplies an
architecture-specific reviewer test route and post-install/customer setup
guidance; PEAK does not prescribe a universal setup or execute it in Assess.

The Gate 5 ledger includes a bounded reassessment path. A partner can supply a
successor candidate, changed evidence, fix rationale, and retest evidence. A
source-only review is `fixed-awaiting-retest`; `fixed-verified` requires
candidate-aligned configured-route evidence. Every reassessment records its
unreviewed boundary and never constitutes whole-solution recertification.

Synthetic tests now exercise these evidence-first, Agentforce, reassessment,
and end-to-end lifecycle decisions without using partner artifacts. Current
policy claims use a capability receipt and a dated official-web refresh record.
