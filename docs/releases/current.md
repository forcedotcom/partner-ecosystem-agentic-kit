# ISV/OEM Advisor 0.2.0 — Beta

This release promotes the tested `0.2.0-rc.1` metadata/portability candidate.
Beta is the product-maturity label. The library/plugin version is `0.2.0`;
individual skill versions remain `1.0.0`, and each skill retains its declared
maturity. This is not a claim that every skill or harness is fully validated.

## Included

- Portable metadata and versioned contracts for all 27 current skills.
- ID-based routing, conditional Ask dependencies, and thin harness exports.
- Scoped documentation preferences and no unnecessary web-consent prompt when
  documentation tools are exposed.
- Versioned plugin/source-review assets and release consistency checks.

Plugin identity remains `oem-isv-advisor`; marketplace identity remains
`partner-ecosystem-agentic-kit`. This promotion changes release versions and
documentation, not the candidate's advisor instructions or domain references.
The proposed invocation-time update reminder is not included.

## Validation and limitations

See [the validation summary](https://github.com/forcedotcom/partner-ecosystem-agentic-kit/blob/v0.2.0/docs/releases/0.2.0-validation.md). The maintainer-supervised
Claude Code comparison completed seven identical prompts before and after,
including approved read-only evidence inspection, a separately human-approved
one-field synthetic edit, and return to Ask. Native update and content hashes
were checked. User-supplied plugin screenshots separately showed a GitHub-backed
project installation move from `0.1.0` to `0.2.0-rc.1` and remain enabled.

Library tests cover all contracts, unchanged descriptions/domain-reference
guards, source-independent extracted layouts and release-version consistency.
Other live harnesses, real-org actions and full filesystem isolation are not
certified by these checks. Documentation conflicts remain qualified unknowns.

## Update existing installations

After merge, main-tracking Claude Code users can open `/plugin` → **Marketplaces**
→ **partner-ecosystem-agentic-kit** → **Update marketplace**. If pending, open
**Installed** → **ISV/OEM Advisor** → **Update now**. Start a fresh session and
confirm `0.2.0`. Auto-update is an optional user/admin setting, not something
this release silently enables. A GitHub Release alone does not change the
source branch a user follows.

Candidate-branch testers must explicitly return their marketplace source to
`main` to follow normal releases. Standalone copied-skill installations require
their existing copy/install procedure and source-lock update; plugin commands
do not update those copies. Preserve local edits, other libraries and backups.

## Assets

- `advisor-plugin.zip`: native plugin-root payload and manifests, retaining
  existing optional documentation MCP configuration and host prompts.
- `advisor-source-review.zip`: complete source, manifests, checks and tests;
  not a native single-skill upload.

No PEAK console code, private captures, credentials or customer data is included.
