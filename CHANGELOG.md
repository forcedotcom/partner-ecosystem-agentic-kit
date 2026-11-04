# Changelog

## 0.2.0 — Beta (2026-11-04)

- Promote the tested portability candidate to a normal SemVer release; Beta
  remains a product-maturity label, not certification of every skill or harness.
- Retain all 27 individual skill versions and declared maturity; only the
  library/plugin release version changes from the candidate.
- Record completed Claude Code before/after Ask, Assess, approval-gated Act,
  and context-recap checks, plus the user-observed GitHub-backed plugin upgrade.
- Document in-Claude plugin updates and distinguish standalone copied-skill
  upgrades from marketplace-managed plugin upgrades.
- Preserve candidate lineage and explicitly list not-run compatibility checks
  in `docs/releases/0.2.0-validation.md`.
- No new invocation-time update checker is included. No partner advisory
  instructions or domain references change during this promotion.

## 0.2.0-rc.1 — portability hardening candidate

### Added
- Individual SemVer headers and tooling contracts for all 27 current skills.
- Generated ID-based routing catalog, contract checks, source-review archives,
  plugin-shaped harness exports, compatibility/upgrade evidence records.
- Release manifest/tag consistency checks and tag-triggered GitHub releases.

### Corrected
- Catalog routing no longer points into a source checkout or another skill's contract.
- Declared handoffs match explicit skill routing/workflow references.
- Ask dependencies are conditional; incomplete installation still limits claimed validation.
- Shared instructions use neutral skill IDs and load contracts only when needed.
- Preflight reads scoped saved preferences and skips unused web-consent prompts
  when documentation tools are exposed. Deferred tools and maintainer-listed
  endpoints are not described as live-verified retrievals.

### Unchanged / pending
- Plugin/skill IDs, current descriptions, practitioner/domain knowledge, and
  Ask/Assess/approval-gated Act boundaries are preserved.
- No live host upgrade or behavioral-equivalence result is claimed. The owner
  will test the older local install before stable promotion.
- Consolidated app packaging and description changes are deferred.
- Skill versions begin at 1.0.0 as tracking labels, not validation certificates.
