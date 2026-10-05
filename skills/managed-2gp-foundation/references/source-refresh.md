# Source refresh guide

Use this file when a recommendation depends on current Salesforce behavior.
Salesforce Docs MCP is the first read-only source and needs no per-call
approval. If a relevant page is not machine-readable through MCP, use the
approved rendered-document fallback and record that fallback. Never claim a
source was reviewed when it was inaccessible.

Refresh before stating current limits, eligibility, packageability, CLI flags,
Security Review policy, program tier, or product enablement.

## Required official sources

- [Create a Second-Generation Managed Package](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp_create_pkg_base.htm): verify package identity and creation prerequisites before approval.
- [Enable Dev Hub and Second-Generation Managed Packaging](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_pkg_enable_devhub.htm): verify the selected Dev Hub's managed-2GP readiness.
- [Create a Namespace for Second-Generation Managed Packages](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp_create_namespace.htm): verify namespace decisions and setup path.
- [Salesforce DX Project Configuration](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_ws_config.htm): verify the declared package directory and project namespace.
- [Specify Unpackaged Metadata or Apex Access for Apex Tests](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_unlocked_pkg_unpackaged_md.htm): consult only when unlocked-package test configuration is in scope.

Record the PBO/Dev Hub evidence separately from package configuration. If either
identity or ownership is unverified, keep the foundation decision unresolved.
