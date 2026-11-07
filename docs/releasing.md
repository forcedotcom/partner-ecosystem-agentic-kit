# Versions and GitHub releases

Use [Semantic Versioning](https://semver.org/) with `v`-prefixed tags. The
repository/plugin version in `VERSION`, both plugin manifests, and the Claude
marketplace entry must agree. Skill versions and contract schema versions are
independent; do not bump every skill just because the library is released.

The `0.2.0` Beta release promotes the tested `0.2.0-rc.1` portability candidate.
See `releases/0.2.0-validation.md` for acceptance evidence and not-run checks.
Beta describes product maturity; `0.2.0` is a normal SemVer version and its
release is eligible to be latest. It does not certify all hosts or change
individual skill maturity. A tag on a candidate branch leaves main-tracking
installs unchanged; a GitHub release does not itself upgrade a plugin.

## Release candidate

1. Integrate current main while preserving all current skills and descriptions.
2. Set the intended next VERSION and matching distribution manifest versions.
3. Update CHANGELOG.md and docs/releases/current.md with changes, behavior-impact
   labels, upgrade instructions, tests actually run, and explicit not-run checks.
4. Run unit/regression tests, contract/catalog validation, extracted-layout checks,
   and source-review archive tests away from the original checkout.
5. Commit/push the reviewed candidate branch. Create an annotated immutable tag
   such as `v0.2.0-rc.1` at that exact candidate commit and push the tag.
6. The tag-triggered release workflow validates the version and tests again,
   builds plugin/source-review ZIPs, and creates a GitHub prerelease with
   `latest=false` when the version contains a prerelease suffix. If publication
   fails, investigate; never move the tag to hide a failure.
7. Run the owner/pilot upgrade tests in docs/upgrade-testing.md. Record acceptance
   separately from structural tests. Do not claim all hosts passed from one run.

For the `isv-partner-advisor` identity change, use
[the rename migration procedure](advisor-rename-migration.md), not the historical
0.1.0-to-0.2.0 procedure. Already-renamed installs use normal same-ID updates.
Publish a matching reviewed branch revision before asking testers to fetch it;
a local candidate or session-only plugin load is not a marketplace upgrade.

Repository CI needs permission to create releases for the workflow. A maintainer
can publish the same validated tag/assets manually if organization policy blocks
Actions publication; record that fact. Do not enable broader org permissions as
a workaround. Release tags/assets must not be silently replaced.

## Stable promotion

After accepted upgrade results and peer review, choose the stable version,
update matching manifests/notes, rerun checks, merge through normal review, and
tag the approved stable commit (for example `v0.2.0`). The release workflow marks
a non-prerelease tag as latest. Only authorized maintainers should push release
tags; add repository tag/ruleset restrictions through normal governance.

Do not merge the candidate just to make a prerelease available to main-tracking
users. Do not treat a pre-1.0 minor increment as proof that behavior is compatible.
Changes to decisions/modes/outputs still need regression review. Description
shortening and consolidated app packaging stay separate experiments.

## Behavior impact in this candidate

- Plugin/entry identity and invocation change; ordinary updates cannot migrate
  the old ID. Retain recoverable backups and verify the active source/scope.
- Follow-up questions reselect their capability owner before focused advisors.
- Beta target advice separates 1GP from 2GP and leaves unverified persistent
  test prerequisites blocked rather than inventing eligibility.
- Scratch-template convenience settings are not universal build prerequisites.
- Contract schema, authority modes, maturity, and original practitioner records
  remain unchanged. Explicit clarification files scope older guidance.
- The current [validation record](releases/0.3.0-rename-validation.md) distinguishes
  automated checks, session-local behavior, marketplace delivery, and not-run
  coverage. No result automatically authorizes publication or upgrades users.

The legacy 0.1.0 label covered multiple source revisions before this policy.
Preserve the actual prior installed payload/hash for rollback, not only that
label. Do not invent a retrospective release commit for every older install.

Sources: https://semver.org/ and
https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository.
