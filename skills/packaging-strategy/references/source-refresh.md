# Source refresh guide

Use this file when a recommendation depends on current Salesforce behavior.
Salesforce Docs MCP is the first read-only source and needs no per-call
approval. If a relevant page is not machine-readable through MCP, use the
approved rendered-document fallback and record that fallback. Never claim a
source was reviewed when it was inaccessible.

Refresh before stating current limits, eligibility, packageability, CLI flags,
Security Review policy, program tier, or product enablement.

## Required official sources

- [Components Available in Second-Generation Managed Packages](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/packaging_packageable_components.htm): verify the intended managed-2GP boundary by exact metadata type.
- [Metadata Coverage Report](https://developer.salesforce.com/docs/success/metadata-coverage-report/references/coverage-report/metadata-coverage-report.html): distinguish metadata availability from package-model support.
- [Create a Second-Generation Managed Package](https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/sfdx_dev_dev2gp_create_pkg_base.htm): refresh package-type and package-identity decisions before an Act handoff.
- [Specify Unpackaged Metadata or Apex Access for Apex Tests](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_unlocked_pkg_unpackaged_md.htm): refresh whether configured unpackaged metadata is intentionally available to package-version testing.
- [AgentExchange Publishing for Partners](https://trailhead.salesforce.com/content/learn/modules/appexchange-partners-publishing): refresh listing and distribution implications separately from package creation.
- [Package Named Credentials](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-package-credentials.md): verify which Named Credential definitions can be packaged.
- [Populate External Credential Principals](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-populate-external-credentials.md): verify subscriber-side principal population and authentication setup.
- [Test Credentials in the Target Org](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-test-credentials.md): verify target-org connectivity before release or upgrade claims.
- [Upgrade a Named Credentials Managed Package](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-upgrade-package.md): verify managed-upgrade behavior for packaged credential definitions.
- [Named Credentials Developer Guide for OAuth](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-oauth-dev-guide.md): refresh OAuth architecture and ownership boundaries.
- [Create an OAuth Named Credential](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-create-oauth-cred.md): verify supported creation and authorization flow.
- [Manage an OAuth Named Credential](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-manage-oauth-cred.md): verify post-install management responsibilities.
- [Update or Delete an OAuth Named Credential](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-update-delete-oauth-cred.md): verify lifecycle and upgrade-safe change paths.
- [Use the Named Credential in a Callout](https://developer.salesforce.com/docs/platform/named-credentials/guide/nc-use-oauth-cred-in-callout.md): verify the packaged callout integration pattern.

Record the selected package model, exact source consulted, access date, and
unresolved subscriber, entitlement, or distribution assumptions.
