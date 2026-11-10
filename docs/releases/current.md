# ISV Partner Advisor 0.3.0-rc.2 — rename test candidate

Unreleased branch preview. This checkout does not create a tag or GitHub release.
The published 0.2.0 Beta retains its old identity; it is not silently upgraded.

## Identity change

- Product: **ISV Partner Advisor**.
- Plugin and entry skill: `isv-partner-advisor`.
- Claude invocation: `/isv-partner-advisor:isv-partner-advisor`.
- Codex: select the entry skill or use `$isv-partner-advisor` where supported.
- Existing repository and marketplace identity remain unchanged.
- Entry skill version: 2.0.1; five corrected domain skills: 1.0.2; other skills:
  1.0.1. Contract schema, authority modes, and declared maturity are unchanged.

This is an intentional install/command breaking change, not a routine update.
OEM-specific guidance, specialist scope, and Ask/Assess/approval-gated Act
rules remain. Historical 0.2.0 evidence and baseline fixtures are not rewritten
to claim the new identity was already tested.

## Migration

Use [the scoped project migration guide](../advisor-rename-migration.md).
The preview-first helper uses native Claude plugin commands, private backups,
payload hashes, and explicit approval. It installs/verifies the candidate
before disabling—not deleting—the old project plugin. Rollback re-enables the
retained old plugin and uses the verified private recovery copy as its local
marketplace source. Keep the backup until the source is explicitly changed.

Only a dedicated-profile GitHub-backed Claude project plugin is automated.
Other install methods stop for manual handling. No production/user profiles
are migrated by these edits. Already-renamed plugins use
[ordinary same-ID updates](../../INSTALL.md#updates), not the migration helper.

## Behavior corrections in rc.2

- Select the primary capability as each follow-up changes the partner decision;
  do not skip it merely because a focused specialist is already available.
- Do not reuse 1GP beta target eligibility for managed 2GP. A persistent testing
  recommendation stays conditional on the actual eligible environment and access.
- Do not require the password-setting-through-API convenience feature unless
  the selected workflow needs it.

OEM-specific knowledge and the original practitioner records are retained.
Explicit clarification files scope older guidance. This follow-up includes
bounded behavior changes, not branding alone.

## Validation status

See the [dated rename validation record](0.3.0-rename-validation.md).
66 automated checks (including three documentation guards) and six skill
format checks passed. The automated suite also passed in an independently
extracted source-review archive. A native Claude Code
four-question Ask run of the exact frozen rc.2 payload passed the targeted
routing/eligibility/template-scope checks. It used a session-local plugin load;
it did not update the installed marketplace plugin to rc.2.

Earlier migration/rollback mechanics and the owner's observed renamed rc.1
installation are separate evidence. Native marketplace delivery of rc.2,
Assess/Act, OEM-specific behavior, other hosts, and candidate isolation were
not certified by the four-question rerun. No actual package/org action ran.
The new archive check establishes packaging/test completeness, not an installed
host upgrade or new behavioral coverage. Keep incomplete checks visible.

No PEAK console changes, new MCP connections, or Salesforce org actions are
included. Do not merge or publish until review and owner acceptance.

## One-time installed-source repair tooling (unreleased)

An already-renamed project plugin can still retain the deleted rename branch
in its saved marketplace configuration. The separate
[`repair_update_source.py`](../../scripts/repair_update_source.py) helper repairs
that specific pin before ordinary updates; it does not rerun identity migration.
See [the preview/apply instructions](../../INSTALL.md#repair-a-deleted-branch-pin).

The expanded suite passes 82 tests, including 16 source-repair tests. A native
Claude Code rehearsal in a disposable project/profile completed read-only
preview, source repair, refresh, same-ID update, payload verification, and an
idempotent repeat with no further changes. Its stale pin was deliberately
seeded in the synthetic fixture after installing from main. No real user's
configuration, gateway, model session, MCP session, or Salesforce org was used.
This does not certify every installation scope or prove a fresh host loaded
the plugin; actual session loading remains a separate check.
