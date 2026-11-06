# Salesforce Partner Ecosystem Agentic Kit

The **ISV Partner Advisor** helps Salesforce partners turn an idea into a product,
choose its architecture and packaging, prepare for security review, and guide
it through release and operation. Start wherever you are in that journey.

One advisor, with a portable library of 27 supporting skills. You do not need
to select or assemble the individual advisors yourself. The plugin's technical
identifier is `isv-partner-advisor`.

[Install the Advisor](INSTALL.md) ·
[Latest release](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/releases/latest) ·
[Architecture](ARCHITECTURE.md) · [Contributing](CONTRIBUTING.md)

> **Rename preview — not released:** This branch tests **0.3.0-rc.1**, renaming
> the product and entry command to **ISV Partner Advisor** / `isv-partner-advisor`.
> The public **0.2.0 — Beta** release still uses the old identity. Existing users:
> follow the [project migration test](docs/advisor-rename-migration.md), not a
> normal plugin update. OEM-specific knowledge is retained. No new release or
> successful live migration is claimed yet.

## Usage

Choose your app and install the complete advisor library.

| App | Install | Start using the advisor |
| --- | --- | --- |
| Claude Code | [GitHub marketplace plugin](INSTALL.md#claude-code) | `/isv-partner-advisor:isv-partner-advisor` |
| Codex | [Plugin or project-local skills](INSTALL.md#codex) | Select the entry skill or use `$isv-partner-advisor` where supported |
| Cursor | [Project-local skills](INSTALL.md#cursor-and-opencode) | Select `/isv-partner-advisor` in Agent |
| OpenCode | [Project-local skills](INSTALL.md#cursor-and-opencode) | Ask it to load `isv-partner-advisor` |
| ChatGPT and other chat apps | [Check app/workspace capabilities](INSTALL.md#chatgpt-and-other-chat-apps) | Native installation and supporting-skill access must be verified first |

The previous identity's Claude Code upgrade was maintainer-tested; this renamed
candidate still needs its own live upgrade test. Other routes have packaging or
documented discovery support, not equivalent live-host validation.
[Compatibility details](docs/harness-compatibility.md).

## Install the advisor

### Claude Code quick start

For a **fresh, dedicated candidate test profile**, open Claude Code in the
intended project and enter these commands one at a time. Existing installs
should use the [migration helper](docs/advisor-rename-migration.md) instead.

```text
/plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit#codex/isv-partner-advisor-migration
/plugin install isv-partner-advisor@partner-ecosystem-agentic-kit
```

Choose **project** scope for a repository-shared configuration, or **local**
scope for just you in that repository. Review the scope and components before
confirming. Start a fresh session, then invoke:

```text
/isv-partner-advisor:isv-partner-advisor
```

For other apps, terminal commands, copyable setup prompts, and verification,
use the **[installation guide](INSTALL.md)**. Do not install a second copied
library beside an existing plugin without checking for duplicates.

### Try your first question

```text
Use the ISV Partner Advisor. I am considering a Salesforce partner app, but have
no implementation yet. Help me choose a sensible first build. Stay in Ask
mode, use only the context I provide and available documentation, and ask
the questions that would materially change your recommendation.
```

The advisor routes by your decision, not by the title of a document. It can
also start with an existing product, packaging question, or approved evidence.

## How the advisor works

| Capability | Decisions it helps with | Explore its specialists |
| --- | --- | --- |
| [Solution discovery](skills/solution-discovery/SKILL.md) | Product fit, target users, scope, and first build | Handled directly by the capability |
| [Packaging and distribution](skills/packaging-distribution/SKILL.md) | Package strategy, versions, dependencies, upgrades, and distribution | [7 packaging specialists](#packaging-specialists) |
| [Development environments](skills/development-environment/SKILL.md) | Partner foundations, scratch orgs, testing, demos, and trials | [5 environment specialists](#environment-specialists) |
| [Implementation best practices](skills/implementation-best-practices/SKILL.md) | Agentforce, APIs, MCP, and cross-product implementation patterns | [6 implementation specialists, including Headless/MCP](#implementation-specialists) |
| [Platform constraints](skills/platform-constraints/SKILL.md) | Limits, metadata support, gaps, and workarounds | Handled directly by the capability |
| [Security readiness](skills/security-readiness/SKILL.md) | Secure design, review preparation, evidence, and remediation | Handled directly by the capability |
| [Operations and release](skills/operations-release/SKILL.md) | Testing, release, rollback, monitoring, and support | Handled directly by the capability |

### Specialist advisors

These specialists are included in the same advisor installation. Start through
**ISV Partner Advisor** and describe your goal; it routes to the relevant capability
and specialists. You can name an area such as Headless/MCP in your question
without learning the internal skill IDs. The owning capability combines the
specialists' findings into one recommendation.

Browse the linked skill instructions for scope, references, and declared
maturity. A directory entry describes responsibility, not a claim that every
workflow is production-validated or that execution tools are installed. Some
specialists currently provide baseline guidance and still need deeper domain
content and validation; their contracts record that distinction.

#### Implementation specialists

<details open>
<summary>Explore Agentforce, Headless/MCP, Data 360, Slack, Tableau Next, and cross-product patterns</summary>

| Specialist | What it helps you decide |
| --- | --- |
| [Headless / MCP Advisor](skills/headless-mcp-advisor/SKILL.md) | Whether native actions, direct APIs, or MCP fit the job; client/server direction; reusing existing Salesforce logic; package versus customer setup boundaries; optional HXL rich output; and delivery to Agentforce, Slackbot, Claude, or ChatGPT. Advises and assesses approved designs; delegates approved builds to execution skills. |
| [Agentforce Implementation Advisor](skills/agentforce-implementation-advisor/SKILL.md) | Agent, topic, action, prompt template, orchestration, state, testing, and user-experience choices. |
| [Data 360 Implementation Advisor](skills/data-360-implementation-advisor/SKILL.md) | Data architecture, data-kit workflows, enablement prerequisites, package boundaries, and activation ordering. |
| [Slack Implementation Advisor](skills/slack-implementation-advisor/SKILL.md) | Slack applications, authentication, partner sandboxes, Salesforce integration, and packaging boundaries. |
| [Tableau Next Implementation Advisor](skills/tableau-next-implementation-advisor/SKILL.md) | Semantic models, workspaces, visualizations, dashboards, Data 360 dependencies, and deployment ordering. |
| [Implementation Pattern Router](skills/implementation-pattern-router/SKILL.md) | Which product-specific specialists to consult and how to combine Agentforce, Apex, APIs, prompts, MCP, and other product findings into a cross-product pattern. |

Example: “We already have Salesforce business logic and want to expose one task
to Claude and Slackbot. Do we need MCP, what belongs in our package, and what
must each customer configure?”

</details>

#### Packaging specialists

<details>
<summary>Explore package strategy, packageability, foundations, validation, dependencies, promotion, and migration</summary>

| Specialist | What it helps you decide |
| --- | --- |
| [Packaging Strategy](skills/packaging-strategy/SKILL.md) | Whether to package, which model to use, and where package and distribution boundaries belong. |
| [Packageability Assessment](skills/packageability-assessment/SKILL.md) | What approved source and metadata can be packaged, which dependencies or unsupported components matter, and what remediation evidence is needed. |
| [Managed 2GP Foundation](skills/managed-2gp-foundation/SKILL.md) | Package ownership, Dev Hub, namespace, source layout, and irreversible creation decisions. |
| [Package Version Validation](skills/package-version-validation/SKILL.md) | Build-org shape, validation mode, code coverage, installation keys, candidate testing, and version-create failures. |
| [Package Ancestry and Dependencies](skills/package-ancestry-dependencies/SKILL.md) | Version numbering, ancestry, explicit and transitive dependencies, patches, and upgrade paths. |
| [Package Release Promotion](skills/package-release-promotion/SKILL.md) | Whether an exact version has the evidence and prerequisites needed for promotion and distribution. |
| [Package Migration and Transfer](skills/package-migration-transfer/SKILL.md) | Managed 1GP-to-2GP migration and recovery when a managed 2GP package belongs to the wrong Dev Hub. |

</details>

#### Environment specialists

<details>
<summary>Explore PBO/Dev Hub, namespaces, scratch org shape, environment selection, and provisioning diagnostics</summary>

| Specialist | What it helps you decide |
| --- | --- |
| [PBO / Dev Hub Foundation](skills/pbo-dev-hub-foundation/SKILL.md) | Partner Business Org identity, lifecycle evidence, Dev Hub selection, entitlements, and ownership recovery. |
| [Namespace and Access Governance](skills/namespace-access-governance/SKILL.md) | Namespace-org topology, namespace linking, Environment Hub inventory, developer access, and least privilege. |
| [Scratch Org Shape](skills/scratch-org-shape/SKILL.md) | Scratch definitions, editions, features, settings, entitlement checks, and package-build shape. |
| [Environment Portfolio](skills/environment-portfolio/SKILL.md) | Which environment fits each job: disposable development, persistent tests, demos, trials, or customer validation. |
| [Org Provisioning Diagnostics](skills/org-provisioning-diagnostics/SKILL.md) | Provisioning status, capacity, expiration, errors, cleanup, and health for scratch, Test/Demo, Trialforce, and template-backed environments. |

</details>

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
│   ├── isv-partner-advisor/
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

The old ID will not turn into the new ID through **Update now**. Existing users
must first complete the [identity migration](docs/advisor-rename-migration.md).
After migration, ordinary updates for the new plugin use `/plugin` → **Marketplaces** →
**partner-ecosystem-agentic-kit** → **Update marketplace**, then **Installed** →
**ISV Partner Advisor** → **Update now** if pending. Start a fresh session and verify
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
