# Salesforce Partner Ecosystem Agentic Kit

The **ISV/OEM Advisor** is one portable Salesforce partner advisory system for
Codex, Claude Code, Cursor, and other compatible harnesses. ISV and OEM
partners install the advisor to accelerate their partnership at any stage—from
an initial product idea through architecture, packaging, implementation,
distribution, security review, release, and long-term operation.

The plugin is the product. Its skills are the advisor's internal capability
library, not separate products that a partner must assemble. The technical
plugin identifier is `oem-isv-advisor`; its user-facing name is **ISV/OEM
Advisor**.

**[Install the Advisor](#install-the-advisor)** ·
[Latest release](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/releases/latest) ·
[Installation and update guide](INSTALL.md)

## Architecture baseline

The repository contains the 27-skill ISV/OEM Advisor: two foundation skills,
seven capability routers, and eighteen focused advisors.
Every folder has a stable ID, ownership boundary, Ask/Assess/Act authority,
evidence rules, and execution-delegation contract. Some skills begin with
baseline guidance and mature through partner scenarios, practitioner input,
and evidence-backed updates without changing the overall product architecture.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the capability map, skill inventory,
and pull-request layering model.

Every skill declares portable metadata in its header and a versioned
`references/skill-contract.json` for ownership, mode boundaries, conditional
dependencies, evidence, and declared maturity. The capability catalog is
generated from these contracts. See [skill contract maintenance](docs/skill-contracts.md)
for authoring and validation commands. Declarations do not grant permissions or
replace commit-bound validation evidence.

The two foundation entry points are:

- `oem-isv-advisor`, which preserves the partner goal and routes the decision.
- `advisor-capability-preflight`, which checks Salesforce documentation
  capability, obtains customer consent, and selects an honest fallback.

The preflight never probes a Salesforce org. A Salesforce org/data MCP server
is not treated as a documentation MCP server.

## Install the advisor

Choose your app below. Install the **whole advisor library**, not just the entry
skill: its supporting advisors and references are needed for routing.

| App | Installation route | Validation status |
| --- | --- | --- |
| Claude Code | GitHub marketplace plugin | Maintainer-tested install/upgrade and scoped behavior |
| Codex | Plugin, or project-local skill folders | Packaging checked; separate live host test still needed |
| Cursor | Project-local skill folders | Documented discovery route; live test still needed |
| OpenCode | Project-local skill folders | Documented discovery route; live test still needed |
| ChatGPT | Depends on app/workspace installation capabilities | Not certified by the Claude Code test |

<details open>
<summary><strong>Claude Code — install commands</strong></summary>

Open Claude Code in the project where you want to use the advisor. Enter these
commands **inside Claude Code**, one at a time:

```text
/plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit
/plugin install oem-isv-advisor@partner-ecosystem-agentic-kit
```

Choose **project** scope when asked if you only want it in that project.
Start a new session, then invoke:

```text
/oem-isv-advisor:oem-isv-advisor
```

Verify **ISV/OEM Advisor** is enabled under `/plugin` → **Installed**.
The marketplace is a GitHub source registration, not a requirement to join a
public app store. [Shell alternative and updates](INSTALL.md#claude-code).

</details>

<details>
<summary><strong>Codex — installation prompt</strong></summary>

Copy this into Codex in the intended project:

```text
Help me install the complete ISV/OEM Advisor from
https://github.com/forcedotcom/partner-ecosystem-agentic-kit.
Use its INSTALL.md Codex instructions. Prefer the native plugin route if this
host supports it; otherwise propose a project-local installation of all skill
folders, including references. Inspect existing copies first and ask before
overwriting files or changing shared settings. Do not connect MCPs or access
a Salesforce org as part of installation. Report the source revision and scope.
```

After installation, start a fresh session and select **ISV/OEM Advisor**, or
invoke `$oem-isv-advisor` where supported. [Codex setup details](INSTALL.md#codex).

</details>

<details>
<summary><strong>Cursor — installation prompt</strong></summary>

Copy this into Cursor Agent in the intended project:

```text
Help me install the complete ISV/OEM Advisor from
https://github.com/forcedotcom/partner-ecosystem-agentic-kit.
Follow INSTALL.md for Cursor. Propose copying all released skill folders,
including references and scripts, into this project's .cursor/skills/.
Check for duplicate or locally modified skills first. Ask before making changes,
do not overwrite unrelated skills, and do not change global settings or connect
MCPs. Report the installed source revision and how to select the entry skill.
```

[Cursor setup and verification](INSTALL.md#cursor-and-opencode).

</details>

<details>
<summary><strong>OpenCode — installation prompt</strong></summary>

Copy this into OpenCode in the intended project:

```text
Help me install the complete ISV/OEM Advisor from
https://github.com/forcedotcom/partner-ecosystem-agentic-kit.
Follow INSTALL.md for OpenCode. Propose copying all released skill folders,
including references and scripts, into this project's .opencode/skills/.
Check for duplicate or locally modified skills first. Ask before making changes,
do not overwrite unrelated skills, and do not change global settings or connect
MCPs. Report the installed source revision and verify oem-isv-advisor is available.
```

[OpenCode setup and verification](INSTALL.md#cursor-and-opencode).

</details>

<details>
<summary><strong>ChatGPT — check your installation options first</strong></summary>

ChatGPT surfaces and workspace policies differ. This repository does not yet
claim a verified one-click ChatGPT installation or a public directory listing.
Do not upload `advisor-plugin.zip` or `advisor-source-review.zip` as if either
were a single native skill.

Copy this into the intended ChatGPT surface:

```text
I want to use the complete ISV/OEM Advisor from
https://github.com/forcedotcom/partner-ecosystem-agentic-kit.
Read its INSTALL.md ChatGPT section if you can access it. Tell me which native
plugin or skill-installation options are actually available in this surface.
Do not claim it is installed by merely reading files. If installation or access
to all supporting advisors cannot be verified, explain that limitation.
```

[ChatGPT limitations and next steps](INSTALL.md#chatgpt-and-other-chat-apps).

</details>

**More options:** [terminal commands and manual installation](INSTALL.md) ·
[view release downloads](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/releases/latest).
Review downloaded source before running scripts. Installation does not authorize
Salesforce access, deployment, or connecting an MCP server.

### Beta release and updates

The library/plugin version is in `VERSION` and the distribution manifests;
individual skill versions are tracked independently in their metadata headers.
See [GitHub Releases](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/releases),
[release policy](docs/releasing.md), and [upgrade testing](docs/upgrade-testing.md).
The current release is **0.2.0 — Beta**, promoting the tested `0.2.0-rc.1`
candidate. Beta describes product maturity; individual skills retain their
declared maturity. See the [validation summary](docs/releases/0.2.0-validation.md)
for observed behavior, installation evidence, and checks not run.

Existing main-tracking Claude Code plugin users can update without shell
commands: open `/plugin`, select **Marketplaces**, select
**partner-ecosystem-agentic-kit**, and choose **Update marketplace**. If an
update remains pending, open **Installed**, select **ISV/OEM Advisor**, and choose
**Update now**. Start a fresh session and confirm the version. Auto-update is
optional and can be enabled in the marketplace's settings; this repository does
not silently enable it.

An ordinary marketplace update follows the configured source branch or tag.
Publishing a GitHub Release alone does not move an installation to a different
source. Testers pinned to the candidate branch must explicitly return their
marketplace source to `main` to follow normal releases.

Project-local copies in `.agents/skills/` or another skill folder are a different
installation method, even if they originally came from GitHub. Update them
using their original installer/copy mapping and source lock, preserving local
changes and other libraries. A plugin update does not update copied files.

### Other harnesses and isolated compatibility testing

Use the [harness compatibility guide](docs/harness-compatibility.md) for Cursor,
app-based skill uploads, and explicit file-based fallback. The review-bundle
tool packages the same versioned skills with thin host-specific guidance; it
does not install skills or certify app behavior. Draft candidates must stay out
of ordinary discovery folders and shared app libraries.

## Documentation setup behavior

On first use, the advisor checks the tools exposed by the harness:

1. If Salesforce Docs MCP is connected, it is preferred.
2. The plugin offers Salesforce's published `salesforce-docs` MCP as an
   optional, highly recommended integration. The advisor asks before installing
   or connecting it; declining never blocks the advisor.
3. If no verified installation source is available, the advisor offers exact,
   read-only Salesforce documentation domains as fallback.
4. If the customer declines or enterprise policy blocks access, the advisor
   continues with packaged knowledge and labels unsupported current claims as
   unknown.

Customer consent never bypasses host or enterprise security policy. The
Salesforce Docs MCP identity, endpoint, tools, and Claude Code command are
verified against
`https://labs.agentforce.com/docs/salesforce-docs-mcp`. Changes to that source
must be reviewed before updating the packaged dependency.

## Validate

```bash
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py skills/oem-isv-advisor
python3 /path/to/skill-creator/scripts/quick_validate.py skills/advisor-capability-preflight
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the normal human review process.
