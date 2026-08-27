# Agent Script package-boundary guidance

Use this focused practitioner guidance when deciding whether and what to package
for an Agentforce solution authored with Agent Script.

## Ownership of the decision

`packaging-strategy` owns package-boundary framing: which assets belong in the
managed 2GP package and which require a delivery pattern outside the native
metadata boundary. `packaging-distribution` owns the final cross-skill
distribution and lifecycle synthesis. `agentforce-implementation-advisor`
supports post-install creation/import, dependency binding, validation, and
activation.

## Boundary rules

- **Practitioner knowledge:** Do not claim authored Agent Script is natively
  packageable unless a current source and an exact package-version test prove it.
- **Practitioner knowledge:** An unsupported script artifact does not make the
  whole solution undistributable. Package the supported application foundation
  and carry the script separately for post-install ingestion.
- **Recommendation:** Inventory every referenced action, topic, prompt template,
  Apex class, flow, and data asset. Include only package-owned dependencies with
  current packageability proof. Exclude subscriber-owned and external resources
  by default.
- **Recommendation:** Keep carrier selection conditional on script count,
  format, size, setup experience, retrieval behavior, and upgrade lifecycle.
  Validate the exact choice in a clean target org.

## Partner-facing outcome

Explain the packageable foundation, the unpackageable or unproven boundary, the
candidate carrier, the subscriber setup step, and the evidence still required.
Do not stop at “Agent Script is not packageable,” and do not let package-boundary
framing override the final distribution owner.
