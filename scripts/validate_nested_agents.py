#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_AGENTS_DOCS: dict[str, tuple[str, ...]] = {
    'profiles/AGENTS.md': (
        'source-authored role-contract surface',
        'profiles/*.profile.json',
        'generated/agent_registry.min.json',
        'docs/AGENT_PROFILE_SURFACE.md',
    ),
    'model_tiers/AGENTS.md': (
        'tier-oriented source-authored surface',
        'generated/model_tier_registry.json',
        'not model brands',
        'route -> plan -> do -> verify -> deep? -> distill',
    ),
    'cohort_patterns/AGENTS.md': (
        'generated/cohort_composition_registry.json',
        '`solo`',
        '`checkpoint_cohort`',
        'scenario composition',
    ),
    'runtime_seam/AGENTS.md': (
        'generated/runtime_seam_bindings.json',
        'route -> plan -> do -> verify -> deep? -> distill',
        'examples/runtime_artifacts/',
        'runtime infrastructure implementation',
    ),
    'generated/AGENTS.md': (
        'Do not hand edit anything under `generated/`.',
        'python scripts/build_published_surfaces.py',
        'python scripts/validate_agents.py',
        'cohort_patterns/',
    ),
    'examples/AGENTS.md': (
        'public-safe, schema-backed examples',
        'runtime_artifacts/',
        'self_agent_checkpoint/',
        'reference_routes/',
        'not the source-authored canon layer',
    ),
    'examples/runtime_artifacts/AGENTS.md': (
        'schemas/artifact.*.schema.json',
        'generated/runtime_seam_bindings.json',
        '`invalid/` exists for negative coverage',
        'docs/RUNTIME_ARTIFACT_TRANSITIONS.md',
    ),
    'examples/self_agent_checkpoint/AGENTS.md': (
        'schemas/self-agent-checkpoint.schema.json',
        'docs/SELF_AGENT_CHECKPOINT_STACK.md',
        '`checkpoint_cohort`',
        '`invalid/` exists for negative coverage',
    ),
    'examples/reference_routes/AGENTS.md': (
        'schemas/reference-route.example.schema.json',
        'docs/REFERENCE_ROUTE_EXAMPLES.md',
        'manifest.json',
        'not playbooks',
    ),
    'examples/alpha_reference_routes/AGENTS.md': (
        'schemas/alpha-reference-route.schema.json',
        'generated/alpha_reference_routes.min.json',
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
