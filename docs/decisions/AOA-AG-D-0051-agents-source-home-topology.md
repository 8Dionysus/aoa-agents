# 2026-05-26: agents source home topology

## Status

Accepted. Superseded in part by
`AOA-AG-D-0052-agents-convex-source-tree.md`.

## Index Metadata

- Decision ID: AOA-AG-D-0051
- Original date: 2026-05-26
- Surface classes: agent source, root/topology, generated/readout
- Agent facets: source-home, role contract
- Mechanic parents: cross-mechanic
- Guard families: source topology, generated/read-model
- Posture: accepted

## Context

`agents/` had become the source-authored district for profiles, adjuncts,
model tiers, orchestrator classes, cohort patterns, and runtime seam bindings.
After the mechanics refactor, that was directionally right but still too
implicit: the home had family folders and builders, but no checked map that
said which families belong there, who owns each route, what publishes from
them, and where non-agent pressure must leave the repository.

Sibling organs use owner-specific homes rather than a universal template:
`skills/` owns skill bundles, `techniques/` owns technique bundles, `evals/`
owns proof bundles, and `memo/` owns reviewed memory objects. `aoa-agents`
therefore needs a role-object home, not a copied bundle layout from another
organ.

## Decision

Keep the source family paths under the active `agents/` home, and add a checked
source-home contract:

- `agents/source_home.manifest.json` records the active source families,
  owner cards, schema or mechanic-local contracts, publication targets,
  builders, validators, and stronger-owner stop lines.
- `schemas/agent-source-home.schema.json` constrains that manifest.
- `scripts/validate_agent_source_home.py` validates the manifest, family
  coverage, owner cards, matched source objects, readers, builders, and
  validators.
- `agents/roles/AGENTS.md` gives the role-house and companion-form layer a near
  route card instead of leaving forms governed only by the root agent card.

This makes `agents/` a source home for role-bearing objects while keeping
operation topology in `mechanics/` and generated readers in `generated/`.

## Consequences

- Future source-family additions or publication-route changes must update the
  manifest and pass the source-home validator.
- Adjunct profile companions stay additive to base role houses and route to
  mechanic-local schemas and validators for their narrower contracts.
- The change does not move source JSON files and does not change generated
  registry wire shape.
- Non-agent pressure still routes to the stronger owner: `aoa-skills`,
  `aoa-evals`, `aoa-memo`, `aoa-routing`, `aoa-playbooks`, or `abyss-stack`.

## Validation

Verification covers the source-home, semantic and nested-agent,
repository-wide, and focused test gates.
