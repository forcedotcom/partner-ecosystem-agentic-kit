# Test the ISV Partner Advisor rename

This is a branch-only migration candidate, **0.3.0-rc.1**, not a release.
The public 0.2.0 release and normal users are unchanged. It builds on the
installation/documentation work in PR #24; do not merge or tag before review
and the owner's live upgrade test.

| Before | Candidate |
| --- | --- |
| ISV/OEM Advisor | ISV Partner Advisor |
| Plugin and entry skill `oem-isv-advisor` | `isv-partner-advisor` |
| `/oem-isv-advisor:oem-isv-advisor` | `/isv-partner-advisor:isv-partner-advisor` |

The repository/marketplace stays `partner-ecosystem-agentic-kit`. OEM guidance,
including partner-specific circumstances, is preserved. Only branding,
discovery descriptions/prompts, entry identity, and its references change.
The entry version is 2.0.0 because its ID changes; other skills get a 1.0.1
identity-reference/branding patch. These version changes do not promote maturity.

## Supported test installation

The helper supports **one existing GitHub-backed Claude Code project-scoped
plugin** in a dedicated non-default `CLAUDE_CONFIG_DIR`. It does not migrate
user, local, managed, synced, directory-backed, or copied-skill installations,
Codex, Cursor, or OpenCode. Those cases stop for manual review, not deletion.
This is deliberately narrower than a general-purpose cleanup utility.

Use the exact project and config directory containing the old installation.
A new empty profile is not an upgrade test. No profile is silently created.
Close all Claude sessions using that profile before applying or rolling back.
The helper refuses recorded marketplace installations in other projects/scopes
and recognized duplicate entry folders. These checks are not an OS sandbox or
proof that every possible synced/global/custom source is inaccessible.

## 1. Get and review the branch

In a terminal, clone to a new directory outside your runtime skill folders:

```bash
git clone --branch codex/isv-partner-advisor-migration --single-branch https://github.com/forcedotcom/partner-ecosystem-agentic-kit.git advisor-rename-test
cd advisor-rename-test
```

Review `scripts/migrate_advisor.py`. Run it from this checkout: it compares
installed skill hashes with **this checkout**, so the branch and source must
match. The default source is the candidate branch; `--ref <commit>` can pin a
reviewed candidate commit. Do not run a remote script through a shell pipe.

## 2. Preview only

Replace the project path. The profile below is an example: use the profile
where your old project plugin is actually installed, not your default profile.

```bash
PROJECT="/absolute/path/to/your/test-project"
PROFILE="$HOME/.claude-advisor-upgrade-test"
python3 scripts/migrate_advisor.py --project "$PROJECT" --claude-config-dir "$PROFILE"
```

No `--apply` means no installation/configuration changes, no backup creation,
and no network calls. The preview reads selected settings/inventory and old
skill files, and reads the cached marketplace Git revision for rollback.
If it stops, review the reason; do not delete files just to satisfy the check.

## 3. Apply after reviewing the preview

Choose a **new** backup directory outside both the test project and profile:

```bash
BACKUP="$HOME/advisor-rename-backup-test-1"
python3 scripts/migrate_advisor.py --project "$PROJECT" --claude-config-dir "$PROFILE" --apply --backup-dir "$BACKUP"
```

Type `MIGRATE` when asked. The helper:

1. Rechecks the preview and takes a private configuration/payload backup.
2. Aligns just this marketplace's source ref in the selected profile's
   `extraKnownMarketplaces` declaration, then uses the native command to repoint
   the existing marketplace to the candidate source. This
   source registration is profile-wide, not project-local, which is why a
   dedicated test profile is required. Other marketplace declarations, unrelated
   settings, and managed settings are not rewritten. Project/local source
   declarations stop for manual alignment rather than being overridden.
3. Installs the new project plugin using native Claude commands. It checks the
   installed identity/version and full skill payload hash against the checkout.
4. Checks unrelated settings and the original skill payload are unchanged, then
   **disables** the old project plugin. It does not uninstall or purge its cache.

MCP configuration must match the old plugin. No host/model session is launched,
no MCP server is connected by the helper, and no org or customer project is
queried. A later host session can request permissions under the new namespace;
installation is not consent to connect or execute anything.

The backup can contain private settings and local content. Keep it private;
never attach it to a public PR or commit it. The script uses a private backup
directory and does not print raw configuration or native CLI output.

## 4. Verify in a fresh Claude session

```bash
cd "$PROJECT"
CLAUDE_CONFIG_DIR="$PROFILE" claude
```

Check `/plugin` → **Installed**: the new identity is enabled in project scope,
the old one is disabled, and the version is `0.3.0-rc.1`. Then invoke:

```text
/isv-partner-advisor:isv-partner-advisor
```

Use a familiar synthetic Ask question and confirm routing to the expected
capability/specialists. Ask an OEM-specific question to check that knowledge
remains. If desired, repeat the previous tightly scoped Assess and separately
approved harmless Act fixture test. Verify actual loaded paths—not just the
model's claim. Capture pass/fail/not-run and any new permission prompts.

An idempotent apply after success verifies the same new payload and makes no
native plugin changes. Structural/synthetic tests are not live upgrade proof.

## Roll back or recover from a partial migration

If a native command fails or a payload/settings check fails, stop. A new plugin
may already be enabled while the old one remains enabled. **Do not start an
advisor session in that partial state.** Inspect the private backup and use:

```bash
python3 scripts/migrate_advisor.py --project "$PROJECT" --claude-config-dir "$PROFILE" --rollback "$BACKUP"
```

Type `ROLLBACK`. This repoints the marketplace to the recorded old commit,
enables the retained old project plugin, and disables the candidate if present.
It does not restore entire settings files over later unrelated edits, delete
caches, or overwrite modified payloads. Restart Claude and verify the old
identity is active. Rollback leaves the marketplace **pinned to the old commit**,
not tracking `main`; return to `main` explicitly only when appropriate.

If the old payload changed or disappeared, automatic rollback stops. The private
backup's `old-plugin/` and configuration snapshots are available for reviewed
manual recovery, not automatic overwrites. A failed or rolled-back candidate
may leave disabled install records; review those before starting another test.

## Cleanup after acceptance

For this test, retaining the disabled old plugin is intentional. Only after
the owner accepts the upgrade should a separate, reviewed cleanup uninstall
the old ID at its exact scope. Do not remove an entire marketplace, shared
cache, `.claude` directory, or another library. No such cleanup is run here.

Native command reference:
[Claude plugin commands](https://code.claude.com/docs/en/plugins/cli-reference).
