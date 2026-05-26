# 2026-05-26: Mechanics Config Localization

## Status

Accepted.

## Context

The docs localization moved mechanics-facing public docs into
`mechanics/<mechanic>/parts/<part>/docs/`, but the active seed and wiring
payloads for Agon, recurrence, Codex projection, and Titan still lived in root
`config/`. That kept executable source inputs far away from the mechanic parts
that explain and validate them.

Root `config/` is still useful for repository-level publication or policy
configuration, but these files were not generic repository config. They were
mechanic-specific seeds with existing builders, validators, manifests, tests,
and generated readers.

## Decision

Move mechanic-specific config payloads from root `config/` into active
part-local routes:

```text
mechanics/<mechanic>/parts/<part>/config/
```

Use part-local names that do not repeat the former root prefix. Preserve the
old root paths only as lookup facts in the target package `PROVENANCE.md`,
`legacy/INDEX.md`, and `legacy/DISTILLATION_LOG.md`.

Keep root `config/AGENTS.md` as a route card for future repository-level
config, not as the active home for Agon, recurrence, Codex projection, or
Titan mechanic seeds.

## Consequences

- Agon rank/school/epistemic seeds live with their Agon parts.
- Recursor readiness and Codex recursor projection configs live with recurrence
  parts.
- Codex subagent wiring lives with the Codex projection part it drives.
- Titan role classes, bearers, and lineage ledger live with Titan parts.
- Builders, validators, manifests, schemas, examples, tests, and generated
  source references must use the new active paths.
- Shared schemas, examples, scripts, tests, generated readers, manifests, quest
  files, and agent source objects remain in their current districts until their
  own package-local move proof exists.

## Verification

Run the affected builders/validators plus the repo topology checks:

```bash
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_rank_jurisdiction_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_rank_jurisdiction.py
python mechanics/agon/parts/arena-rank-school/scripts/build_agon_agent_school_campaign_posture_registry.py --check
python mechanics/agon/parts/arena-rank-school/scripts/validate_agon_agent_school_campaign_posture_registry.py
python mechanics/agon/parts/epistemic-actor/scripts/build_agon_epistemic_actor_posture_registry.py --check
python mechanics/agon/parts/epistemic-actor/scripts/validate_agon_epistemic_actor_posture.py
python mechanics/recurrence/scripts/build_recursor_role_readiness.py --check
python mechanics/recurrence/scripts/build_recursor_projection_candidates.py --check
python mechanics/recurrence/scripts/validate_recursor_role_readiness.py
python mechanics/recurrence/scripts/validate_recursor_boundary.py
python scripts/validate_codex_subagents.py --profiles-root agents/profiles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
python mechanics/titan/scripts/validate_titan_lineage.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --ledger mechanics/titan/parts/lineage-ledger/config/ledger.v0.json
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/validate_agents.py
python -m pytest -q tests
```
