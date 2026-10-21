# Headless and MCP decision guide

Read with the skill's source-refresh guide. The MCP In/Out names below are the
partner's working vocabulary, not a claim that Salesforce's docs define those
terms. Always describe the roles and direction explicitly.

## Start with the client/server map

| Partner label | MCP client and engagement layer | MCP server and tool owner | Direction of the protocol call | Primary choice |
|---|---|---|---|---|
| MCP In | Agentforce agent in Salesforce | Partner's externally hosted MCP server | Agentforce → external server | Register external server in Agentforce Registry; activate selected tools |
| MCP Out | Slackbot, Claude, or ChatGPT outside the Salesforce UI | Salesforce hosted standard or custom MCP server | External client → Salesforce server | Enable standard server or configure custom server and connect client |

An Agentforce agent can also be *exposed* as a tool on a Salesforce hosted
custom server. In that case the external assistant is the MCP client and the
Agentforce agent is the Salesforce-side backing capability: classify it as MCP
Out under the partner vocabulary. Do not infer direction from where Apex code
or data is stored. If a partner uses the labels differently, use their terms
but retain the concrete map.

Headless Toolkit also includes APIs, Salesforce CLI, plugins, and skills. If
the partner wants a builder workflow, assess those development tools. If an
ordinary application needs Salesforce functionality without an AI MCP client,
assess a direct API. Reserve a hosted or external MCP server for an actual MCP
client and tool workflow.

Keep the builder harness separate from the runtime client. Claude Code,
Agentforce Vibes, and Builder Central are development environments; an
Agentforce agent, Slackbot, Claude, or ChatGPT can be the runtime engagement
layer. Ask which Agentforce surface the partner means before assigning an MCP
direction or client-connection path.

Ask only for information that changes the choice:

1. What is the user trying to do, and in which client: Agentforce, Slackbot,
   Claude, ChatGPT, or another surface? Which product/version and channel?
2. Who hosts the MCP endpoint? Is the partner bringing an external server into
   Agentforce, or making Salesforce capabilities available to an external client?
3. Which tools already exist, and who owns them: standard server, packaged
   Apex, Flow, Agentforce agent, Prompt Template, Apex REST, `@AuraEnabled`,
   API Catalog endpoint, or partner service?
4. Does the use case need a read, write, delete, multi-step transaction, or
   reasoning? Which identity, data scope, and permissions govern the call?
5. Is this a managed product? Who installs the package, registers or enables
   the server, connects the client, and maintains the tool descriptions?
6. Is a rich widget needed, or is structured text/JSON sufficient? If rich,
   which output schema and target channels must be rendered?

## Choose the external or Salesforce hosted tool source

