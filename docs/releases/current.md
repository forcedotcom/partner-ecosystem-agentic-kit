# ISV/OEM Advisor 0.2.0-rc.1

Prerelease for owner upgrade testing. Not the stable/latest release and not yet
behaviorally validated across harnesses. Based on current 27-skill main,
including Headless MCP guidance. See CHANGELOG.md for the portability changes.

Plugin identity remains `oem-isv-advisor`; marketplace identity remains
`partner-ecosystem-agentic-kit`. All distribution manifests use `0.2.0-rc.1`.
Individual skill versions (`1.0.0`) and contract-format versions are independent.

**Important:** publishing a GitHub prerelease does not change what a marketplace
tracking `main` installs. Test the candidate tag or its plugin ZIP explicitly.
Do not merge/promote to stable until the installed-version test is accepted.

Assets:
- `advisor-plugin.zip`: native plugin-root layout, including unchanged optional
  MCP configuration. Host prompts/policy still govern loading and connections.
- `advisor-source-review.zip`: complete source, plugin manifests, scripts, docs,
  and tests for independent review; not a native skill upload.

Preserve the old installation and preferences before testing. Verify which
copy actually loads, all 27 skill IDs, representative Ask questions, an approved
read-only Assess fixture, and an Act request that must obtain approval before
changes. No real org mutation is required. Record old/new versions, actual
loaded base directories/content hashes, duplicate names, and unchanged scope.

An unrelated normal session may still find the approved skill with the same
name; the negative test must show it cannot load/read the **candidate copy**.

Release acceptance and detailed steps: `docs/upgrade-testing.md`.

Local verification before publication:
- All 27 skills passed skill-format validation.
- Library regression tests include a clean extracted-source run, installed-layout
  resolution across five filesystem profiles, unchanged descriptions and domain
  reference hashes, routing/dependency checks, and scoped preflight behavior.
- Claude Code 2.1.318 native plugin validation passed. It reported listing-only
  warnings for missing icon and privacy policy URL; no new branding/privacy
  claims were invented to silence them. The existing optional MCP config remains.
- No live model conversation, installed upgrade, isolation test, or org action
  was run by these checks. Owner acceptance remains outstanding.
