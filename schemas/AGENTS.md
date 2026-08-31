# AGENTS.md

## Applies To

This card applies to root `schemas/`. A mechanic-local schema follows the
nearest mechanic route instead.

## Role

Root schemas own shared machine shape for agent source families and generated
registries. Use [README.md](README.md) on demand for the schema inventory and
mechanic-local family map.

## Boundaries

- Schema edits are role contract edits; keep role authority bounded.
- Keep a schema here only when multiple source families, generated readers,
  tests, or public consumers share it.
- Move mechanic-specific shape only to a part with an explicit route and
  validator.
- Preserve `$schema`, stable `$id` or identifier posture, required fields,
  enums, and authority-bounding descriptions.
- Do not loosen a schema to make a vague source object or local example pass.
- Pair semantic schema changes with their source objects, examples, generated
  readers, builders, and validators as applicable.

## Validation

Use root [VALIDATION.md](../VALIDATION.md) and the source-family or
mechanic-local check identified by the affected owner route.

## Closeout

Report the schema owner, source and generated consumers reviewed, checks run,
checks skipped, and any stronger-owner handoff.
