# Capability graph

Derived from `capabilities/families/*.yaml`. This file is a read model, not capability authority.

Source content hash: `038b62eae14ad2525bf5268aaed1b136b4c89572d00dc90bbe18cd52d168e17b`

## Semantic tree

- `aoa-agents` (capability, internal, healthy)
  - `aoa-agents-skills` (capability, internal, healthy)
    - `agents.progression` (capability, internal, healthy)
      - `skill.aoa-session-progression-lift` (skill, advertised, challenger)
    - `mode.agents.bind-incarnation` (mode, internal, challenger)
    - `mode.agents.detect-obligation` (mode, internal, challenger)
    - `mode.agents.form-actor` (mode, internal, challenger)
    - `mode.agents.receive-return` (mode, internal, challenger)
    - `mode.agents.transfer-responsibility` (mode, internal, challenger)
    - `skill.aoa-agents-skills` (skill, advertised, challenger)
      - `agents.lifecycle.incarnation` (capability, internal, healthy)
        - `agents.lifecycle.execution` (capability, internal, healthy)
          - `mode.aoa-summon.decide` (mode, internal, challenger)
          - `mode.aoa-summon.execute` (mode, internal, challenger)
          - `skill.aoa-summon` (skill, advertised, challenger)
      - `agents.lifecycle.pressure` (capability, internal, healthy)
      - `agents.lifecycle.relationship` (capability, internal, healthy)

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
| primary-parent | `mode.agents.bind-incarnation` | `aoa-agents-skills` | - |
| primary-parent | `mode.agents.detect-obligation` | `aoa-agents-skills` | - |
| primary-parent | `mode.agents.form-actor` | `aoa-agents-skills` | - |
| primary-parent | `mode.agents.receive-return` | `aoa-agents-skills` | - |
| primary-parent | `mode.agents.transfer-responsibility` | `aoa-agents-skills` | - |
| primary-parent | `mode.aoa-summon.decide` | `agents.lifecycle.execution` | - |
| primary-parent | `mode.aoa-summon.execute` | `agents.lifecycle.execution` | - |
| primary-parent | `skill.aoa-agents-skills` | `aoa-agents-skills` | - |
| primary-parent | `skill.aoa-session-progression-lift` | `agents.progression` | - |
| primary-parent | `skill.aoa-summon` | `agents.lifecycle.execution` | - |
| produces | `mode.agents.detect-obligation` | `mode.agents.form-actor` | One independent obligation is admitted and actor formation is required. |
| produces | `mode.agents.form-actor` | `mode.agents.bind-incarnation` | The stable mandate is complete and a physical realization is required. |
| requires | `mode.agents.transfer-responsibility` | `mode.agents.bind-incarnation` | External transfer requires the exact admitted incarnation binding. |
