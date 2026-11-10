# Install ISV Partner Advisor

> **Pre-release on `main`.** New identity: `isv-partner-advisor`, version
> `0.3.0-rc.2`, not yet a tagged release. Existing `oem-isv-advisor` installs need the
> [migration procedure](docs/advisor-rename-migration.md). A regular update does
> not rename an installed plugin. The 0.2.0 release downloads still use the old name.

One advisor, with its complete supporting skill library. Choose your app;
you do not need to assemble the individual advisors yourself.

[Claude Code](#claude-code) · [Codex](#codex) ·
[Cursor / OpenCode](#cursor-and-opencode) · [ChatGPT](#chatgpt-and-other-chat-apps) ·
[Verify installation](#verify-installation) · [Updates](#updates)

## Existing users and the name change

The product is **ISV Partner Advisor**. The plugin ID and entry skill are
`isv-partner-advisor`; the repository and marketplace name remain
`partner-ecosystem-agentic-kit`. OEM-specific expertise is still included.

| Your installation | Correct path |
| --- | --- |
| Fresh Claude Code install | Use [Claude Code](#claude-code) below; do not create another copy if one already exists. |
| Old `oem-isv-advisor` Claude project plugin | Use the [scoped migration guide](docs/advisor-rename-migration.md) in a dedicated existing test profile. Preview, back up, install/verify the new identity, then disable the old one. A routine update cannot rename it. |
| Already renamed Claude plugin | Use [Updates](#updates); do not rerun identity migration to update rc.1 to rc.2. |
| Codex plugin | Use the host's supported install/disable flow, verify the new ID, and preserve the old configuration for rollback. The Claude script does not migrate Codex. |
| Copied skills in Codex, Cursor, or OpenCode | Back up the original library and local edits; reconcile against one reviewed revision. Replace the old entry folder with the new one only after reviewing conflicts, and update the supporting library together. Do not leave both entry copies active or delete unrelated skills. |
| User-wide, local-scope, managed, synced, or directory-backed Claude plugin | Manual review is required; these are not supported by the current migration helper. Do not convert the install method silently. |

The old Claude command `/oem-isv-advisor:oem-isv-advisor` becomes
`/isv-partner-advisor:isv-partner-advisor`. In Codex, use
`$isv-partner-advisor` where supported, or select the entry skill in the host.
Update saved prompts and project guidance that invoke the old entry ID; do not
blindly replace OEM terminology inside domain references or historical records.

## Before you install

- Install from `main`, which carries the renamed `isv-partner-advisor`. The
  [latest published release](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/releases/latest)
  (0.2.0) still uses the old identity. Do not point everyday sessions at a draft
  PR or experimental branch.
- Choose the intended project and scope. Project-local folders can still be
  read by other tools with access to that project; they are not a sandbox.
- Check for existing copies before installing. Never overwrite modified skills,
  delete unrelated libraries, or enable global/synced installations silently.
- Installation is not approval to run included scripts, connect MCPs, inspect
  an org, or deploy anything. Honor host and organization permission prompts.

## Copyable setup prompt

If your app has an assistant that can inspect GitHub and manage approved local
files, paste this into the intended project. Review its proposed route and
scope before approving changes; this is a request for setup, not an installer
or a guarantee that the app supports native skills.

```text
Help me install the complete ISV Partner Advisor from
https://github.com/forcedotcom/partner-ecosystem-agentic-kit.
Use the main branch. Read its INSTALL.md and use the route for this app.
Check that the plugin manifest identity is isv-partner-advisor before changing
anything. Prefer its supported native
plugin route; otherwise propose the documented project-local skill layout.
Inspect existing copies first, preserve all supporting references, and ask
before making changes. Do not overwrite modified or unrelated skills, change
global settings, connect MCPs, or inspect a Salesforce org. Report the installed
source revision and scope, and verify that the entry and supporting advisors
are available. If this app cannot install them, explain that limitation rather
than claiming file reading is an installation.
```

## Claude Code

These commands install from `main` (`0.3.0-rc.2`), not the 0.2.0 release
archives. They are for a fresh install; existing `oem-isv-advisor` installs use
the [migration procedure](docs/advisor-rename-migration.md). Verify the actual
installed version below.

In a Claude Code session opened in your intended project:

```text
/plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit
/plugin install isv-partner-advisor@partner-ecosystem-agentic-kit
```

Choose **project** scope for repository-shared settings, or **local** scope for
just you in that repository. In
`/plugin` → **Installed**, check the scope, version, and enabled status.
Start a fresh session, then invoke:

```text
/isv-partner-advisor:isv-partner-advisor
```

If you prefer commands in a terminal rather than inside the Claude chat, use:

```bash
claude plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit --scope project
claude plugin install isv-partner-advisor@partner-ecosystem-agentic-kit --scope project
```

Marketplace registration and plugin installation are separate: adding the
source does not itself install the plugin. The project scope applies to the
plugin; source registration has its own scope. The shell example declares it
at project scope on Claude Code versions supporting that option. Check
`claude plugin marketplace add --help`; do not fall back to a broader scope
without reviewing the impact on other projects. Use the same intended
`CLAUDE_CONFIG_DIR` for installation, updates, and launching Claude when your
setup uses a dedicated profile; it is not selected automatically by `cd`.
Do not add a second copied-skill installation beside the plugin.

Source: [Claude Code plugin installation](https://code.claude.com/docs/en/plugins/install).
See the [rename test evidence](docs/releases/0.3.0-rename-validation.md) and
[historical 0.2.0 upgrade evidence](docs/releases/0.2.0-validation.md) for the
different installation and behavior checks actually performed.

## Codex

Use the host's plugin installation flow for this GitHub repository when it is
available. Confirm that the installed plugin is **ISV Partner Advisor** with
technical identifier `isv-partner-advisor`. If that host cannot install this
repository as a plugin, use the explicit project-local fallback below rather
than inventing an install command or assuming a public directory listing.

For a project-local install, use a reviewed checkout of `main`, not the
0.2.0 release archives with the old identity, and copy **every complete child folder of `skills/`** into the target project's
`.agents/skills/`. Keep each folder's `SKILL.md`, `references/`, `scripts/`, and
other supporting files intact. Review conflicts before copying. Do not copy
only the entry skill or flatten its references. This installs skills, not plugin
MCP configuration, hooks, or automatic updates.

Start a fresh session in that project and select the entry skill, or use the
explicit invocation supported by Codex CLI and IDE surfaces:

```text
$isv-partner-advisor
```

In a desktop skill picker, select **ISV Partner Advisor** instead of assuming
Claude's namespaced slash command works there. Inspect duplicates: local,
plugin, user, and ancestor-folder copies can coexist and are not merged.

Sources: [official skill discovery and invocation](https://learn.chatgpt.com/docs/build-skills),
[Codex marketplace commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin-marketplace).
Host support and permissions still need verification in your actual session.

## Cursor and OpenCode

These are manual, project-local skill installations, not Claude plugin installs.

| App | Copy all complete `skills/` child folders into | Start using it |
| --- | --- | --- |
| Cursor | `<project>/.cursor/skills/` | Open Agent and select `/isv-partner-advisor` |
| OpenCode | `<project>/.opencode/skills/` | Ask it to load the `isv-partner-advisor` skill |

Review the `main` branch source, then copy all skill directories with
their supporting files. For example, the entry file in Cursor must land at
`.cursor/skills/isv-partner-advisor/SKILL.md`, not
`.cursor/skills/skills/isv-partner-advisor/SKILL.md`.

Check existing project, user, plugin, and compatible skill locations for
duplicates first. Start a fresh session after installation. Confirm that the
entry skill and its supporting advisors are visible; do not infer that MCPs
were installed along with the files. These discovery routes are documented by
the hosts, but we have not certified live behavior in these hosts for this release.

Sources: [Cursor skill locations](https://cursor.com/help/customization/skills),
[OpenCode skill locations and permissions](https://opencode.ai/docs/skills/).

For an optional review-only archive from a reviewed library checkout:

```bash
python3 scripts/prepare_harness.py bundle --target cursor-local --output /tmp/advisor-cursor-review.zip
```

This creates a ZIP; it does **not** install anything. Review its `START-HERE.md`
and payload before extracting into the intended project. Do not run downloaded
scripts without reviewing them. [Packaging and isolation details](docs/harness-compatibility.md).

## ChatGPT and other chat apps

Do not assume that ChatGPT, Codex, Claude chat, and Claude Code share the same
installation features. Native plugin/skill access depends on the exact app and
workspace policy. Official OpenAI documentation describes skills and plugin
distribution across ChatGPT/Codex; that does not establish a directory listing
or working installation for this particular library.

This release has no verified end-to-end ChatGPT installation record. If the
surface offers a compatible installation route, confirm that it can load all
required advisors and linked contract/reference files before relying on the
library. If it cannot, use a supported local-host route above. Attaching source
files for one conversation is reference use, not persistent skill installation.

The release's `advisor-plugin.zip` is a plugin distribution, and
`advisor-source-review.zip` is a review archive. Neither is a consolidated,
single-skill upload for a chat app. Do not relabel them as such.

Source: [OpenAI skills and plugin distribution](https://learn.chatgpt.com/docs/build-skills).
For other app-specific packaging, see the [compatibility guide](docs/harness-compatibility.md).

## Documentation access

On first use, the advisor checks tools exposed by the host. Salesforce Docs MCP
is optional and preferred when available; an org/data MCP is not a substitute.
The advisor asks before installing or connecting the documentation integration.
If unavailable, it offers approved official-documentation domains as fallback.
If access is declined or blocked, it continues with packaged knowledge and
labels unsupported current claims as unknown. Host security prompts still apply.

The published Salesforce Docs MCP identity and setup source is
[Salesforce Docs MCP](https://labs.agentforce.com/docs/salesforce-docs-mcp).
The library's [documentation policy](skills/advisor-capability-preflight/references/documentation-policy.json)
records its approved source and fallback rules. Installation alone does not
prove documentation connectivity or authorize access to a Salesforce org.

## Verify installation

For the current `main`, expect plugin version **0.3.0-rc.2** and
entry ID **isv-partner-advisor**. Plugin versions, individual skill versions,
and contract-schema versions are different; do not compare them as one number.
The full library has 27 skills. After migration, the old entry must be disabled
or otherwise excluded from the tested scope, not silently blended with the new.

In a fresh session, ask:

```text
Use the installed ISV Partner Advisor. Confirm the installed source and scope if
visible, load its entry skill, and tell me whether its supporting advisors are
available. Stay in Ask mode. Do not inspect a Salesforce org, edit files, or
connect tools. If you cannot verify an installation detail, mark it unknown.
```

Check host inventory/settings and actual loaded paths as well as the answer.
Successful file reading alone does not prove native discovery, complete routing,
or isolation. A missing optional Salesforce Docs MCP does not block installation;
the advisor must report documentation limitations honestly.

### First conversation

```text
Use the ISV Partner Advisor. We are considering a Salesforce partner app for
account managers to prepare renewal-risk briefs from approved Salesforce
information. We have no implementation yet. Help choose a sensible first build.
Stay in Ask mode; do not inspect a project or Salesforce org or create anything.
```

Continue in the same conversation as the decision changes. For example, add
your users, approved data, and whether the brief is viewed/copied or saved,
then ask whether native capabilities, direct APIs, or MCP are needed. The
appropriate capability owns the response and incorporates specialist findings.
You do not need to invoke every specialist yourself.

Ask uses supplied context and available references. Assess needs explicit
read-only inspection scope. Act needs a bounded plan and approval for the
specific change. Approving an installation is not approval for an org action.

## Updates

For the old-to-new identity transition, use the
[migration helper](docs/advisor-rename-migration.md), not the normal update menu.
The instructions below apply once the new plugin is installed and a supported
release source has been chosen.

For a Claude Code plugin already using the new ID, open `/plugin` → **Marketplaces** →
**partner-ecosystem-agentic-kit** → **Update marketplace**. If pending, use
**Installed** → **ISV Partner Advisor** → **Update now**. Start a fresh session and
verify the version. Auto-update is optional; this repository does not enable it.

The equivalent shell commands, run from the intended project with the same
profile as the installation, are:

```bash
claude plugin marketplace update partner-ecosystem-agentic-kit
claude plugin update isv-partner-advisor@partner-ecosystem-agentic-kit --scope project
```

Use the actual installed scope if it is not project-scoped; do not create a
second installation to make the example match. These commands refresh the
configured source and update the **same** plugin ID; they do not change a
branch pin or migrate the old identity. An already-migrated rc.1 tester uses
this update flow after the reviewed rc.2 branch changes are pushed.

Copied-folder installs do not update through the plugin menu. Use the original
installer/copy mapping, preserve local changes and other libraries, and record
the new source revision. Ask before replacing existing files. Do not switch
someone's installation method silently.

Sources pinned to a branch or tag follow that source, not automatically the
latest GitHub release. Testers who pinned the deleted
`codex/isv-partner-advisor-migration` branch must repoint their marketplace to
`main` to keep receiving updates. See [upgrade testing](docs/upgrade-testing.md) for the
separate maintainer verification procedure.

## Troubleshooting names, versions, and profiles

- **Only the old name appears:** check whether you installed the published
  0.2.0 source or a stale branch. Do not install both identities and assume the
  host will choose correctly. Use the migration path for an existing old plugin.
- **Update reports no change:** check the marketplace's saved source ref and
  actual remote revision. A GitHub release, local edit, or version label alone
  does not update a pinned source. Refresh the marketplace, update the plugin,
  and start a fresh session before verifying the loaded path.
- **Renamed rc.1 is already installed:** use ordinary same-ID updates, not the
  old-to-new migration helper. Preserve the original migration backup.
- **Gateway/authentication fails only in the test profile:** verify the same
  intended profile and organization-approved authentication configuration are
  used when launching. Do not copy an entire global configuration, bypass the
  gateway, print credentials, or re-enable unrelated plugins as a workaround.
- **Unexpected agents, banners, or skills load:** inspect project, ancestor,
  user, managed, and synced sources with the host's inventory tools. A new
  folder or profile is not proof of isolation. Do not delete shared settings.
