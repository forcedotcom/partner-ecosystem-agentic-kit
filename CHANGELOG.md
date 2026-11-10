# Changelog

## Unreleased — installed-source repair tooling

- Add `scripts/repair_update_source.py`: preview-first repair of this advisor's
  deleted branch pin for an already-renamed project plugin in a dedicated profile.
- Back up private settings and the installed payload; align existing source
  declarations without broadening scope, refresh/update through native Claude
  commands, and verify the reviewed target while preserving unrelated settings.
- Refuse custom pins, unsupported/shared scopes, unrelated sources, missing
  installations, concurrent changes, or unexpected integration/payload changes.
- Document one-time repair before ordinary updates. No skill content, plugin
  identity/version, model behavior, or existing user configuration is changed
  by adding this maintainer helper. Apply always needs explicit approval.
- Verification: 82 automated tests pass, including 16 repair tests; a disposable
  native Claude CLI rehearsal verified preview, repair/update, payload, preserved
  unrelated settings, and a no-op repeat. No real installation was changed.

## 0.3.0-rc.2 — rename follow-up and documentation (unreleased)

- Explain fresh installation, old-ID migration, same-ID updates, copied-skill
  handling, and app-specific invocation under ISV Partner Advisor branding.
- Keep repository/marketplace identity unchanged. OEM knowledge remains.
- Re-evaluate capability ownership on follow-ups before using focused advisors.
- Distinguish managed 1GP and 2GP beta installation targets; keep unverified
  persistent-testing prerequisites explicit. Do not promote as a testing shortcut.
- Treat password-setting-through-API as workflow-specific, not a universal
  minimal package-build feature. Preserve original practitioner records.
- Entry version 2.0.1; five affected skills 1.0.2; other skills remain 1.0.1.
  Contract schema, supported modes, and declared maturity are unchanged.
- Record 63 passing automated checks, six skill format checks, and a fresh
  four-turn Claude Code Ask rerun of the frozen rc.2 candidate. This was a
  session-local load, not a marketplace upgrade to rc.2 or all-host certification.
- No tag, release, merge, or installed-user upgrade is performed by these edits.
- Add documentation version/command/link guards; the expanded 66-test suite
  passes in the checkout and an independently extracted source-review archive.
- Include the linked code of conduct and security policy in source-review ZIPs.

## 0.3.0-rc.1 — ISV Partner Advisor rename preview (unreleased)

- Rename branding, plugin identity, entry folder, routing references, and
  invocation to `isv-partner-advisor`; keep the repository/marketplace name.
- Preserve OEM-specific knowledge and authority boundaries. Remove OEM from
  discovery descriptions and suggested prompts, not domain guidance.
- Entry skill version becomes 2.0.0 for the ID change. Other skills become
  1.0.1 for updated identity references/branding; their maturity is unchanged.
- Add a preview-first Claude project-plugin migration helper with private
  backups, payload verification, retained old install, and explicit rollback.
- Keep the 0.2.0 test record historical. Live migration/behavior on the renamed
  identity must be tested before promotion. No tag or release is published here.

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
