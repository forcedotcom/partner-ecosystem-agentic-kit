# Source refresh guide

Read this reference before stating a Salesforce feature, setting, allocation,
edition, entitlement, API-version, or CLI claim as current.

## Current-source path

1. Run `$advisor-capability-preflight`.
2. Prefer Salesforce Docs MCP when connected; otherwise use approved official
   Salesforce documentation read-only.
3. Verify the exact value against the relevant source:
   - [Scratch Org Features catalog](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_scratch_orgs_def_file_config_values.htm)
   - [Metadata API Settings catalog](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_settings.htm)
   - [Supported Scratch Org Editions and Allocations](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_scratch_orgs_editions_and_allocations.htm)
4. For a setting, open the selected setting's specific setting reference and
   its field documentation before naming nested JSON fields or values.
5. Check the partner's selected edition, PBO/Dev Hub entitlement, and relevant
   API/release context before presenting a current recommendation.

## Evidence rule

Record the source identity and label the result as fact, practitioner
knowledge, inference, recommendation, assumption, or unknown. If the required
source is unavailable, label the exact value as **unknown** rather than
inferring it from a template or prior release.
