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

## Architecture baseline

The repository contains the complete 26-skill ISV/OEM Advisor skeleton: two
foundation skills, seven capability routers, and seventeen focused advisors.
Every folder has a stable ID, ownership boundary, Ask/Assess/Act authority,
evidence rules, and execution-delegation contract. Some skills begin with
baseline guidance and mature through partner scenarios, practitioner input,
and evidence-backed updates without changing the overall product architecture.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the capability map, skill inventory,
and pull-request layering model.

The two foundation entry points are:

- `oem-isv-advisor`, which preserves the partner goal and routes the decision.
- `advisor-capability-preflight`, which checks Salesforce documentation
  capability, obtains customer consent, and selects an honest fallback.

The preflight never probes a Salesforce org. A Salesforce org/data MCP server
is not treated as a documentation MCP server.

## Install the advisor

### Codex

Install this repository as a plugin. The plugin appears as **ISV/OEM Advisor**.
Then start a new session and invoke its entry skill:

```text
$oem-isv-advisor
```

### Claude Code

Add this repository as a marketplace and install the **ISV/OEM Advisor**
plugin using its technical identifier:

```text
/plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit
/plugin install oem-isv-advisor@partner-ecosystem-agentic-kit
```

Start a new session after installation.

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
