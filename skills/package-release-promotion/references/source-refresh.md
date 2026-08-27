# Source refresh guide

Use this file when a recommendation depends on current Salesforce behavior.
Salesforce Docs MCP is the first read-only source and needs no per-call
approval. If a relevant page is not machine-readable through MCP, use the
approved rendered-document fallback and record that fallback. Never claim a
source was reviewed when it was inaccessible.

Refresh before stating current limits, eligibility, packageability, CLI flags,
Security Review policy, program tier, or product enablement.

## Required official sources

- [Release a Second-Generation Managed Package](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp_create_pkg_ver_promote.htm): verify current promotion prerequisites and irreversible effects.
- [Salesforce CLI Package Version Promote Reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_package_version_promote.html): verify the exact promotion command and flags before execution.
- [Recommend a Specific Package Version](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp_recommended_version.htm): keep recommendation state separate from promotion.

Record the exact `04t`, terminal validation evidence, approved release policy,
promotion result, and access date. Do not substitute a generic package name or
a successful command submission for post-promotion proof.
