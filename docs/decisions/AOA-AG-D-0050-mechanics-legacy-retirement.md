# AOA-AG-D-0050 Mechanics Legacy Retirement

## Decision

On 2026-09-04, the `.agents/spark/` companion and twelve package-local
`mechanics/*/legacy/` scaffolding roots are retired. Active part routes remain
the sole current source. Former content is recoverable from baseline commit
`850b86674e77dc741cb53322fb89eaee8bcb1aef` and immutable Git history; the
retired roots are intentionally not an active compatibility route.

## Boundary

This removes archive-only scaffolding and does not change role meaning,
behavioral contracts, source objects, or generated authority. Reviewed memo
candidates retain their historic source references and are not rewritten.

## Recovery

The complete path/blob baseline is recorded in
`surface-retirement-20260904/baseline.json`; every targeted blob was verified
recoverable before removal. No `.aoa`, host, runtime, remote, tag, PR, or merge
surface is part of this decision.
