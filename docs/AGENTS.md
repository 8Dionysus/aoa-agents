# AGENTS.md

## Guidance For `docs/`

`docs/` explains the agent model, role contracts, handoff posture, boundary
posture, current surface contour, decision rationale, and route maps for
`aoa-agents`.

It is not the source object home, mechanic package home, generated companion
home, or sibling-owner doctrine shelf.

## Operating Card

| Field | Route |
| --- | --- |
| role | docs-local route card for role-layer explanation and maps |
| input | docs-map, boundary, contour, decision, model, memory-posture, or handoff wording changes |
| output | clarified docs surface or route to source object, mechanic package, decision, generated companion, or sibling owner |
| owner | this card for docs edits; target docs own their meaning |
| next route | `docs/README.md`, target doc, nearest source or mechanic owner |
| validation | `python scripts/validate_agents.py` and `python scripts/validate_semantic_agents.py` |

## Read First

1. root `AGENTS.md`
2. `docs/README.md`
3. target docs surface
4. nearest source, mechanic, generated, or sibling-owner route that the doc names

For current shipped surface inventories, use `docs/CURRENT_CONTOUR.md`.
For preserved root-era detail, use `docs/AGENTS_ROOT_REFERENCE.md` only as a
reference; do not promote it back into active root law.

## Boundaries

Docs can clarify role semantics, but source-authored profile and class surfaces
still own concrete identity fields.

Keep personhood, self-agency, Titan, formation, recurrence, checkpoint, and
growth language bounded, reviewable, evidence-linked, and reversible. Do not
make autonomy claims that profiles, evals, memory posture, projection law, or
runtime seams cannot support.

When docs change handoff, memory, evaluation, projection, formation, or runtime
posture, re-check the relevant profile, cohort, runtime seam, mechanic package,
and downstream proof/memo surfaces.

## Verify

```bash
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
```

Run broader tests from root `AGENTS.md` when root entrypoints, contour
discoverability, or route-card law changes.
