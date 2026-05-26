# Artifact Contracts Part

This part routes `artifact-contracts` pressure inside `mechanics/runtime-seam/`.

## Active Contracts

- [schemas/](schemas/) contains the seven public runtime artifact schemas for
  the `route -> plan -> do -> verify -> deep? -> distill` loop and explicit
  transition governance.
- [examples/](examples/) contains schema-backed public examples and bounded
  invalid fixtures for negative coverage.

## Active Docs

- [Agent Authority Claim Runtime](docs/authority-claim-runtime.md)

## Validation

```bash
python scripts/validate_runtime_artifact_contracts.py
python scripts/validate_agents.py
```

Use parent [PARTS.md](../../PARTS.md) for the full mechanic map and parent
[PROVENANCE.md](../../PROVENANCE.md) for former root-path accounting.
