# Documentation Map

This is the human and agent entrypoint for the `docs/` surface of
`aoa-agents`.

Use the root [README](../README.md) as the public front door. Use this file
after entering `docs/` to choose the right role-layer source, map, boundary,
decision, or operation route.

Operational edit law belongs in the nearest `AGENTS.md`. This map explains
where meaning lives and which surface to open next.

## Operating Card

| Field | Route |
| --- | --- |
| role | docs entrypoint and source-of-truth chooser |
| input | role-model, boundary, contour, formation, projection, handoff, or docs-placement questions |
| output | next owner surface, mechanic package, source object, decision record, or stronger-owner route |
| owner | `docs/AGENTS.md` for docs edits; target source files own their meaning |
| next route | `agents/`, `mechanics/`, `docs/decisions/`, or sibling owner repositories |
| validation | [docs/AGENTS](AGENTS.md) and the nearest owner route card |

## First Route

| Question | Open |
| --- | --- |
| What is this repository? | [aoa-agents](../README.md) |
| May this claim live here? | [CHARTER](../CHARTER.md), then [BOUNDARIES](BOUNDARIES.md) |
| What shape is the role layer preserving? | [DESIGN](../DESIGN.md) |
| How should agent-facing route cards look? | [DESIGN.AGENTS](../DESIGN.AGENTS.md) |
| What is an agent here? | [AGENT_MODEL](AGENT_MODEL.md) |
| Where do role source objects live? | [agents](../agents/README.md) |
| Which shipped route family should I inspect? | [CURRENT_CONTOUR](CURRENT_CONTOUR.md) |
| Which repeatable operation owns this? | [mechanics](../mechanics/README.md), then the owning package |
| What should happen next at repo level? | [ROADMAP](../ROADMAP.md) |
| Why was this topology chosen? | [decisions](decisions/README.md) |

## Source Families

| Family | Owner Surface |
| --- | --- |
| Agent conceptual model | [AGENT_MODEL](AGENT_MODEL.md) |
| Source-authored profile shape | [AGENT_PROFILE_SURFACE](AGENT_PROFILE_SURFACE.md) |
| Role-level memory posture | [AGENT_MEMORY_POSTURE](AGENT_MEMORY_POSTURE.md) |
| Model-tier posture | [MODEL_TIER_MODEL](MODEL_TIER_MODEL.md) |
| Orchestrator class identity | [ORCHESTRATOR_CLASS_MODEL](ORCHESTRATOR_CLASS_MODEL.md) |
| Repository boundaries | [BOUNDARIES](BOUNDARIES.md) |
| Current shipped contour | [CURRENT_CONTOUR](CURRENT_CONTOUR.md) |
| Structural decisions | [decisions](decisions/README.md) |
| Preserved root reference | [AGENTS_ROOT_REFERENCE](AGENTS_ROOT_REFERENCE.md) |

## Mechanic Routes

Mechanic-local docs live with their mechanics, not as a flat `docs/` pile.

| Route Family | Start Surface |
| --- | --- |
| Codex projection, specialization eligibility, and Codex Subagent Refresh Law | [mechanics/codex-projection](../mechanics/codex-projection/README.md) |
| Agonic Actor Rechartering, Agent Kind Model, Agent Resistance and Revision Posture, Agent Formation Trial, Formation Trial Landing, and Codex Projection Agon Boundary | [mechanics/agon](../mechanics/agon/README.md) |
| Assistant Civil Rechartering, Assistant Service Contract Model, Assistant Escalation to Agon, service identity, governance, certification, and arena exclusion | [mechanics/experience](../mechanics/experience/README.md) |
| Titan role-bearing, lineage, summon, runtime roster, service cohort, and incarnation identity | [mechanics/titan](../mechanics/titan/README.md) |
| Agent Stress Posture, Agent Stress Handoffs, via negativa, and scar/adaptation posture | [mechanics/antifragility](../mechanics/antifragility/README.md) |
| Runtime seam, role-tier bindings, artifact contracts, and transition discipline | [mechanics/runtime-seam](../mechanics/runtime-seam/README.md) |
| Self-agent checkpoint, continuity lane, reference routes, and reviewed closeout holds | [mechanics/checkpoint](../mechanics/checkpoint/README.md) |
| Quest execution passport, Alpha reference routes, dispatch readers, and quest source store posture | [mechanics/questbook](../mechanics/questbook/README.md) |
| Workspace Surface Trigger Posture, federation consumer seams, source registry, and published compatibility | [mechanics/boundary-bridge](../mechanics/boundary-bridge/README.md) |
| Recursor readiness, recurrence discipline, component manifests, and projection candidates | [mechanics/recurrence](../mechanics/recurrence/README.md) |
| Cohort patterns, progression model, checkpoint growth, and quest-readable status | [mechanics/rpg](../mechanics/rpg/README.md) |

## Claim Routes

| Question | Route |
| --- | --- |
| Is this role or persona meaning? | [CHARTER](../CHARTER.md), [AGENT_MODEL](AGENT_MODEL.md), then `agents/` |
| Is this a source object or generated reader? | [agents](../agents/README.md), source object, builder, generated output, validator |
| Is this repeatable operation pressure? | [mechanics](../mechanics/README.md), then package `AGENTS.md` and `PARTS.md` |
| Is this Codex install or projection drift? | [codex-projection](../mechanics/codex-projection/README.md), then refresh-law and projection docs |
| Is this proof or verdict logic? | route to `aoa-evals` |
| Is this workflow execution? | route to `aoa-skills` |
| Is this reusable practice? | route to `aoa-techniques` |
| Is this memory object or recall truth? | route to `aoa-memo` |
| Is this dispatch policy? | route to `aoa-routing` |
| Is this scenario choreography? | route to `aoa-playbooks` |
| Is this runtime implementation? | route to `abyss-stack` |

## Change Routes

| Change | First route |
| --- | --- |
| Root or docs-map wording | [AGENTS](../AGENTS.md), [DESIGN](../DESIGN.md), this map |
| Source object family | [agents](../agents/README.md), then nearest branch card |
| Mechanic package or part | [mechanics](../mechanics/README.md), then package `AGENTS.md` and `PARTS.md` |
| Current contour discoverability | [CURRENT_CONTOUR](CURRENT_CONTOUR.md) |
| Generated parity | source surface, builder, generated output, validator, and test together |
| Decision rationale | [decisions/AGENTS](decisions/AGENTS.md), then [decisions/README](decisions/README.md) |
| Release-visible public docs | [AGENTS](../AGENTS.md), [CHANGELOG](../CHANGELOG.md) when a release note is actually needed |

## Validation Route

Executable commands for docs-map and root-route changes live in
[AGENTS.md#verify](../AGENTS.md#verify) and the nearest local route card.

Generated reader parity routes through [generated/AGENTS](../generated/AGENTS.md).
Mechanic-owned payload docs route through [mechanics/AGENTS](../mechanics/AGENTS.md)
and the package card.

## Notes

- Prefer [CURRENT_CONTOUR](CURRENT_CONTOUR.md) for shipped surface inventories.
- Prefer [BOUNDARIES](BOUNDARIES.md) when a document starts absorbing sibling
  meaning.
- Prefer [decisions](decisions/README.md) when future contributors need to know
  why a route or topology changed.
- Prefer the nearest owner route over adding another root paragraph.
