#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_AGENTS_DOCS: dict[str, tuple[str, ...]] = {
    '.agents/AGENTS.md': (
        '.agents/',
        'agent-facing companion surfaces',
        '.agents/spark/AGENTS.md',
        'not the source-authored `agents/` district',
    ),
    '.agents/spark/AGENTS.md': (
        '.agents/spark/',
        'fast-loop lane',
        'Spark work',
        'source docs before editing',
    ),
    'agents/AGENTS.md': (
        'Operating Card',
        'source-authored agent district',
        'agents/README.md',
        'agents/profiles/',
        'mechanics/',
    ),
    'agents/profiles/AGENTS.md': (
        'source-authored role-contract surface',
        'agents/profiles/*.profile.json',
        'generated/agent_registry.min.json',
        'docs/AGENT_PROFILE_SURFACE.md',
    ),
    'agents/model_tiers/AGENTS.md': (
        'tier-oriented source-authored surface',
        'generated/model_tier_registry.json',
        'not model brands',
        'route -> plan -> do -> verify -> deep? -> distill',
    ),
    'agents/orchestrator_classes/AGENTS.md': (
        'source-authored class-identity surface',
        'generated/orchestrator_class_catalog.min.json',
        'generated/orchestrator_class_capsules.json',
        'generated/orchestrator_class_sections.full.json',
    ),
    'agents/cohort_patterns/AGENTS.md': (
        'generated/cohort_composition_registry.json',
        '`solo`',
        '`checkpoint_cohort`',
        'scenario composition',
    ),
    'agents/runtime_seam/AGENTS.md': (
        'generated/runtime_seam_bindings.json',
        'route -> plan -> do -> verify -> deep? -> distill',
        'mechanics/runtime-seam/parts/artifact-contracts/examples/',
        'runtime infrastructure implementation',
    ),
    'mechanics/AGENTS.md': (
        'Operating Card',
        'operation atlas',
        'mechanics/README.md',
        'mechanics/ARTIFACT_TOPOLOGY.md',
        'runtime implementation',
    ),
    'mechanics/agon/AGENTS.md': (
        'mechanics/agon/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'Formation is a part of Agon',
    ),
    'mechanics/antifragility/AGENTS.md': (
        'mechanics/antifragility/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'Durable memory of scars belongs to `aoa-memo`.',
    ),
    'mechanics/boundary-bridge/AGENTS.md': (
        'mechanics/boundary-bridge/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'General routing policy belongs to `aoa-routing`.',
    ),
    'mechanics/checkpoint/AGENTS.md': (
        'mechanics/checkpoint/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'Runtime checkpoint execution belongs to runtime owners.',
    ),
    'mechanics/codex-projection/AGENTS.md': (
        'mechanics/codex-projection/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'Generated projection manifests are evidence, not authority.',
    ),
    'mechanics/experience/AGENTS.md': (
        'mechanics/experience/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'Runtime assistant services do not live here.',
    ),
    'mechanics/questbook/AGENTS.md': (
        'mechanics/questbook/',
        'Operating Card',
        'root `quests/` owns source records',
        'PROVENANCE.md',
        'aoa-playbooks',
    ),
    'mechanics/recurrence/AGENTS.md': (
        'mechanics/recurrence/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'Runtime owners own live recurrence execution.',
    ),
    'mechanics/release-support/AGENTS.md': (
        'mechanics/release-support/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'Root `AGENTS.md` still owns branch, PR, CI, and merge route.',
    ),
    'mechanics/rpg/AGENTS.md': (
        'mechanics/rpg/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'Stats and movement summaries belong to `aoa-stats`.',
    ),
    'mechanics/runtime-seam/AGENTS.md': (
        'mechanics/runtime-seam/',
        'Operating Card',
        'parts/AGENTS.md',
        'agents/runtime_seam/AGENTS.md',
        'Runtime implementation belongs to runtime owners',
    ),
    'mechanics/titan/AGENTS.md': (
        'mechanics/titan/',
        'Operating Card',
        'parts/AGENTS.md',
        'PROVENANCE.md',
        'AoA center owns larger Titan doctrine.',
    ),
    'docs/decisions/AGENTS.md': (
        'docs/decisions/',
        'route-law',
        'topology decisions',
        'validate_nested_agents.py',
    ),
    'generated/AGENTS.md': (
        'Do not hand edit anything under `generated/`.',
        'python scripts/build_published_surfaces.py',
        'python scripts/validate_agents.py',
        'agents/cohort_patterns/',
        'orchestrator_class_catalog.min.json',
    ),
    'examples/AGENTS.md': (
        'public-safe, schema-backed examples',
        'mechanics/runtime-seam/parts/artifact-contracts/examples/',
        'mechanics/checkpoint/parts/self-agent-checkpoint/examples/',
        'mechanics/checkpoint/parts/reference-routes/examples/',
        'not the source-authored canon layer',
    ),
    'mechanics/runtime-seam/parts/artifact-contracts/examples/README.md': (
        '[schemas/](../schemas/)',
        'generated/runtime_seam_bindings.json',
        '`invalid/` exists for negative coverage',
        'mechanics/runtime-seam/parts/transition-discipline/docs/runtime-artifact-transitions.md',
    ),
    'mechanics/checkpoint/parts/self-agent-checkpoint/examples/README.md': (
        '../schemas/self-agent-checkpoint.schema.json',
        'mechanics/checkpoint/parts/self-agent-checkpoint/docs/self-agent-checkpoint-stack.md',
        '`checkpoint_cohort`',
        '`invalid/` exists for negative coverage',
    ),
    'mechanics/checkpoint/parts/reference-routes/examples/README.md': (
        'mechanics/checkpoint/parts/reference-routes/schemas/reference-route-manifest.schema.json',
        'mechanics/checkpoint/parts/reference-routes/docs/reference-route-examples.md',
        'manifest.json',
        'not playbooks',
    ),
    'mechanics/questbook/parts/alpha-reference-routes/examples/README.md': (
        'mechanics/questbook/parts/alpha-reference-routes/schemas/alpha-reference-route.schema.json',
        'mechanics/questbook/parts/alpha-reference-routes/generated/alpha-reference-routes.min.json',
        'curated Alpha cohort',
        'readiness proof lane',
    ),
}

