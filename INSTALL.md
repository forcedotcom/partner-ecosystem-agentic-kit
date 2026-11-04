# Install ISV/OEM Advisor

One advisor, with its complete supporting skill library. Choose your app;
you do not need to assemble the individual advisors yourself.

[Claude Code](#claude-code) · [Codex](#codex) ·
[Cursor / OpenCode](#cursor-and-opencode) · [ChatGPT](#chatgpt-and-other-chat-apps) ·
[Verify installation](#verify-installation) · [Updates](#updates)

## Before you install

- Use the [latest published release](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/releases/latest),
  or the approved `main` branch for normal marketplace updates. Do not point
  everyday sessions at a draft PR or experimental branch.
- Choose the intended project and scope. Project-local folders can still be
  read by other tools with access to that project; they are not a sandbox.
- Check for existing copies before installing. Never overwrite modified skills,
  delete unrelated libraries, or enable global/synced installations silently.
- Installation is not approval to run included scripts, connect MCPs, inspect
  an org, or deploy anything. Honor host and organization permission prompts.

## Claude Code

In a Claude Code session opened in your intended project:

```text
/plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit
/plugin install oem-isv-advisor@partner-ecosystem-agentic-kit
```

Choose **project** scope when prompted for a project-only installation. In
`/plugin` → **Installed**, check the scope, version, and enabled status.
Start a fresh session, then invoke:

```text
/oem-isv-advisor:oem-isv-advisor
```

If you prefer commands in a terminal rather than inside the Claude chat, use:

```bash
claude plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit
claude plugin install oem-isv-advisor@partner-ecosystem-agentic-kit --scope project
```

Marketplace registration and plugin installation are separate: adding the
source does not itself install the plugin. The project scope applies to the
plugin; source registration may be shared by your Claude configuration.
Do not add a second copied-skill installation beside the plugin.

Source: [Claude Code plugin installation](https://code.claude.com/docs/en/plugins/install).
See the [observed upgrade evidence](docs/releases/0.2.0-validation.md) for what
we tested and what remains untested.

## Codex

Use the host's plugin installation flow for this GitHub repository when it is
available. Confirm that the installed plugin is **ISV/OEM Advisor** with
technical identifier `oem-isv-advisor`. If that host cannot install this
repository as a plugin, use the explicit project-local fallback below rather
than inventing an install command or assuming a public directory listing.

For a project-local fallback, download a released source archive, review it,
and copy **every complete child folder of `skills/`** into the target project's
`.agents/skills/`. Keep each folder's `SKILL.md`, `references/`, `scripts/`, and
other supporting files intact. Review conflicts before copying. Do not copy
only the entry skill or flatten its references. This installs skills, not plugin
MCP configuration, hooks, or automatic updates.

Start a fresh session in that project and select the entry skill, or invoke:

```text
$oem-isv-advisor
```

Sources: [official skill discovery and invocation](https://learn.chatgpt.com/docs/build-skills),
[Codex marketplace commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin-marketplace).
Host support and permissions still need verification in your actual session.

## Cursor and OpenCode

These are manual, project-local skill installations, not Claude plugin installs.

| App | Copy all complete `skills/` child folders into | Start using it |
| --- | --- | --- |
| Cursor | `<project>/.cursor/skills/` | Open Agent and select `/oem-isv-advisor` |
| OpenCode | `<project>/.opencode/skills/` | Ask it to load the `oem-isv-advisor` skill |

Download and review the released source, then copy all skill directories with
their supporting files. For example, the entry file in Cursor must land at
`.cursor/skills/oem-isv-advisor/SKILL.md`, not
`.cursor/skills/skills/oem-isv-advisor/SKILL.md`.

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

## Verify installation

In a fresh session, ask:

```text
Use the installed ISV/OEM Advisor. Confirm the installed source and scope if
visible, load its entry skill, and tell me whether its supporting advisors are
available. Stay in Ask mode. Do not inspect a Salesforce org, edit files, or
connect tools. If you cannot verify an installation detail, mark it unknown.
```

Check host inventory/settings and actual loaded paths as well as the answer.
Successful file reading alone does not prove native discovery, complete routing,
or isolation. A missing optional Salesforce Docs MCP does not block installation;
the advisor must report documentation limitations honestly.

## Updates

For main-tracking Claude Code plugins, open `/plugin` → **Marketplaces** →
**partner-ecosystem-agentic-kit** → **Update marketplace**. If pending, use
**Installed** → **ISV/OEM Advisor** → **Update now**. Start a fresh session and
verify the version. Auto-update is optional; this repository does not enable it.

Copied-folder installs do not update through the plugin menu. Use the original
installer/copy mapping, preserve local changes and other libraries, and record
the new source revision. Ask before replacing existing files. Do not switch
someone's installation method silently.

Sources pinned to a branch or tag follow that source, not automatically the
latest GitHub release. Candidate testers must explicitly return to `main` to
follow normal updates. See [upgrade testing](docs/upgrade-testing.md) for the
separate maintainer verification procedure.
