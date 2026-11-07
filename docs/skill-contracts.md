# Advisor skill contracts

Every skill declares a portable scalar metadata header in `SKILL.md` and links
to `references/skill-contract.json` in its instructions. Contract schema 1.0.0
describes identity, role, home capability, bounded decision ownership, modes,
conditional relationships/dependencies, evidence pointers, output, and declared
maturity. It grants no runtime permissions and contains no evaluator answers.

The schema is at
`skills/isv-partner-advisor/references/skill-contract.schema.json`. The portable
checker is `skills/isv-partner-advisor/scripts/check_skill_contracts.py`.

## Maintain the library

1. Edit the owning skill's contract and the relevant instructions together.
2. Keep header identity, role, capability, and schema version consistent.
3. Regenerate the catalog:
   `python3 skills/isv-partner-advisor/scripts/check_skill_contracts.py . --write-catalog`
4. Verify without writing:
   `python3 skills/isv-partner-advisor/scripts/check_skill_contracts.py .`
5. Run `python3 -m unittest discover -s tests -v`.

The generated catalog is an index, not a second author-maintained contract.
The checker reports malformed metadata, unsafe paths, missing required internal
advisors, inconsistent authority, nonexistent routes, routing-section drift,
and index drift. It does
not execute candidate scripts or connect tools to discover dependencies.

## Interpret relationships and authority

The home capability is structural. Being primary or supporting depends on the
active decision. A consultation and return is not by itself an invocation loop.
The primary retains synthesis unless the decision is explicitly handed off.

Required internal dependencies must be available for complete library validation,
not as an unconditional Ask gate. Ask dependencies are conditional/optional;
required dependencies are scoped to Assess/Act. Conditional advisors need not
be invoked in every scenario. External tools/libraries are discovered only when
the selected operation needs them; absence preserves an honest fallback or a
not-run result. Documentation providers are not execution libraries. No blanket
CLI, org, or API-version prerequisite is imposed on Ask.

Catalog entries use stable IDs only, never cross-skill contract paths. The
router reads owns/modes/maturity in the catalog, invokes the selected skill
through the host catalog (with namespace when needed), then that skill reads
its own local references. Contract reads are targeted, not every-turn overhead.
Explicit IDs in introductions/routing/workflow are checked against relationships
or internal dependencies; exclusions and examples are not inferred as handoffs.
Every declared `routes_to` target must also be explicitly documented in the body.

Ask advises without project/org inspection. Assess inspects only approved
evidence. Act orchestration requires a bounded plan and explicit approval;
execution can be delegated. Preflight's Act scope is documentation configuration
only. Installation/connection approval does not authorize deployment or data
changes. Host and enterprise permissions always take precedence.

## Evidence and versions

The output contract `advisor-readout-v1` means the goal, recommendation,
rationale, evidence with source/status labels, risks, unknowns, and next action
with approval needs. Specialist extensions apply only when consequential.

Evidence references retain practitioner policy, claim provenance, applicability,
source refresh, exceptions, and supersession. A contract's declared maturity is
not proof of testing. Actual validation binds the skill content, tested commit,
scenario, harness, and human decision separately. Never embed test expectations,
raw private transcripts, credentials, org aliases, or customer paths here.

### Version tracking

Each `SKILL.md` header declares `metadata.version` as a quoted SemVer string.
The initial tracked baseline is `1.0.0` for each existing skill; this introduces
version tracking, not invented historical releases or proof of validation.
The generated catalog records each skill's version from that single source.
PEAK preserves it with the contract in snapshot evidence alongside the exact
tested Git revision. It never substitutes a version label for a content hash.

Follow [Semantic Versioning](https://semver.org/): patch for compatible fixes,
minor for compatible new behavior, major for incompatible changes. A skill's
public contract is its supported decisions, modes, inputs, outputs, and handoff
boundaries. Include durable reference/knowledge changes when deciding the bump.
During development, keep the intended next version; once published, never change
the contents of that version. Bump only changed skills, not every skill in a
library release. Regenerate the catalog after changing versions.

The library release is a separately approved repository Git tag/GitHub release
that identifies the collection at an exact commit. Do not duplicate the library
release number into every skill or create a release just by editing headers.
`metadata.contract-schema` versions the declaration format independently of both.
Missing individual versions on older contracts produce a warning, not a broken
legacy import; declared invalid versions block contract validation.

Schema version, skill version, library release version, and tested Git revision
are distinct. Do not invent platform minimums from unrelated tools.
Maintainers are marked unassigned where this repository has not established an
accountable identity. Assign them through normal human review; do not infer
ownership from an example or test author.

## Add a skill or contribute knowledge

A new skill needs a stable name, one existing home capability, bounded owned and
excluded decisions, explicit mode behavior, and a contract. Adding a capability
outside the seven requires an architecture decision. An observation or corrected
rule normally updates the existing owner's references and evidence rather than
creating a new skill. Preserve existing evidence provenance and rerun affected
decisions; do not label a whole skill validated because one pattern was reviewed.
