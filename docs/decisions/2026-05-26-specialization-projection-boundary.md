# 2026-05-26: Specialization Projection Boundary

## Status

Accepted.

## Context

`aoa-agents` now has two adjacent agent-layer surfaces:

- base role profiles under `agents/roles/<role>/profile.json`;
- role-local specializations under
  `agents/roles/<role>/specializations/<slug>/specialization.json`.

The Codex custom-agent projection existed before the specialization layer and
publishes install companions under `generated/codex_agents/`.
Without an explicit boundary, future changes could silently turn every
`role.specialization` source record into a `.codex/agents/` install entry.
That would blur role identity, permission posture, tool posture, and refresh
law before the repo has a reviewed promotion contract for specialized Codex
agents.

The external agent-building guidance we are following favors clear operational
maps: role, input, output, owner, route, tool posture, and validation. Here the
clean map is to keep role source, specialization catalog, and install projection
separate until a promotion gate exists.

## Decision

Keep `generated/codex_agents/` base-role-only.

The active projection scope is:

```text
base_role_profiles_only
```

Codex subagent projection consumes:

- `agents/roles/*/profile.json`;
- `mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json`.

It does not consume:

- `agents/roles/*/specializations/*/specialization.json`;
- `generated/role_specialization_catalog.min.json`;
- `generated/capability_pack_registry.min.json`.

Role specializations remain source-layer actor contracts and publish through
`generated/role_specialization_catalog.min.json`. A specialization may become a
Codex custom agent later only after a separate projection eligibility surface
names its install identity, permission posture, refresh law, and owner consent.

## Consequences

- `architect`, `coder`, `reviewer`, `evaluator`, and `memory-keeper` remain the
  current Codex custom-agent install units.
- `coder.repo-refactor`, `reviewer.route-drift-review`, and similar records are
  available to catalogs, planners, and future promotion work without multiplying
  installed agents today.
- Capability packs may contain projection hints, but those hints do not grant
  install authority.
- The projection manifest now declares `projection_scope:
  base_role_profiles_only`.
- Validators reject manifest entries that look like `role.specialization` names
  or point at specialization source paths.

## Verification

The intended verification route is:

```bash
python mechanics/codex-projection/parts/subagent-projection/scripts/build_codex_subagents_v2.py --check
python mechanics/codex-projection/parts/subagent-projection/scripts/validate_codex_subagents.py --profiles-root agents/roles --wiring mechanics/codex-projection/parts/subagent-projection/config/wiring.v2.json --agents-dir generated/codex_agents/agents --config-snippet generated/codex_agents/config.subagents.generated.toml --manifest generated/codex_agents/projection_manifest.json
python -m unittest discover -s mechanics/codex-projection/parts/subagent-projection/tests -p "test_*.py"
python scripts/validate_agents.py
```
