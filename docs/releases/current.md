# ISV Partner Advisor 0.3.0-rc.1 — rename test candidate

Unreleased branch preview. No tag or GitHub release is created by this change.

## Identity change

- Product: **ISV Partner Advisor**.
- Plugin and entry skill: `isv-partner-advisor`.
- Claude invocation: `/isv-partner-advisor:isv-partner-advisor`.
- Existing repository and marketplace identity remain unchanged.
- Entry skill version: 2.0.0. Other skills: 1.0.1 for identity references and
  branding. Contract schema and declared maturity are unchanged.

This is an intentional install/command breaking change, not a routine update.
OEM-specific guidance, specialist scope, and Ask/Assess/approval-gated Act
rules remain. Historical 0.2.0 evidence and baseline fixtures are not rewritten
to claim the new identity was already tested.

## Migration

Use [the scoped project migration guide](../advisor-rename-migration.md).
The preview-first helper uses native Claude plugin commands, private backups,
payload hashes, and explicit approval. It installs/verifies the candidate
before disabling—not deleting—the old project plugin. Rollback re-enables the
retained old plugin and pins the source to the recorded old commit.

Only a dedicated-profile GitHub-backed Claude project plugin is automated.
Other install methods stop for manual handling. No production/user profiles
or real installations were migrated while building this candidate.

## Validation status

All 55 automated library and synthetic migration/failure/rollback tests pass,
including in an independently extracted source-review archive. Contract checks,
knowledge-preservation guards, skill validation, and native Claude plugin
validation pass. Existing listing warnings about icon/privacy URL remain.
The owner must still test the actual old-to-new plugin upgrade and relevant
Ask/Assess/Act behavior in the selected project. No new live-host result,
cross-harness certification, or successful candidate isolation is claimed.

No PEAK console changes, new MCP connections, or Salesforce org actions are
included. Do not merge or publish until review and owner acceptance.