ACTIVE_PROVENANCE_DOCS: tuple[str, ...] = (
    'mechanics/AGENTS.md',
    'mechanics/README.md',
    'mechanics/ARTIFACT_TOPOLOGY.md',
    'mechanics/PAYLOAD_RECON.md',
    'mechanics/PROVENANCE_TOPOLOGY.md',
    'mechanics/agon/AGENTS.md',
    'mechanics/agon/PARTS.md',
    'mechanics/agon/parts/AGENTS.md',
    'mechanics/antifragility/AGENTS.md',
    'mechanics/antifragility/PARTS.md',
    'mechanics/antifragility/parts/AGENTS.md',
    'mechanics/boundary-bridge/AGENTS.md',
    'mechanics/boundary-bridge/PARTS.md',
    'mechanics/boundary-bridge/parts/AGENTS.md',
    'mechanics/checkpoint/AGENTS.md',
    'mechanics/checkpoint/PARTS.md',
    'mechanics/checkpoint/parts/AGENTS.md',
    'mechanics/codex-projection/AGENTS.md',
    'mechanics/codex-projection/PARTS.md',
    'mechanics/codex-projection/parts/AGENTS.md',
    'mechanics/experience/AGENTS.md',
    'mechanics/experience/PARTS.md',
    'mechanics/experience/parts/AGENTS.md',
    'mechanics/questbook/AGENTS.md',
    'mechanics/questbook/PARTS.md',
    'mechanics/questbook/parts/AGENTS.md',
    'mechanics/recurrence/AGENTS.md',
    'mechanics/recurrence/PARTS.md',
    'mechanics/recurrence/parts/AGENTS.md',
    'mechanics/recurrence/parts/component-manifests/manifests/README.md',
    'mechanics/release-support/AGENTS.md',
    'mechanics/release-support/PARTS.md',
    'mechanics/release-support/parts/AGENTS.md',
    'mechanics/rpg/AGENTS.md',
    'mechanics/rpg/PARTS.md',
    'mechanics/rpg/parts/AGENTS.md',
    'mechanics/runtime-seam/AGENTS.md',
    'mechanics/runtime-seam/PARTS.md',
    'mechanics/runtime-seam/parts/AGENTS.md',
    'mechanics/titan/AGENTS.md',
    'mechanics/titan/PARTS.md',
    'mechanics/titan/parts/AGENTS.md',
)

