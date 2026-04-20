# Agon Wave II Seed: Assistant Civil Rechartering

Target repository: `aoa-agents`

This seed lands the second Agon imposition wave for the agent layer.

Wave 0 made the current system subject to Agon.
Wave I rechartered current role-bearing actors into agonic-ready forms.
Wave II recharters the civil/service pole: assistant actors that must stay transparent, predictable, externally revised, receipt-bearing, and excluded from contestant authority unless a later explicit owner-reviewed recharter creates a different form.

## What this seed adds

```text
docs/
  ASSISTANT_CIVIL_RECHARTERING.md
  ASSISTANT_KIND_MODEL.md
  ASSISTANT_SERVICE_IDENTITY_MODEL.md
  ASSISTANT_SERVICE_CONTRACT_MODEL.md
  ASSISTANT_SERVICE_GOVERNANCE_MODEL.md
  ASSISTANT_SERVICE_CERTIFICATION_MODEL.md
  ASSISTANT_ARENA_EXCLUSION_MODEL.md
  ASSISTANT_ESCALATION_TO_AGON.md
  AGON_WAVE2_LANDING.md

schemas/
  assistant_variant_v1.json
  assistant_service_identity_v1.json
  assistant_service_contract_v1.json
  assistant_service_governance_v1.json
  assistant_service_certification_v1.json
  assistant_arena_exclusion_v1.json

profiles/adjuncts/
  assistant_variant/
  assistant_service_identity/
  assistant_service_contract/
  assistant_service_governance/
  assistant_service_certification/
  assistant_arena_exclusion/

generated/
  assistant_civil_formation_index.min.json

scripts/
  build_assistant_civil_formation_index.py
  validate_assistant_civil_formation.py

tests/
  test_assistant_civil_formation.py

examples/
  assistant_civil_formation.example.json

quests/
  AOA-AG-Q-AGON-0004-assistant-civil-recharter.md
  AOA-AG-Q-AGON-0005-assistant-formation-index-integration.md
  AOA-AG-Q-AGON-0006-assistant-projection-boundary.md
```

## What this seed does not do

It does not change:

```text
schemas/agent-profile.schema.json
profiles/*.profile.json
generated/agent_registry.min.json
generated/codex_agents/
runtime_seam/
```

It does not define:

```text
arena sessions
sealed commits
lawful moves
verdict logic
scar storage
retention checks
runtime packets
ToS promotion
```

Those belong to later center-owned Agon protocol work and other owner repositories.

## Merge posture

Copy the contents of `repo/` into the root of `aoa-agents`.

Then run:

```bash
python scripts/build_assistant_civil_formation_index.py --check
python scripts/validate_assistant_civil_formation.py
python -m pytest -q tests/test_assistant_civil_formation.py
```

The validator expects the five current base profiles to exist:

```text
profiles/architect.profile.json
profiles/coder.profile.json
profiles/reviewer.profile.json
profiles/evaluator.profile.json
profiles/memory-keeper.profile.json
```

## Core invariant

Assistant actors are not weaker warriors.
They are a separate civil/service form.

They may support arena infrastructure later as notaries, monitors, stewards, couriers, librarians, or other service seats, but they must not silently become contestants, judges, closers, summoners, scar writers, or canonical interpreters.
