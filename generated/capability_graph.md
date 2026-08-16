# Capability graph

Derived from `capabilities/families/*.yaml`. This file is a read model, not capability authority.

Source content hash: `32da0fd32f39be5e30bc69149314f3593d28899e163fb53e5fe439249ac8ab8f`

## Semantic tree

- `aoa-agents` (capability, internal, healthy)
  - `aoa-agents-skills` (capability, internal, healthy)
    - `agents.progression` (capability, internal, healthy)
      - `skill.aoa-session-progression-lift` (skill, advertised, challenger)
    - `skill.aoa-agents-skills` (skill, advertised, challenger)
      - `agents.lifecycle.incarnation` (capability, internal, healthy)
        - `agents.lifecycle.execution` (capability, internal, healthy)
          - `mode.aoa-summon.decide` (mode, internal, challenger)
          - `mode.aoa-summon.execute` (mode, internal, challenger)
          - `skill.aoa-summon` (skill, advertised, challenger)
        - `mode.agents.bind-incarnation` (mode, internal, challenger)
      - `agents.lifecycle.pressure` (capability, internal, healthy)
        - `mode.agents.detect-obligation` (mode, internal, challenger)
        - `mode.agents.form-actor` (mode, internal, challenger)
      - `agents.lifecycle.relationship` (capability, internal, healthy)
        - `mode.agents.receive-return` (mode, internal, challenger)
        - `mode.agents.transfer-responsibility` (mode, internal, challenger)
      - `mode.agents.role-first-entry` (mode, internal, challenger)

## Typed relations

| kind | source | target | condition |
|---|---|---|---|
| conflicts-with | `mode.agents.form-actor` | `skill.aoa-session-progression-lift` | A progression candidate cannot mutate the stable role or grant the new mandate. |
| conflicts-with | `skill.aoa-session-progression-lift` | `mode.agents.form-actor` | Role formation cannot cite an unreviewed progression candidate as authority. |
| hands-off-to | `mode.agents.transfer-responsibility` | `skill.aoa-summon` | The admitted transfer emits a complete external execution request and the selected leaf exposes a real external CLI lane. |
| hands-off-to | `skill.aoa-summon` | `mode.agents.receive-return` | A bound runtime result, event, refusal, failure, or return enters the responsibility filter. |
| primary-parent | `agents.lifecycle.execution` | `agents.lifecycle.incarnation` | - |
| primary-parent | `agents.lifecycle.incarnation` | `skill.aoa-agents-skills` | - |
| primary-parent | `agents.lifecycle.pressure` | `skill.aoa-agents-skills` | - |
| primary-parent | `agents.lifecycle.relationship` | `skill.aoa-agents-skills` | - |
| primary-parent | `agents.progression` | `aoa-agents-skills` | - |
| primary-parent | `aoa-agents-skills` | `aoa-agents` | - |
| primary-parent | `mode.agents.bind-incarnation` | `agents.lifecycle.incarnation` | - |
| primary-parent | `mode.agents.detect-obligation` | `agents.lifecycle.pressure` | - |
| primary-parent | `mode.agents.form-actor` | `agents.lifecycle.pressure` | - |
| primary-parent | `mode.agents.receive-return` | `agents.lifecycle.relationship` | - |
| primary-parent | `mode.agents.role-first-entry` | `skill.aoa-agents-skills` | - |
| primary-parent | `mode.agents.transfer-responsibility` | `agents.lifecycle.relationship` | - |
| primary-parent | `mode.aoa-summon.decide` | `agents.lifecycle.execution` | - |
| primary-parent | `mode.aoa-summon.execute` | `agents.lifecycle.execution` | - |
| primary-parent | `skill.aoa-agents-skills` | `aoa-agents-skills` | - |
| primary-parent | `skill.aoa-session-progression-lift` | `agents.progression` | - |
| primary-parent | `skill.aoa-summon` | `agents.lifecycle.execution` | - |
| produces | `mode.agents.detect-obligation` | `mode.agents.form-actor` | One independent obligation is admitted and actor formation is required. |
| produces | `mode.agents.form-actor` | `mode.agents.bind-incarnation` | The stable mandate is complete and a physical realization is required. |
| produces | `mode.agents.role-first-entry` | `mode.agents.detect-obligation` | The explicit semantic intent is normalized into goal-pressure-v1 before obligation detection. |
| requires | `mode.agents.transfer-responsibility` | `mode.agents.bind-incarnation` | External transfer requires the exact admitted incarnation binding. |
