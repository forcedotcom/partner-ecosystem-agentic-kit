# Salesforce Partner Ecosystem Agentic Kit

The **ISV/OEM Advisor** helps Salesforce partners turn an idea into a product,
choose its architecture and packaging, prepare for security review, and guide
it through release and operation. Start wherever you are in that journey.

One advisor, with a portable library of 27 supporting skills. You do not need
to select or assemble the individual advisors yourself. The plugin's technical
identifier is `oem-isv-advisor`.

[Install the Advisor](INSTALL.md) ·
[Latest release](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/releases/latest) ·
[Architecture](ARCHITECTURE.md) · [Contributing](CONTRIBUTING.md)

> **Beta:** The current release is **0.2.0 — Beta**. Individual skills retain
> their declared maturity. See the [validation summary](docs/releases/0.2.0-validation.md)
> for observed behavior and checks not run; portability is not certification
> of every app, model, or tool configuration.

## Usage

Choose your app and install the complete advisor library.

| App | Install | Start using the advisor |
| --- | --- | --- |
| Claude Code | [GitHub marketplace plugin](INSTALL.md#claude-code) | `/oem-isv-advisor:oem-isv-advisor` |
| Codex | [Plugin or project-local skills](INSTALL.md#codex) | Select the entry skill or use `$oem-isv-advisor` where supported |
| Cursor | [Project-local skills](INSTALL.md#cursor-and-opencode) | Select `/oem-isv-advisor` in Agent |
| OpenCode | [Project-local skills](INSTALL.md#cursor-and-opencode) | Ask it to load `oem-isv-advisor` |
| ChatGPT and other chat apps | [Check app/workspace capabilities](INSTALL.md#chatgpt-and-other-chat-apps) | Native installation and supporting-skill access must be verified first |

Claude Code installation/upgrade and scoped behavior were maintainer-tested.
Other routes have packaging or documented discovery support, not equivalent
live-host validation. [Compatibility details](docs/harness-compatibility.md).

## Install the advisor

### Claude Code quick start

Open Claude Code in the intended project and enter these commands one at a time:

```text
/plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit
/plugin install oem-isv-advisor@partner-ecosystem-agentic-kit
```

Choose **project** scope for a repository-shared configuration, or **local**
scope for just you in that repository. Review the scope and components before
confirming. Start a fresh session, then invoke:

```text
/oem-isv-advisor:oem-isv-advisor
```

For other apps, terminal commands, copyable setup prompts, and verification,
use the **[installation guide](INSTALL.md)**. Do not install a second copied
library beside an existing plugin without checking for duplicates.

### Try your first question

```text
Use the ISV/OEM Advisor. I am considering a Salesforce partner app, but have
no implementation yet. Help me choose a sensible first build. Stay in Ask
mode, use only the context I provide and available documentation, and ask
the questions that would materially change your recommendation.
```

The advisor routes by your decision, not by the title of a document. It can
also start with an existing product, packaging question, or approved evidence.

## How the advisor works

| Capability | Decisions it helps with |
| --- | --- |
| Solution discovery | Product fit, target users, scope, and first build |
| Packaging and distribution | Package strategy, versions, dependencies, upgrades, and distribution |
| Development environments | Partner foundations, scratch orgs, testing, demos, and trials |
| Implementation best practices | Agentforce, APIs, MCP, and cross-product implementation patterns |
| Platform constraints | Limits, metadata support, gaps, and workarounds |
| Security readiness | Secure design, review preparation, evidence, and remediation |
| Operations and release | Testing, release, rollback, monitoring, and support |

**Ask** guides from supplied context without inspecting your projects or orgs.
**Assess** inspects explicitly approved evidence read-only. **Act** proposes a
bounded plan and requires explicit approval before material changes. Evidence
and uncertainty are labeled; skill metadata does not grant tool permissions.

The advisor checks exposed documentation tools without probing a Salesforce
org. Salesforce Docs MCP is optional and preferred when available. If it is
missing, the advisor offers setup or an approved official-documentation fallback;
declining does not block advice from packaged knowledge. Host and enterprise
permissions always apply. [Documentation setup](INSTALL.md#documentation-access).

## Repository structure

```text
partner-ecosystem-agentic-kit/
├── .claude-plugin/       # Claude plugin and marketplace manifests
├── .codex-plugin/        # Codex plugin manifest
├── skills/               # Complete 27-skill advisor library
│   ├── oem-isv-advisor/
│   ├── advisor-capability-preflight/
│   └── .../
├── adapters/             # Thin host-specific packaging profiles
├── docs/                 # Compatibility, contracts, releases, and testing
├── scripts/              # Maintainer validation and review-bundle utilities
├── tests/                # Library and packaging regression checks
└── INSTALL.md            # App-specific installation and updates
```

The library contains two foundation skills, seven capability routers, and
eighteen focused advisors. Every skill has a portable metadata header and
versioned `references/skill-contract.json` for ownership, modes, dependencies,
evidence, and maturity. [Architecture and inventory](ARCHITECTURE.md) ·
[Contract maintenance](docs/skill-contracts.md).

## Plugins, standalone skills, and updates

Plugins distribute the advisor with client-specific configuration; copied skill
folders carry instructions and supporting files, not automatic MCP setup or
plugin updates. The same skill library is shared across supported layouts,
while each host controls discovery, tools, and permissions.

For Claude Code, use `/plugin` → **Marketplaces** →
**partner-ecosystem-agentic-kit** → **Update marketplace**, then **Installed** →
**ISV/OEM Advisor** → **Update now** if pending. Start a fresh session and verify
the version. Auto-update is optional.

Copied skills must be updated through their original installer/copy mapping,
preserving local changes. Branch- or tag-pinned installs follow that source,
not automatically the latest release. [Update instructions](INSTALL.md#updates) ·
[Release policy](docs/releasing.md).

## Contributing and feedback

Open an [issue](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/issues)
for problems or suggestions, or propose a reviewed pull request. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the process.

Run the library checks from a reviewed checkout:

```bash
python3 -m unittest discover -s tests -v
```

[License](LICENSE.txt) · [Code of conduct](CODE_OF_CONDUCT.md) · [Security](SECURITY.md)
