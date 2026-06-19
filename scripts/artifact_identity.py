from __future__ import annotations


GENERATED_REGISTRY_TRUST_LAYER = ["abi_contract_signature", "w3c_prov_lineage"]
GENERATED_REGISTRY_PRIVACY_BOUNDARY = (
    "Public source-authored agent-layer metadata only; no private prompts, "
    "session transcripts, secrets, live runtime state, or hidden operator traces."
)
GENERATED_REGISTRY_VERIFICATION = [
    "python scripts/build_published_surfaces.py",
    "python scripts/validate_agents.py",
    "python -m pytest -q tests/test_published_consumer_feeds.py",
]


def build_generated_registry_artifact_identity(
    *,
    artifact_class: str,
    surface_state: str,
    authority_ref: str,
    producer: str,
    consumer_expectation: str,
    content_identity: str,
    abi_epoch: str,
    contract_version: str,
) -> dict[str, object]:
    return {
        "artifact_class": artifact_class,
        "surface_state": surface_state,
        "owner_repo": "aoa-agents",
        "authority_ref": authority_ref,
        "producer": producer,
        "consumer_expectation": consumer_expectation,
        "privacy_boundary": GENERATED_REGISTRY_PRIVACY_BOUNDARY,
        "content_identity": content_identity,
        "abi_epoch": abi_epoch,
        "contract_version": contract_version,
        "trust_layer": list(GENERATED_REGISTRY_TRUST_LAYER),
        "verification": list(GENERATED_REGISTRY_VERIFICATION),
        "action": "ADD_CONSUMER_EXPECTATION",
    }
