# Source refresh guide

Use this file when a recommendation depends on current Salesforce behavior.
Salesforce Docs MCP is the first read-only source and needs no per-call
approval. If a relevant page is not machine-readable through MCP, use the
approved rendered-document fallback and record that fallback. Never claim a
source was reviewed when it was inaccessible.

Refresh before stating current limits, eligibility, packageability, CLI flags,
Security Review policy, program tier, or product enablement.

## Required official sources

- [Create Versions of a Second-Generation Managed Package](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp_create_pkg_ver.htm): refresh version-create prerequisites and validation behavior.
- [Salesforce CLI Package Version Create Reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_package_version_create.html): verify the exact current flags before an Act handoff.
- [How Scratch Orgs Fit in the Package Development Workflow](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/dev2gp_so_how_fit_pkg_dev.htm): verify build-org shape expectations.
- [Components Available in Second-Generation Managed Packages](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/packaging_packageable_components.htm): resolve component-support blockers separately from build configuration.

Record the package/version identity, definition-file result, validation mode,
coverage result, terminal request state, and source access date. A submitted
request is not evidence of a successful candidate.
