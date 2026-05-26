#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_AGENTS_DOCS: dict[str, tuple[str, ...]] = {
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
