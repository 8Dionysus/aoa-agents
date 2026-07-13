# Artifact Bundles

This directory holds OS Abyss artifact-bundle input manifests for public,
generated `aoa-agents` reader surfaces.

The manifests do not make generated readers stronger than their source role
objects. They define the portable ABI/provenance envelope that consumers must
verify before using a generated reader as orientation.

Current bundle:

- `role_contract_registry.bundle.json` wraps `generated/agent_registry.min.json`
  as `role_contract_registry` with ABI identity, SLSA/in-toto generation
  provenance, durable evidence promotion, materialized subject-store gating,
  registry latest selection, and explicit no-SBOM/no-Sigstore/no-C2PA deferrals.
