# 2026-05-26: Titan Check Localization

## Status

Accepted.

## Context

Titan docs, config, schemas, and examples already live under
`mechanics/titan/parts/`, but the package-level validators and focused tests
still lived in root `scripts/` and `tests/`. Those checks protect Titan-specific
contracts across multiple Titan parts rather than one repo-wide agent source
surface.

The refactored mechanics pattern in sibling repositories allows mechanic-root
`scripts/` and `tests/` when a check protects a whole mechanic package.

## Decision

Move Titan-owned validators and focused tests into:

- `mechanics/titan/scripts/validate_titan_lineage.py`
- `mechanics/titan/scripts/validate_titan_schemas.py`
- `mechanics/titan/scripts/validate_titan_examples.py`
- `mechanics/titan/tests/test_validate_titan_lineage.py`
- `mechanics/titan/tests/test_titan_schemas.py`
- `mechanics/titan/tests/test_titan_examples.py`
- `mechanics/titan/tests/test_titan_contracts.py`

Keep `scripts/validate_agents.py` as the repo-wide validation coordinator by
loading the Titan schema and example validators explicitly. Keep
`scripts/render_titan_codex_agents.py` in root for this slice because it writes
root-published generated projection companions and needs its own builder route
decision before moving.

Teach `scripts/release_check.py` to run the Titan package-local tests before
the remaining root test suite.

## Supersession Note

The temporary root route for `scripts/render_titan_codex_agents.py` was
superseded by
[2026-05-26: Titan Codex projection builder localization](2026-05-26-titan-codex-projection-builder-localization.md).
The builder now lives in `mechanics/titan/parts/codex-projection/scripts/`,
while its generated output remains root-published.

## Consequences

- Titan package checks now live next to the mechanic package they protect.
- Root `scripts/` remains active for repo-wide builders, validators, and
  publication helpers.
- Root `tests/` remains active for repo-wide tests, while package-local Titan
  tests are explicitly covered by the release gate.
- Former root check paths are provenance/legacy lookup facts only.

## Verification

```bash
python mechanics/titan/scripts/validate_titan_lineage.py --roles mechanics/titan/parts/role-bearing/config/role-classes.v0.json --bearers mechanics/titan/parts/role-bearing/config/bearers.v0.json --ledger mechanics/titan/parts/lineage-ledger/config/ledger.v0.json
python mechanics/titan/scripts/validate_titan_schemas.py
python mechanics/titan/scripts/validate_titan_examples.py
python -m unittest discover -s mechanics/titan/tests -p "test_*.py"
python scripts/validate_agents.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
python scripts/release_check.py
```
