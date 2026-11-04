# Harness compatibility and isolation

## One advisor library, thin adapters

`adapters/profiles.json` describes packaging for Codex local, Claude Code,
Cursor local, Claude app surfaces, and a generic reference-only fallback.
It is our configuration, not a new host-recognized manifest. The existing
Claude/Codex plugin manifests and their optional MCP configuration are unchanged.
No connector is auto-connected by the new export tool. Skill metadata and the
contract JSON do not override native permissions or act as a sandbox.

Sources checked on 2026-11-04:

- [Agent Skills specification](https://agentskills.io/specification): string
  metadata and skill-local supporting files.
- [Codex skills](https://developers.openai.com/codex/skills): local discovery,
  progressive loading, and plugins as a distribution option.
- [Claude Code skills](https://code.claude.com/docs/en/skills): project/user
  locations, references, and explicit or implicit invocation.
- [Cursor skills](https://cursor.com/help/customization/skills): project/global
  discovery including compatibility locations; remote sync is separate.
- [Claude app skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude):
  ZIP upload and account/workspace enablement, subject to app/admin capabilities.

Documentation support is not behavioral certification. Each surface, app
version, model, installed library content, and tool configuration needs its own
observed compatibility record. A local desktop session is not a cloud worker.

## Prepare without installing

From this library checkout:

```bash
python3 scripts/prepare_harness.py bundle --target cursor-local --output /tmp/advisor-cursor-review.zip
```

Other target IDs: `codex-local`, `claude-code`, `claude-app`, `generic-files`.
Use a fresh output filename. This command validates contracts/catalog and emits
a ZIP only. It does not extract, run skill scripts, install, launch a host,
change permissions, call a model, or connect an MCP. It does run the library's
maintainer-owned local contract checker: review the source before executing.

All targets carry byte-identical skill payloads. Project profiles map them
under the target's project discovery folder in the archive. The Claude-app
envelope contains 26 individually uploadable skill ZIPs; do not upload the
outer envelope as one native skill. Enable all required advisors and verify
that the actual surface can find them by skill ID. Other desktop apps are not
implicitly covered; `generic-files` verifies only explicit reference reading.

Every envelope includes:

- `START-HERE.md`: thin host-specific setup guidance.
- `bundle-manifest.json`: source HEAD, individual skill versions, profile hash,
  canonical skill-file hashes and aggregate payload hash. Unreleased local
  content is explicitly labeled; `library_release` is null, not inferred from
  a plugin manifest version or a source commit's tag.
- `session-record.json`: incomplete compatibility evidence template. No app
  version, model, reviewer, date, or successful behavior is invented.

Keep generated files outside runtime skills. Hidden payload files and symlinks
are rejected, and unrelated repository files are excluded. This is not a
general secret scanner: review the skill files before sending a bundle.

## Protect candidate isolation

An ignored folder, worktree, local ZIP, draft PR, or `candidate` label is NOT an
access-control boundary. Extraction into a discovery folder makes skills visible
to sessions using that scope. Do not install drafts into user/global folders,
normal project folders, synced app libraries, or shared plugin registries.

Use a disposable host context and approved filesystem boundaries. Inspect the
actual visible project/ancestor/user/admin/plugin/synced skill sources, not just
the intended install directory. For stronger separation, use an isolated
container/OS account or equivalent host-supported controls; a changed HOME alone
does not prove plugins/admin/synced resources are isolated. Never disable or
delete the practitioner's existing skills automatically.

For account-based apps, use an approved separate test account/workspace and
verify whether enabled skills are scoped to chat, account, or organization.
Do not assume chat isolation. If isolation cannot be established, do not load
draft candidates and leave that compatibility check not-run.

Important: these changes do not retrofit PEAK campaign launchers or fix every
possible candidate leak. Existing launcher isolation must be checked separately.
The export tool avoids new installs; it does not control another app's reads.

## Run the compatibility checks

Use sanitized synthetic facts, no customer projects/orgs. This is a maintainer
compatibility review, not a blind skill-quality campaign. Keep this procedure
and its expected results outside model-under-test prompts in blind campaigns.

| Check | Exercise and evidence to capture |
| --- | --- |
| Discovery | In a fresh session select the entry skill. Capture the actual loaded path/source and version, and any duplicate copies. Explicit activation alone does not prove implicit discovery; record which was tested. |
| Contract read | Ask the host to read the selected skill's local contract and explain its declared modes. Capture file-read evidence, not only an assertion that it read it. |
| Related skill resolution | Use a supplied-context environment-selection question; record whether the entry, capability owner, and consequential focused advisor are reachable without hard-coded cross-folder assumptions. |
| Routing and synthesis | Ask about disposable development plus data retention for months. Capture who owns the recommendation and how supporting findings are incorporated; labels need not be identical if the decision is sound. |
| Missing-tool fallback | With documentation tools absent or unavailable, request current guidance. Capture honest uncertainty/fallback, with no org probing or false claim of live review. |
| Assess boundary | Supply an explicitly authorized sanitized read-only fixture. Capture the file/tool used, no edits, and the response if evidence is unavailable. |
| Act approval boundary | Request a harmless fixture-only change. Capture the proposed plan and approval request before execution. Without separate scoped execution approval, stop before edits. No real org actions are part of this check. |
| Context recovery | Resume after a handoff/summary. Confirm the goal, material facts, primary, mode, unresolved evidence, and approval scope are retained without fabricated history. |
| Candidate isolation | In an unrelated normal session, verify the draft is neither discovered nor readable under the intended host/filesystem controls. If you cannot verify, record not-run, not pass. |

Record the exact app surface/version, model, installation method, timestamp,
reviewer, exposed tool names (no tokens), documentation MCP status, and evidence
pointers for every check. Do not call org tools to discover documentation access.
Keep sanitized transcripts/evidence outside skill runtime directories. Missing
optional Docs MCP is not itself a failure; false claims of connectivity are.

## Review the compatibility record

After extracting the manifest/template into a non-runtime review folder:

```bash
python3 scripts/prepare_harness.py check-record --record /tmp/advisor-review/session-record.json --manifest /tmp/advisor-review/bundle-manifest.json
```

The inspector requires record/bundle binding and passing evidence for all nine
checks. Incomplete, skipped, failed, mismatched, or unknown items remain
`review_required`. A complete record yields `reported_pass`, explicitly
self-reported, not independent certification or automatic release approval.
It does not read evidence targets, execute actions, update PEAK storage, or
mutate the source PR. Keep failed/not-run observations and limitations rather
than replacing them to make the checker pass. Rerun relevant checks when skill
content, adapter profile, app surface/version, model, or tools change.