FORBIDDEN_ACTIVE_PROVENANCE_SNIPPETS: tuple[str, ...] = (
    'Legacy Bridge',
    'legacy/',
    'legacy accounting',
    'legacy lookup',
    'legacy is',
    'Legacy is',
)

PROVENANCE_BRIDGE_DOCS: tuple[str, ...] = (
    'mechanics/agon/PROVENANCE.md',
    'mechanics/antifragility/PROVENANCE.md',
    'mechanics/boundary-bridge/PROVENANCE.md',
    'mechanics/checkpoint/PROVENANCE.md',
    'mechanics/codex-projection/PROVENANCE.md',
    'mechanics/experience/PROVENANCE.md',
    'mechanics/questbook/PROVENANCE.md',
    'mechanics/recurrence/PROVENANCE.md',
    'mechanics/release-support/PROVENANCE.md',
    'mechanics/rpg/PROVENANCE.md',
    'mechanics/runtime-seam/PROVENANCE.md',
    'mechanics/titan/PROVENANCE.md',
)

REQUIRED_PROVENANCE_BRIDGE_SNIPPETS: tuple[str, ...] = (
    '## Current Route First',
    'If those surfaces answer the task, stop there.',
    '## Archive Route',
    'legacy/INDEX.md',
    'legacy/DISTILLATION_LOG.md',
    'legacy/raw/README.md',
    '## Distillation Rule',
    'Active part docs must not grow',
)


class NestedAgentsValidationError(RuntimeError):
    pass


def _describe_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except FileNotFoundError as exc:
        raise NestedAgentsValidationError(f'missing required file: {_describe_path(path)}') from exc


def validate_nested_agents_docs(root: Path = REPO_ROOT) -> None:
    for rel_path, required_snippets in REQUIRED_AGENTS_DOCS.items():
        path = root / rel_path
        text = _read_text(path)
        missing = [snippet for snippet in required_snippets if snippet not in text]
        if missing:
            joined = ', '.join(repr(snippet) for snippet in missing)
            raise NestedAgentsValidationError(
                f'{rel_path} is missing required guidance snippet(s): {joined}'
            )
    for rel_path in ACTIVE_PROVENANCE_DOCS:
        path = root / rel_path
        text = _read_text(path)
        found = [snippet for snippet in FORBIDDEN_ACTIVE_PROVENANCE_SNIPPETS if snippet in text]
        if found:
            joined = ', '.join(repr(snippet) for snippet in found)
            raise NestedAgentsValidationError(
                f'{rel_path} should route through PROVENANCE.md without active archive leakage: {joined}'
            )
    for rel_path in PROVENANCE_BRIDGE_DOCS:
        path = root / rel_path
        text = _read_text(path)
        missing = [snippet for snippet in REQUIRED_PROVENANCE_BRIDGE_SNIPPETS if snippet not in text]
        if missing:
            joined = ', '.join(repr(snippet) for snippet in missing)
            raise NestedAgentsValidationError(
                f'{rel_path} is missing provenance bridge operating snippet(s): {joined}'
            )


def main() -> int:
    try:
        validate_nested_agents_docs()
    except NestedAgentsValidationError as exc:
        print(f'[error] {exc}', file=sys.stderr)
        return 1

    print('[ok] validated nested AGENTS.md guidance surfaces')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
