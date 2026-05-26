# Recurrence Component Manifest Set

## Operating Card

| Field | Route |
| --- | --- |
| role | package-local support payload set for recurrence component declarations |
| input | component JSON and hook JSON records |
| output | validated manifest graph over observed agent-layer recurrence surfaces |
| owner | `mechanics/recurrence/parts/component-manifests/` |
| next route | `components/`, `hooks/`, target component part, validator |
| tools | `../scripts/validate_recurrence_component_manifests.py` |
| validation | validator checks file set, component/hook pairing, stale root paths, commands, and local path references |

## Layout

- `components/` holds recurrence component declarations.
- `hooks/` holds observation-only hook binding declarations.

Former root paths are lookup facts only. Use the parent package
`PROVENANCE.md` before opening archive accounting.
