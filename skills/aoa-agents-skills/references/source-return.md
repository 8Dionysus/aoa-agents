# Owner source return

Resolve the canonical `aoa-agents` owner after applicability is established and
before reading role, specialization, tier, capability, or operating-model
sources. This gate locates authored meaning; it does not prove runtime health,
installed parity, model fit, or execution.

## Gate

1. Use the `<bundle_dir>` recorded from the loaded `SKILL.md`.
2. In one tool turn containing no other read or command, read exactly
   `<bundle_dir>/.aoa-skill-source.json`.
3. When it exists, require:
   - schema `aoa_skill_source_receipt_v1` or
     `aoa_skill_source_receipt_v2`;
   - bundle and source name `aoa-agents-skills`;
   - owner `aoa-agents`;
   - version `0.4.0`;
   - an existing absolute `owner_root` and safe relative `source_path`;
   - `<owner_root>/<source_path>/SKILL.md`;
   - for v2, non-empty `digest`, `source_fingerprint`,
     `source_fingerprint_scope`, and `prompt_description_sha256`; preserve a
     non-empty `capability_graph_hash` when present.
4. An invalid or mismatched existing handle is terminal:
   `blocked_missing_owner_source`. Do not try another checkout.
5. Only when the exact handle does not exist, run
   `git -C <bundle_dir> rev-parse --show-toplevel` once and use that root.
6. In the next isolated tool turn, read only
   `<owner_root>/skills/port.manifest.json`. Require owner `aoa-agents`, bundle
   `aoa-agents-skills`, version `0.4.0`, and the exact bundle path. A manifest
   read batched with an owner document terminates
   `blocked_owner_source_gate_not_observed`.
7. Only after manifest success may a later tool turn read the exact owner
   sources required by the selected mode.

Never use parent traversal, sibling scans, `find`, `rg --files`, repository-wide
search, workspace conventions, `.system`, another skill directory, or a
temporary fixture to discover a substitute owner. Handle digests, commit refs,
dirty posture, source fingerprints, capability graph hashes, and prompt hashes
are install provenance, not source authority or currentness proof.

## Bounded owner routes

| Mode | First owner sources |
| --- | --- |
| `role-first-entry` | `AGENTS.md`, `CHARTER.md`, `agents/README.md`, and `agents/operating-model/README.md`; then the exact `agents/roles/README.md` and one bounded finite candidate-source read over `agents/roles/*/profile.json` plus `agents/roles/*/specializations/*/specialization.json`; after semantic selection, read only the exact role/specialization sources and each stronger-owner contract through its own gate |
| `detect-obligation` | `AGENTS.md`, `CHARTER.md`, `agents/README.md`, and `agents/operating-model/README.md` |
| `form-actor` | `agents/roles/README.md`, then only the exact supplied role, specialization, tier, and capability-pack refs |
| `bind-incarnation` | exact supplied mandate refs, then the declared `aoa-models`, `aoa-sdk`, and `abyss-stack` contracts through their own owner gates |
| `transfer-responsibility` | exact supplied mandate/incarnation refs and the selected execution leaf contract |
| `receive-return` | exact supplied mandate, transfer, runtime-event, output, and return-owner refs |

Do not broaden from a missing exact role or owner ref into repository
archaeology. Return the missing input and the stronger owner route.

## Receipt

Report the source route, owner root, source handle identity or git action,
manifest action, first owner-source action, selected mode, stronger-owner roots
resolved separately, and skipped checks.
