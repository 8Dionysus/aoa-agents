# 2026-05-26: Antifragility Stress Check Localization

## Status

Accepted.

## Index Metadata

- Decision ID: AOA-AG-D-0014
- Original date: 2026-05-26
- Surface classes: mechanic part, validation guard
- Agent facets: mechanics atlas, stress posture
- Mechanic parents: antifragility
- Guard families: part-local artifact, validation guard
- Posture: accepted

## Context

The stress-posture part already owned its docs, schemas, examples, and
payload validator semantics, but the executable validator and its public-surface
test still lived in root `scripts/` and `tests/`. That made the part-local
contract depend on root districts after the payloads had already moved.

Sibling mechanics in `Agents-of-Abyss`, `aoa-evals`, and `aoa-memo` use
package-local or part-local `scripts/` and `tests/` when a check protects a
mechanic-specific contract. Root release gates still call those checks when the
repo needs a single validation entrypoint.

## Decision

Move the stress-posture validator and test into:

- `mechanics/antifragility/parts/stress-posture/scripts/validate_stress_posture.py`
- `mechanics/antifragility/parts/stress-posture/tests/test_stress_posture.py`

Keep `scripts/validate_agents.py` as the repo-wide validation coordinator by
loading the part-local validator explicitly. Teach `scripts/release_check.py`
to run the part-local stress test before the remaining root test suite.

Preserve former root-path lookup only through antifragility `PROVENANCE.md` and
`legacy/`.

## Consequences

- The `stress-posture` part now owns its contract payloads and direct checks.
- Root `scripts/` and `tests/` remain active for repo-wide builders, validators,
  and tests.
- The release gate protects the new test location explicitly, so localizing the
  test does not reduce coverage.
- This is a precedent for moving mechanic-specific checks one bounded part at a
  time, not a wholesale move of every root script or test.

## Verification

Verification routes through the focused owner checks and the repository release gate.
