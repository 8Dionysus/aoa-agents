# agents/operating-model/AGENTS.md

## Purpose

`agents/operating-model/` is the cross-role operating branch for `aoa-agents`.
It holds compact source contracts that shape how role houses are tiered,
specialized, orchestrated, grouped, and bound to runtime-seam phases.

It is not a runtime implementation home and not a playbook or routing policy
owner.

## Source of truth

Canonical authoring lives in:

- `agents/operating-model/tiers/*.tier.json`
- `agents/operating-model/capabilities/packs/*.capability.json`
- `agents/operating-model/orchestrators/*.class.json`
- `agents/operating-model/cohorts/*.pattern.json`
- `agents/operating-model/runtime-seams/*.binding.json`
- `agents/source_home.manifest.json`

Published derived surfaces live under `generated/` and must be rebuilt from
the source objects.

## Editing posture

Use the nearest child `AGENTS.md` before editing a concrete family. Keep the
branch convex:

- tiers describe effort and handoff posture;
- capabilities describe reusable permission, tool, skill, technique, memory,
  proof, and projection posture;
- orchestrators describe class identity and boundaries;
- cohorts describe bounded role grouping hints;
- runtime seams bind phases, tiers, roles, and artifact types.

Do not merge these into one flat registry bucket. Do not encode vendor model
brands, live routing policy, playbook choreography, proof doctrine, memory
canon, network protocol, tool implementation, or runtime infrastructure here.

## Validation

Run:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agent_source_home.py
python scripts/validate_agents.py
```

For release-facing changes, run:

```bash
python scripts/release_check.py
```
