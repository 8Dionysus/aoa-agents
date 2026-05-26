# 2026-05-26: agents source home topology

## Status

Accepted.

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

Keep the existing source family paths under `agents/`, and add a checked
source-home contract:

- `agents/source_home.manifest.json` records the active source families,
  owner cards, schema or mechanic-local contracts, publication targets,
  builders, validators, and stronger-owner stop lines.
- `schemas/agent-source-home.schema.json` constrains that manifest.
- `scripts/validate_agent_source_home.py` validates the manifest, family
  coverage, owner cards, matched source objects, readers, builders, and
  validators.
- `agents/profiles/adjuncts/AGENTS.md` gives the companion-form layer a near
  route card instead of leaving it governed only by the parent profile card.

This makes `agents/` a source home for role-bearing objects while keeping
operation topology in `mechanics/` and generated readers in `generated/`.

## Consequences

- Future source-family additions or publication-route changes must update the
  manifest and run `python scripts/validate_agent_source_home.py`.
- Adjunct profile companions stay additive to base role houses and route to
  mechanic-local schemas and validators for their narrower contracts.
- The change does not move source JSON files and does not change generated
  registry wire shape.
- Non-agent pressure still routes to the stronger owner: `aoa-skills`,
  `aoa-evals`, `aoa-memo`, `aoa-routing`, `aoa-playbooks`, or `abyss-stack`.

## Validation

- `python scripts/validate_agent_source_home.py`
- `python scripts/validate_semantic_agents.py`
- `python scripts/validate_nested_agents.py`
- `python scripts/validate_agents.py`
- `python -m unittest discover -s tests -p 'test_*.py'`
