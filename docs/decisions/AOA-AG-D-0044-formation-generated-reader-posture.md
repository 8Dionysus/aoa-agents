# 2026-05-26: Formation Generated Reader Posture

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0044
- Original date: 2026-05-26
- Surface classes: generated/readout
- Agent facets: quest/alpha
- Mechanic parents: questbook, agon, experience, titan
- Guard families: generated/read-model, quest dispatch
- Posture: accepted

## Context

After the Questbook source-store repair, the next likely generated-reader
cluster was:

```text
generated/agent_agonic_formation_index.min.json
generated/assistant_civil_formation_index.min.json
generated/agent_formation_trial.min.json
```

Sibling source comparison showed two patterns:

- repo-wide generated readers stay under root `generated/` when they summarize
  root or source-object districts for low-context consumers;
- part-local generated companions move under `mechanics/*/parts/*/generated/`
  only when they summarize part-local source truth such as configs, schemas,
  examples, or mechanic payloads.

The formation readers are built from `agents/roles/`,
`agents/roles/*/forms/`, and other root generated formation readers. The
Agon and Experience parts own formation contracts, examples, docs, and
stop-lines, but not the authored agent source records.

## Decision

Keep the three formation readers root-published under `generated/`.

Document the posture in `generated/README.md`, `generated/AGENTS.md`,
`mechanics/agon/parts/formation/README.md`, and
`mechanics/experience/parts/assistant-civil-service/README.md`.

Do not create generated-reader legacy old-path accounting because no generated
reader path moved. Treat this as a route-law clarification over the existing
generated surfaces.

## Consequences

Future formation-reader work starts from the source agent family, then the
part-local builder, then the root-published generated reader. The owning
mechanics parts remain the place for builders, validators, contracts, and
stop-lines around formation, not a replacement source home for `agents/`
records.

Root `generated/` continues to own repo-wide registries, formation readers,
quest readers, and Codex/Titan projection outputs. Part-local generated
companions remain appropriate only when the reader summarizes part-local
mechanic source truth.

## Validation

Verification routes through the focused owner checks and the repository release gate.
