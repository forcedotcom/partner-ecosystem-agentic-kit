# Owner upgrade test: 0.1.0 to 0.2.0-rc.1

> **Historical procedure:** the old IDs and commands below are intentional.
> For the current rename use [advisor-rename-migration.md](advisor-rename-migration.md).
> For an already-renamed plugin use [ordinary updates](../INSTALL.md#updates).
> Do not follow these legacy commands to install ISV Partner Advisor rc.2.

This is the retained candidate acceptance procedure. The completed owner
comparison and separately observed GitHub-backed installed-version update are
summarized in [0.2.0 validation](releases/0.2.0-validation.md). The `0.2.0` Beta
promotion keeps the candidate's skill payload unchanged. Instructions below
intentionally retain the immutable candidate version for reproducibility; they
do not claim that every installation method or harness has passed.

## Historical candidate test setup

The maintainer's older installation is a project-scoped, directory-backed
marketplace pointing at `vendor/partner-ecosystem-agentic-kit-main`. Its plugin
declares 0.1.0 and predates Headless MCP. Do not replace it before capturing the
baseline. Other users may have different commits despite the same 0.1.0 label.

## Before changing the test installation

1. Finish/close active test sessions; leave unrelated sessions and global skill
   installs alone. Record the installed Claude Code version.
2. In the test project, inspect `/plugin` (or `claude plugin list` where supported).
   Record marketplace source, enabled scope, cache location/version, visible
   skills and duplicate names. Capture the actual base directories reported as
   skills load. Preserve a file inventory/content hashes, not only version labels.
3. Back up the vendor directory and project configuration, including recorded
   `.advisor` preferences, to a separate non-discovery location. Do not publish
   configuration, credentials, or raw private transcripts in this repository.
4. Ask 5–10 representative supplied-context questions. Save sanitized answers,
   loaded skill IDs/base directories, and conclusions before updating.

Suggested comparisons (not evaluator expectations to inject into blind runs):

- An initial product idea with no implementation yet.
- Disposable scratch development versus retaining integration data for months.
- A package boundary/validation question requiring a focused advisor handoff.
- A Headless/API/MCP client-server choice, with no assumption that MCP is needed.
- Current documentation with Docs MCP absent; preserve uncertainty and fallback.
- Documentation tools exposed with no saved web preference; no unused web prompt.
- An explicitly approved synthetic Assess fixture; no org access or edits.
- A proposed harmless fixture change: an Act plan/approval request before execution.
- A context recap preserving goal, mode, evidence gaps, and approval scope.

Do not judge by identical wording or route labels alone. Compare factual
recommendations, consequential questions, evidence honesty, and approval boundaries.

## Obtain the candidate without changing stable users

The GitHub prerelease tag is `v0.2.0-rc.1`. Download `advisor-plugin.zip` from that
release. It has a native plugin-root layout; the source-review ZIP is different.
Do not install the candidate into global directories or publish it as latest.

A tag on the candidate branch does not change a marketplace tracking main.
There are two different tests:

- **Session load:** extract to an isolated review directory and use
  `claude --plugin-dir <plugin-root>`; invoke
  `/oem-isv-advisor:oem-isv-advisor`. This proves only session loading if observed,
  not the installed marketplace upgrade. Check competing copies first.
- **Your directory-backed upgrade:** after baseline/backup, deliberately replace
  the existing marketplace's vendor payload with the candidate plugin payload,
  preserving the configured source path and identities. Then refresh that
  marketplace and update the installed project-scoped plugin. This tests the
  existing directory-backed installation rather than a parallel project-skill copy.

Current documented shell commands, run by the owner in the test project:

```bash
claude plugin marketplace update partner-ecosystem-agentic-kit
claude plugin update oem-isv-advisor@partner-ecosystem-agentic-kit --scope project
```

Check `claude plugin --help` against the installed version before use. These
commands require the directory-backed source to contain the candidate first;
running them against its old files will not fetch the new release from GitHub.
Do not add a second marketplace with the same identity as a shortcut.

For Git-backed users, test a separately configured marketplace pinned to the
candidate tag in an isolated context. Verify the installed-version update there
before claiming GitHub delivery works. Do not repoint a normal user's main-tracking
marketplace silently. The repository README's normal install stays unchanged.

## After update

Start a fresh Claude Code session. Verify plugin version `0.2.0-rc.1`, 27 skills
including `headless-mcp-advisor`, and actual loaded base directories matching
the candidate. Individual metadata version `1.0.0` is not the plugin version.
Compare file hashes with the release manifest, including plugin config hashes.
Repeat the baseline questions and preserve the before/after comparison.

Verify saved preferences are reused only for the same project, harness, and
policy. Legacy preferences lacking project scope may need one explicit
confirmation; this is intentional and must not broaden permission. Neither a
plugin upgrade nor a documentation approval authorizes domain actions.

In an unrelated normal session, the approved skill with the same ID may remain
available. Verify that the **candidate copy**, not the skill name generally,
cannot be discovered or read under the intended controls. A fresh directory or
separate Claude config directory alone does not establish this. Managed
settings, synced resources, credentials, and tool scopes still need inspection.
Do not copy secrets into a test config or bypass permission prompts.

Record loaded skills as objects with `id`, `base_directory`, `version`, and
`skill_md_sha256` in the generated compatibility record. Record visible sources,
duplicate names (including an empty list if none), previous/new plugin versions,
actual delivery mechanism, and sanitized evidence. Missing checks remain not-run.

## Accept or roll back

Accept only after the actual installed candidate loads and recommendations,
handoffs, evidence boundaries, preferences, and approvals are satisfactory.
This does not automatically approve stable publication or unrelated app surfaces.

If it fails, stop candidate sessions, restore the backed-up directory/config,
and use the host's supported project-scoped reinstall/version-selection flow
to restore the previous plugin. Verify the old content actually loads. Do not
delete user-global caches or assume an update command automatically downgrades.
Keep observations and failed evidence; correct the candidate and release a new
RC tag, never retag/overwrite the old one.

Sources checked 2026-11-04:
https://code.claude.com/docs/en/plugins/create,
https://code.claude.com/docs/en/plugins/cli-reference,
https://code.claude.com/docs/en/settings.
