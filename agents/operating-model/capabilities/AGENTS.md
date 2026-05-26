# agents/operating-model/capabilities/AGENTS.md

## Purpose

`agents/operating-model/capabilities/` owns reusable capability packs for role
specializations.

Capability packs describe permission posture, tool refs, skill refs, technique
refs, memory routes, proof routes, and projection hints. They do not implement
tools, skills, techniques, memory objects, proof doctrine, routing policy, or
runtime behavior.

## Source of truth

Canonical authoring lives in:

- `agents/operating-model/capabilities/packs/*.capability.json`
- `schemas/capability-pack.schema.json`
- `agents/source_home.manifest.json`

Published derived surfaces live under `generated/` and must be rebuilt from
the source objects.

## Editing posture

Use capability packs when several role specializations need the same operating
shape without copying a bundle of tools and permissions into each role house.

Keep packs small and referential:

- name the allowed posture;
- point to tools, skills, techniques, memory routes, and proof routes;
- route stronger ownership outward when the referenced thing needs real
  implementation or policy.

Do not place execution workflow bodies, memory canon, proof verdict logic,
tool implementation, network protocol, or runtime infrastructure here.

## Validation

Run:

```bash
python scripts/build_published_surfaces.py
python scripts/validate_agent_source_home.py
python scripts/validate_agents.py
```
