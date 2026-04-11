# QUESTBOOK.md — aoa-agents

This questbook tracks agent-layer obligations related to quest delegation, control posture, and wrapper allowance.

## Frontier

- `AOA-AG-Q-0002` — define the local-wrapper allowance matrix for leaf quests
- `AOA-AG-Q-0004` — publish the router orchestrator class contract and capsule posture
- `AOA-AG-Q-0005` — publish the review orchestrator class contract and closure posture
- `AOA-AG-Q-0006` — publish the bounded-execution orchestrator class contract and smallest-step posture

## Near

- `AOA-AG-Q-0003` — define an adjunct agent progression contract keyed by agent ID

## Blocked / reanchor

- `AOA-AG-Q-0008` — reanchor checkpoint automation role-pressure in the runtime seam

## Harvest candidates

- `AOA-AG-Q-0008` — reanchor checkpoint automation role-pressure in the runtime seam

## Quest-harvest posture

`aoa-quest-harvest` may be installed at `.agents/skills/aoa-quest-harvest` as a post-session aid for this repo.

- use it only after a reviewed run, closure, or pause
- do not use it inside an active route
- it does not define orchestrator identity
- it does not replace playbook, memo, eval, or source-owned doctrine
- do not promote on one anecdotal repeat

Allowed verdicts:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

## Backing Files

- `quests/*.yaml`
- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.example.json`
