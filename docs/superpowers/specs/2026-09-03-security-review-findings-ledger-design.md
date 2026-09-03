# Security Review findings ledger design

## Intent

Strengthen Gate 5, remediation and retest, without adding a top-level skill or
changing the 26-skill catalog. `security-readiness` remains the sole lifecycle
owner: it guides a partner to evidence-backed submission readiness but never
certifies or predicts Salesforce Security Review approval.

PEAK distributes only guidance and synthetic decision tests. Partner source,
scan reports, org/package identifiers, credentials, code locations, and
remediation records remain in the partner's local project and approved storage.

## Two-layer ledger

The detailed ledger is partner-controlled and access-restricted. Its finding
record contains the report or scanner identity, exact candidate, source scope,
source classification, affected trust boundary, reported severity, owner,
disposition, secure evidence location, and next evidence. It adds remediation
change and successor-candidate evidence when applicable; false-positive
location, rationale, and support; and matching-candidate retest scope, result,
and date.

The portable dossier keeps only a safe summary: candidate, finding class,
reported severity, source classification, owner, disposition, coverage status,
next action, and secure ledger location. It never copies report excerpts, code
locations, endpoints, credentials, customer data, or exploit detail.

Finding dispositions are `open`, `remediating`, `fixed-awaiting-retest`,
`fixed-verified`, `false-positive`, and `not-applicable`. Evidence coverage is
independent: `complete`, `partial`, `unavailable`, or `not-applicable`. A
selected scanner-engine error is a coverage record, not a vulnerability
finding. Vendored or minified code is source-classified and remains in scope;
it is not silently discarded as first-party remediation work.

## Gate decision

Gate 5 is `ready` only when applicable evidence coverage is complete or has a
documented non-applicability rationale; no finding is open, remediating, or
awaiting retest; verified fixes have matching-candidate retest evidence; and
false-positive records are complete. It is `blocked` for known incomplete
required coverage, unresolved material findings, failed retests, or managed
package remediation without successor-candidate evidence. It is `unknown` when
scope, owner, candidate alignment, applicability, or evidence cannot be
verified.

A changed candidate or trust boundary, failed retest, or reviewer challenge
reopens the affected record. A reported vulnerability class requires inspection
of all in-scope instances, not only the reported location.

## Implementation and validation

Add a `finding-ledger.md` reference and link it from `security-readiness`.
Update lifecycle, dossier, scanner, failed-report, packageability, package
version, promotion, and operations handoffs to use the same contract.

Add product-neutral synthetic scenarios for first-party findings, vendor
dependencies, selected-engine failure, managed-package successor candidates,
false positives, and a complete resolved ledger. Tests must assert that no
fixture contains partner evidence or product-specific identifiers.
