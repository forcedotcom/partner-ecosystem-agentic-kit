# Source refresh guide

Use this file when a recommendation depends on current Salesforce behavior.
Salesforce Docs MCP is the first read-only source and needs no per-call
approval. If a relevant page is not machine-readable through MCP, use the
approved rendered-document fallback and record that fallback. Never claim a
source was reviewed when it was inaccessible.

Refresh before stating current limits, eligibility, packageability, CLI flags,
Security Review policy, program tier, or product enablement.

## Required official sources

- [Move to 2GP: Migrate Your Managed Packages with Ease](https://developer.salesforce.com/docs/atlas.en-us.pkg1_dev.meta/pkg1_dev/move_to_second_gen_pkg.htm): verify managed-1GP conversion and subscriber-migration eligibility.
- [Managed 2GP with Package Migrations Is Now Generally Available](https://developer.salesforce.com/blogs/2025/06/move-to-managed-2gp-with-package-migrations): refresh current migration context before proposing a program.
- [Transfer a Second-Generation Managed Package to a Different Dev Hub](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev2gp_package_transfer.htm): verify transfer eligibility, preparation, and Support-assisted steps.
- [Transfer an Unlocked Package to a Different Dev Hub](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_unlocked_package_transfer.htm): verify the separate unlocked-package transfer path and its current prerequisites.
- [Salesforce DX Project Configuration](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_ws_config.htm): verify source-project changes and dependency references after a transfer or migration.

Record the package model, conversion history, and exact subscriber/dependency
state. For managed 2GP, record Security Review status; for unlocked packages,
record the separate transfer prerequisites instead of treating Security Review
as a gate. Also record source access date and any Support-owned step.
Do not infer transfer or conversion eligibility from a package identifier.
