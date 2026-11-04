# Versions and GitHub releases

Use [Semantic Versioning](https://semver.org/) with `v`-prefixed tags. The
repository/plugin version in `VERSION`, both plugin manifests, and the Claude
marketplace entry must agree. Skill versions and contract schema versions are
independent; do not bump every skill just because the library is released.

`0.2.0-rc.1` is the portability upgrade candidate. It is not declared stable or
behaviorally accepted. Existing installs and stable main remain unchanged by a
tag on a candidate branch. A GitHub release does not itself upgrade a plugin.

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

- Routing/dependency declarations and invocation resolution can affect handoffs.
- Conditional Ask dependencies allow bounded guidance when a specialist is
  missing; this is not permission to invent that specialist's findings.
- Scoped preference reuse and skipping unused web consent change visible prompts.
- Metadata/catalog/checker/packaging changes are structural but still need actual
  host parsing/loading tests. Existing descriptions and domain knowledge remain.

The legacy 0.1.0 label covered multiple source revisions before this policy.
Preserve the actual prior installed payload/hash for rollback, not only that
label. Do not invent a retrospective release commit for every older install.

Sources: https://semver.org/ and
https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository.
