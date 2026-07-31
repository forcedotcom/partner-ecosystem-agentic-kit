# Salesforce Partner Ecosystem Agentic Kit

Portable Salesforce OEM/ISV advisory skills for Codex, Claude Code, and other
compatible harnesses.

This repository is the production destination for human-reviewed skills. Skill
development and evaluation occur locally before a pull request is opened here.

## Current entry points

- `oem-isv-advisor` preserves the partner goal and routes the decision.
- `advisor-capability-preflight` checks Salesforce documentation capability,
  obtains customer consent, and selects an honest fallback.

The preflight never probes a Salesforce org. A Salesforce org/data MCP server
is not treated as a documentation MCP server.

## Install for local testing

### Codex

Install this repository as a local plugin or copy the skill folders into a
Codex-supported skills location. Then start a new session and invoke:

```text
$oem-isv-advisor
```

### Claude Code

Add this repository as a marketplace and install its plugin:

```text
/plugin marketplace add forcedotcom/partner-ecosystem-agentic-kit
/plugin install oem-isv-advisor@partner-ecosystem-agentic-kit
```

Start a new session after installation.

## Documentation setup behavior

On first use, the advisor checks the tools exposed by the harness:

1. If Salesforce Docs MCP is connected, it is preferred.
2. If a verified MCP installation is offered by the harness, the advisor asks
   before installing or connecting it.
3. If no verified installation source is available, the advisor offers exact,
   read-only Salesforce documentation domains as fallback.
4. If the customer declines or enterprise policy blocks access, the advisor
   continues with packaged knowledge and labels unsupported current claims as
   unknown.

Customer consent never bypasses host or enterprise security policy. The
repository intentionally contains no guessed Salesforce Docs MCP endpoint.
When Salesforce publishes or administrators provide a verified server identity,
add it to the preflight policy and dependency metadata through normal review.

## Validate

```bash
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py skills/oem-isv-advisor
python3 /path/to/skill-creator/scripts/quick_validate.py skills/advisor-capability-preflight
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the normal human review process.

