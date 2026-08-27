# Source refresh guide

Use this file when a recommendation depends on current Salesforce behavior.
Salesforce Docs MCP is the first read-only source and needs no per-call
approval. If a relevant page is not machine-readable through MCP, use the
approved rendered-document fallback and record that fallback. Never claim a
source was reviewed when it was inaccessible.

Refresh before stating current limits, eligibility, packageability, CLI flags,
Security Review policy, program tier, or product enablement.

## Required official sources

- [Create Versions of a Second-Generation Managed Package](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp_create_pkg_ver.htm): verify ancestry and dependency behavior for the selected package model.
- [Salesforce CLI Package Version Create Reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_package_version_create.html): verify current version-selector and dependency flags.
- [Recommend a Specific Package Version](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp_recommended_version.htm): distinguish recommendation lineage from release and ancestry decisions.

Record the exact ancestor, dependency selectors, local alias resolution, and
source access date. Treat an unresolved selector as an unknown, not proof that
the dependency is absent or valid.