For an existing external MCP server used by an Agentforce agent, start with
its documented endpoint and transport, then verify that Salesforce can list
and call its tools. Register the server in Agentforce Registry with the
authentication method the server actually supports; do not assume OAuth is
required when the provider documents no authentication. Review discovered
tool names, descriptions, and data scope before activating only the tools the
agent needs. Then add the resulting MCP tool actions to the intended agent and
test a real request. For managed distribution, the external server registration
can be packaged through `ExternalCredential`, `ExternalServiceRegistration`,
`NamedCredential`, and `PermissionSet` metadata, subject to current platform
and package-version validation. MCP tool actions and Agentforce Gateway
policies remain subscriber setup. Record the endpoint owner, data sent in tool
arguments, and the effect of remote tool-output changes; route security review
to `security-readiness`. See the [Agentforce external MCP registration packaging
guide](https://developer.salesforce.com/docs/platform/pkg2-dev/guide/dev2gp-package-mcp-agentforce.html)
and [external server management example](https://developer.salesforce.com/docs/platform/api-catalog-connectapi/guide/manage-external-mcp-servers.html).
Ask whether the partner needs one customer-org connection or an AgentExchange
distribution. For a listing, route package and listing decisions to
`packaging-distribution`: Salesforce's [Partner Console guidance](https://help.salesforce.com/s/articleView?id=release-notes.rn_list_and_publish_mcp_servers_in_agentforce_extension_packages.htm&language=en_US&release=262&type=5)
describes listing MCP servers and their tools with an Agentforce extension
package. Route review readiness to `security-readiness` and verify current
publishing requirements before recommending release.

If the external server already supplies the required tools, assess a
Salesforce hosted custom server, Apex Action, or HXL widget only for a separate
Salesforce-side capability or supported rich-output need.

- Check the [standard server reference](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/servers-reference.html)
  and [Headless MCP solutions](https://developer.salesforce.com/docs/platform/headless-get-started/guide/headless-mcp.html)
  for an existing scoped tool. Standard server tool sets are fixed and enabled
  by an admin; availability, product entitlement, Beta status, and client
  support must be refreshed per server. Current examples include SObject Reads,
  Mutations, Deletes, and All; Data 360; Headless 360 (Beta); Content; and
  Tableau Next. The broader MCP Solutions catalog also covers Salesforce DX
  and product-specific servers such as Heroku and MuleSoft; do not assume all
  share the same org authentication or client support. Prefer a narrow read or
  mutation server over a broad server when it satisfies the job.
- Choose a [custom Salesforce hosted server](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/custom-servers.html)
  to curate tools for one persona or expose custom capabilities. The documented
  backing choices include Apex Invocable Actions, autolaunched Flows,
  `@AuraEnabled` methods, Apex REST, and supported API Catalog endpoints.
  Agentforce agents built with the current Agent Script Builder and Prompt
  Templates can also be exposed; check their separate requirements. Give each
  tool a specific name and description so the client can choose it.
- Select an [Apex Action](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/invocable-actions.html)
  when logic requires server-side validation, orchestration, or integration.
  For this MCP backing type, Salesforce currently requires a `global`
  `@InvocableMethod`. Its invocable input and output variables define the
  tool contract. Preserve list-oriented invocable signatures and bulk behavior;
  refresh the Apex annotation rules before authoring. Existing admin-owned
  declarative logic may fit an autolaunched Flow better.
- For managed delivery, package the supported Apex/Flow assets and let the
  subscriber admin configure the Salesforce hosted custom server. The current
  [custom server guide](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/custom-servers.html)
  says the hosted MCP server configuration itself cannot yet be included in an
  ISV managed package. This is distinct from a packageable *external server
  registration* for Agentforce MCP In.
- For an external Claude or ChatGPT client connecting to a Salesforce hosted
  server, check the [client connection guide](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/client-connection-overview.html)
  for the current External Client App, OAuth, server URL, and client setup.
  A Connected App is not the documented MCP authentication mechanism. Use
  `channel-rollout.md` for the distinct Slackbot connection path and for
  channel-by-channel validation.
- For MCP In, check the [Agentforce external MCP registration packaging guide](https://developer.salesforce.com/docs/platform/pkg2-dev/guide/dev2gp-package-mcp-agentforce.html).
  It lists ExternalCredential, ExternalServiceRegistration, NamedCredential,
  and PermissionSet as packageable metadata, while MCP tool actions and
  Agentforce Gateway policies are not. Plan subscriber authentication,
  activation, and tool selection separately.

## Apex and rich output

- A global invocable method is required for the current Salesforce hosted MCP
  Apex Action backing. For an Agentforce action supplied by a managed package,
  the indexed excerpt of Salesforce's [Apex Developer Guide](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_apex_developer_guide.pdf)
  additionally calls for the containing class, global static invocable method,
  input/output wrapper classes, their `@InvocableVariable` fields, and custom
  data types in those wrappers to be global. Keep the global entry point thin
  because managed global APIs are hard to change. Review namespace, Apex class
  access, sharing, CRUD/FLS, governor limits, and returned data. Recheck the
  current guide before treating the Agentforce and hosted MCP requirements as
  identical.
- `@JsonAccess(serializable='always' deserializable='always')` is specifically
  documented for Apex classes used by [Apex-based custom Lightning types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-apex.html)
  in Agentforce, along with top-level global classes and `@AuraEnabled` fields.
  Do not present it as a blanket prerequisite for every MCP Apex Action. Check
  the exact serialization and rendering path.
- [HXL widgets](https://developer.salesforce.com/docs/platform/hxl/guide/hxl-rich-ui.html)
  are documented for Agentforce Employee agent in Lightning Experience and
  MCP channels in Slackbot, Claude, and ChatGPT. A widget bundle has a required
  JSON composition and `.uiwidget-meta.xml`; `schema.json` is optional for
  static content but required for dynamic attribute mapping. Check available
  [components](https://developer.salesforce.com/docs/platform/hxl/guide/playground-components.html)
  and preview in the [Playground](https://developer.salesforce.com/docs/platform/hxl/guide/playground.html).
- For Agentforce action output, the documented HXL path uses an Apex-based
  custom Lightning type and direct widget attribute mapping. For an Apex
  invocable action exposed as a Salesforce hosted MCP tool, it uses two
  object-based custom Lightning types: a result wrapper and a payload type.
  The wrapper maps nested `outputValues` into the widget's flat attributes.
  Route these to the two distinct global coordinator skills in the main skill.
- For an HXL widget on an MCP channel, [Setup creates/selects the custom server and adds the Apex action](https://developer.salesforce.com/docs/platform/hxl/guide/hxl-mcp-server.html).
  Current documentation then requires retrieving its metadata, adding a
  widget resource and matching tool `uiResource`, deploying it, and activating
  the server. Setup alone does not yet configure the HXL resource.

For a partner Salesforce DX project assessment, use `sfdx-assessment.md` to
inventory source paths, verify the 2GP boundary, and identify what the customer
must configure after installing the package. Salesforce currently marks
`ApexClass`, `LightningTypeBundle`, and `UiWidgetBundle` for 2GP, but not
`McpServerDefinition`; source presence is not proof of package inclusion.

## Partner readout

State the partner goal; MCP In/Out label plus concrete client → server → tool
path; standard versus custom/external server choice; reused versus new backing
logic; identity and permissions; package versus subscriber setup ownership;
observed SFDX paths and package boundary when assessed; whether HXL is needed
and its channel-specific path; evidence labels and
sources; unknowns; and the approved global skill handoff. Preserve a conflict
when live org evidence differs from this source snapshot.
