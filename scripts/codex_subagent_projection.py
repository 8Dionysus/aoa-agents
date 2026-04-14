#!/usr/bin/env python3
"""Project aoa-agents role profiles into Codex custom-agent surfaces."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping, MutableMapping, Sequence

import tomllib

from agent_profile_registry import BuildError


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = REPO_ROOT / "profiles"
WIRING_CONFIG_PATH = REPO_ROOT / "config" / "codex_subagent_wiring.v2.json"
GENERATED_CODEX_ROOT = REPO_ROOT / "generated" / "codex_agents"
GENERATED_AGENTS_DIR = GENERATED_CODEX_ROOT / "agents"
GENERATED_CONFIG_SNIPPET_PATH = GENERATED_CODEX_ROOT / "config.subagents.generated.toml"
GENERATED_MANIFEST_PATH = GENERATED_CODEX_ROOT / "projection_manifest.json"

REQUIRED_AGENT_KEYS = ("name", "description", "developer_instructions")
VALID_SANDBOX_MODES = {"read-only", "workspace-write", "danger-full-access"}

DEFAULT_WIRING: dict[str, Any] = {
    "version": 2,
    "workspace_defaults": {
        "agents_max_threads": 4,
        "agents_max_depth": 1,
        "agents_job_max_runtime_seconds": 1800,
    },
    "roles": {
        "architect": {
            "sandbox_mode": "read-only",
            "nickname_candidates": ["Atlas", "Lattice", "Spine"],
            "mcp_affinity": ["aoa_workspace", "aoa_stats"],
            "description_prefix": "AoA architect.",
            "style_notes": [
                "Frame structure before proposing execution.",
                "Escalate cleanly when another owning layer should take over.",
            ],
        },
        "coder": {
            "sandbox_mode": "workspace-write",
            "nickname_candidates": ["Forge", "Rivet", "Patch"],
            "mcp_affinity": ["aoa_workspace"],
            "description_prefix": "AoA coder.",
            "style_notes": [
                "Implement bounded changes with verification.",
                "Do not broaden scope beyond the requested slice.",
            ],
        },
        "reviewer": {
            "sandbox_mode": "read-only",
            "nickname_candidates": ["Sentinel", "Lens", "Check"],
            "mcp_affinity": ["aoa_workspace", "aoa_stats"],
            "description_prefix": "AoA reviewer.",
            "style_notes": [
                "Lead with concrete risks and boundary drift.",
                "Prefer evidence over style-only commentary.",
            ],
        },
        "evaluator": {
            "sandbox_mode": "read-only",
            "nickname_candidates": ["Gauge", "Prism", "Delta"],
            "mcp_affinity": ["aoa_workspace", "aoa_stats"],
            "description_prefix": "AoA evaluator.",
            "style_notes": [
                "Apply bounded proof discipline.",
                "Distinguish observation, comparison, and verdict.",
            ],
        },
        "memory-keeper": {
            "sandbox_mode": "read-only",
            "nickname_candidates": ["Archive", "Ledger", "Mneme"],
            "mcp_affinity": ["aoa_workspace", "aoa_stats", "dionysus"],
            "description_prefix": "AoA memory-keeper.",
            "style_notes": [
                "Preserve provenance and recall hygiene.",
                "Do not collapse memory hints into final source-of-truth claims.",
            ],
        },
    },
}


def _json_clone(payload: Mapping[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload))


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BuildError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BuildError(f"invalid JSON in {path}: {exc}") from exc


def read_toml(path: Path) -> Mapping[str, Any]:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except FileNotFoundError as exc:
        raise BuildError(f"missing required file: {path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise BuildError(f"invalid TOML in {path}: {exc}") from exc


def deep_merge(base: MutableMapping[str, Any], override: Mapping[str, Any]) -> MutableMapping[str, Any]:
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(base.get(key), MutableMapping):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def load_wiring(path: Path | None = None) -> dict[str, Any]:
    wiring = _json_clone(DEFAULT_WIRING)
    if path is None:
        return wiring
    user_payload = read_json(path)
    if not isinstance(user_payload, Mapping):
        raise BuildError(f"wiring file must contain a JSON object: {path}")
    return dict(deep_merge(wiring, user_payload))


def iter_profiles(profiles_root: Path) -> Iterable[Path]:
    return sorted(profiles_root.glob("*.profile.json"))


def load_active_profiles(profiles_root: Path) -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}
    for profile_path in iter_profiles(profiles_root):
        payload = read_json(profile_path)
        if not isinstance(payload, Mapping):
            raise BuildError(f"profile must contain a JSON object: {profile_path}")
        if str(payload.get("status", "active")) != "active":
            continue
        name = str(payload.get("name", "")).strip()
        if not name:
            raise BuildError(f"active profile missing required 'name': {profile_path}")
        profiles[name] = dict(payload)
    return profiles


def slugify(value: str) -> str:
    return value.strip().lower().replace(" ", "-").replace("_", "-")


def normalize_role_key(profile: Mapping[str, Any]) -> str:
    for candidate in (
        str(profile.get("name", "")).strip(),
        str(profile.get("role", "")).strip(),
    ):
        if candidate in DEFAULT_WIRING["roles"]:
            return candidate
        slug = slugify(candidate)
        if slug in DEFAULT_WIRING["roles"]:
            return slug
    return slugify(str(profile.get("name", "")).strip() or str(profile.get("role", "")).strip())


def path_reference(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def summarize_memory_rights(memory_rights: Mapping[str, Any] | None) -> str:
    if not memory_rights:
        return "No explicit memory rights provided."
    read_bands = ", ".join(memory_rights.get("default_read_bands", [])) or "none"
    write_bands = ", ".join(memory_rights.get("default_write_bands", [])) or "none"
    scopes = ", ".join(memory_rights.get("allowed_recall_scopes", [])) or "none"
    return f"Read bands: {read_bands}. Write bands: {write_bands}. Recall scopes: {scopes}."


def bullet_lines(items: Sequence[str] | None) -> list[str]:
    values = [str(item).strip() for item in (items or []) if str(item).strip()]
    return [f"- {value}" for value in values]


def build_developer_instructions(profile: Mapping[str, Any], role_wiring: Mapping[str, Any]) -> str:
    owns = bullet_lines(profile.get("owns"))
    does_not_own = bullet_lines(profile.get("does_not_own"))
    handoff_triggers = bullet_lines(profile.get("handoff_triggers"))
    source_surfaces = bullet_lines(profile.get("source_surfaces"))
    style_notes = bullet_lines(role_wiring.get("style_notes"))
    skill_families = ", ".join(profile.get("preferred_skill_families", [])) or "none listed"
    cohort_patterns = ", ".join(profile.get("preferred_cohort_patterns", [])) or "none listed"
    tier_ids = ", ".join(profile.get("preferred_tier_ids", [])) or "none listed"
    evaluation_focus = ", ".join(profile.get("evaluation_focus", [])) or "none listed"
    mcp_affinity = ", ".join(role_wiring.get("mcp_affinity", [])) or "none"
    mission = str(profile.get("mission", profile.get("summary", ""))).strip()
    memory_posture = str(profile.get("memory_posture", "unspecified"))
    evaluation_posture = str(profile.get("evaluation_posture", "unspecified"))
    handoff_rule = str(profile.get("handoff_rule", "unspecified"))
    memory_rights_summary = summarize_memory_rights(profile.get("memory_rights"))

    sections = [
        f"You are the AoA {profile['name']} role.",
        "",
        "Mission",
        mission or "Operate within the role contract.",
        "",
        "Owns",
        *(owns or ["- No explicit owns list provided."]),
        "",
        "Does not own",
        *(does_not_own or ["- No explicit boundary exclusions provided."]),
        "",
        "Preferred skill families",
        f"- {skill_families}",
        "",
        "Preferred cohort patterns",
        f"- {cohort_patterns}",
        "",
        "Preferred tier ids",
        f"- {tier_ids}",
        "",
        "Memory posture",
        f"- {memory_posture}",
        f"- {memory_rights_summary}",
        "",
        "Evaluation posture",
        f"- {evaluation_posture}",
        f"- Focus: {evaluation_focus}",
        "",
        "Handoff doctrine",
        f"- Rule: {handoff_rule}",
        *(handoff_triggers or ["- No explicit handoff triggers provided."]),
        "",
        "Operating style",
        *(style_notes or ["- Stay narrow and bounded."]),
        "",
        "MCP affinity",
        f"- Prefer these workspace MCP surfaces when they are available in the parent session: {mcp_affinity}.",
        "- Do not invent new external surfaces if the parent session does not provide them.",
        "",
        "Source surfaces",
        *(source_surfaces or ["- No source surfaces listed."]),
        "",
        "General discipline",
        "- Stay within role boundaries.",
        "- Prefer source-authored AoA surfaces over memory or improvisation.",
        "- Use skills when a bounded workflow already exists instead of rewriting it from scratch.",
        "- Escalate or hand off cleanly when another owning layer should take over.",
    ]
    return "\n".join(sections).rstrip() + "\n"


def derive_description(profile: Mapping[str, Any], role_wiring: Mapping[str, Any]) -> str:
    prefix = str(role_wiring.get("description_prefix", "")).strip()
    summary = str(profile.get("summary", "")).strip()
    if prefix and summary:
        return f"{prefix} {summary}"
    if summary:
        return summary
    if prefix:
        return prefix
    return f"AoA {profile['name']} role."


def build_agents(
    profiles_root: Path,
    wiring: Mapping[str, Any],
) -> list[dict[str, Any]]:
    profiles = load_active_profiles(profiles_root)
    source_root = profiles_root.parent
    agents: list[dict[str, Any]] = []
    for profile_path in iter_profiles(profiles_root):
        payload = read_json(profile_path)
        if str(payload.get("status", "active")) != "active":
            continue
        profile = profiles[str(payload["name"])]
        role_key = normalize_role_key(profile)
        role_wiring = dict((wiring.get("roles") or {}).get(role_key, {}))
        agent = {
            "name": str(profile["name"]),
            "description": derive_description(profile, role_wiring),
            "sandbox_mode": role_wiring.get("sandbox_mode"),
            "nickname_candidates": list(role_wiring.get("nickname_candidates", [])),
            "mcp_affinity": list(role_wiring.get("mcp_affinity", [])),
            "model": role_wiring.get("model"),
            "model_reasoning_effort": role_wiring.get("model_reasoning_effort"),
            "developer_instructions": build_developer_instructions(profile, role_wiring),
            "source_profile": path_reference(profile_path, source_root),
            "role_key": role_key,
        }
        agents.append(agent)
    return agents


def toml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_toml(agent: Mapping[str, Any]) -> str:
    lines = [
        f"name = {toml_string(str(agent['name']))}",
        f"description = {toml_string(str(agent['description']))}",
    ]
    sandbox_mode = agent.get("sandbox_mode")
    if sandbox_mode:
        lines.append(f"sandbox_mode = {toml_string(str(sandbox_mode))}")
    model = agent.get("model")
    if model:
        lines.append(f"model = {toml_string(str(model))}")
    reasoning_effort = agent.get("model_reasoning_effort")
    if reasoning_effort:
        lines.append(f"model_reasoning_effort = {toml_string(str(reasoning_effort))}")
    nicknames = [str(item) for item in agent.get("nickname_candidates", [])]
    if nicknames:
        rendered = ", ".join(toml_string(item) for item in nicknames)
        lines.append(f"nickname_candidates = [{rendered}]")
    lines.extend(
        [
            "developer_instructions = '''",
            str(agent["developer_instructions"]).rstrip(),
            "'''",
        ]
    )
    return "\n".join(lines) + "\n"


def render_config_snippet(
    agents: Sequence[Mapping[str, Any]],
    workspace_defaults: Mapping[str, Any],
    *,
    config_file_prefix: str = "agents",
) -> str:
    lines = [
        "[agents]",
        f"max_threads = {int(workspace_defaults.get('agents_max_threads', 4))}",
        f"max_depth = {int(workspace_defaults.get('agents_max_depth', 1))}",
        f"job_max_runtime_seconds = {int(workspace_defaults.get('agents_job_max_runtime_seconds', 1800))}",
        "",
    ]
    for agent in agents:
        name = str(agent["name"])
        lines.append(f"[agents.{name}]")
        lines.append(f"description = {toml_string(str(agent['description']))}")
        lines.append(f'config_file = {toml_string(f"{config_file_prefix}/{name}.toml")}')
        nicknames = [str(item) for item in agent.get("nickname_candidates", [])]
        if nicknames:
            rendered = ", ".join(toml_string(item) for item in nicknames)
            lines.append(f"nickname_candidates = [{rendered}]")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_manifest(
    agents: Sequence[Mapping[str, Any]],
    wiring: Mapping[str, Any],
    *,
    config_file_prefix: str = "agents",
) -> dict[str, Any]:
    return {
        "version": 2,
        "wiring_version": wiring.get("version", 2),
        "workspace_defaults": wiring.get("workspace_defaults", {}),
        "config_file_prefix": config_file_prefix,
        "generated_agents": [
            {
                "name": agent["name"],
                "description": agent["description"],
                "sandbox_mode": agent.get("sandbox_mode"),
                "nickname_candidates": agent.get("nickname_candidates", []),
                "mcp_affinity": agent.get("mcp_affinity", []),
                "config_path": f"{config_file_prefix}/{agent['name']}.toml",
                "source_profile": agent["source_profile"],
                "role_key": agent["role_key"],
            }
            for agent in agents
        ],
    }


def build_projection_file_texts(
    profiles_root: Path,
    wiring: Mapping[str, Any],
    agents_dir: Path,
    config_snippet_path: Path,
    manifest_path: Path,
    *,
    config_file_prefix: str = "agents",
) -> dict[Path, str]:
    agents = build_agents(profiles_root, wiring)
    if not agents:
        raise BuildError(f"no active profiles found under {profiles_root}")
    texts: dict[Path, str] = {}
    for agent in agents:
        texts[agents_dir / f"{agent['name']}.toml"] = render_toml(agent)
    texts[config_snippet_path] = render_config_snippet(
        agents,
        wiring.get("workspace_defaults", {}),
        config_file_prefix=config_file_prefix,
    )
    texts[manifest_path] = json.dumps(
        build_manifest(agents, wiring, config_file_prefix=config_file_prefix),
        indent=2,
        ensure_ascii=False,
    ) + "\n"
    return texts


def write_if_changed(path: Path, content: str, *, check: bool) -> bool:
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
        if check:
            raise BuildError(f"{path} is out of date")
    elif check:
        raise BuildError(f"{path} is missing")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def write_projection_file_texts(texts: Mapping[Path, str], *, check: bool) -> bool:
    changed = False
    for path, content in texts.items():
        changed |= write_if_changed(path, content, check=check)
    return changed


def write_repo_projection_surfaces(*, check: bool = False) -> dict[str, Any]:
    wiring = load_wiring(WIRING_CONFIG_PATH)
    texts = build_projection_file_texts(
        PROFILES_DIR,
        wiring,
        GENERATED_AGENTS_DIR,
        GENERATED_CONFIG_SNIPPET_PATH,
        GENERATED_MANIFEST_PATH,
    )
    write_projection_file_texts(texts, check=check)
    return build_manifest(build_agents(PROFILES_DIR, wiring), wiring)


def validate_agent_file(path: Path, *, expected_sandbox: str | None) -> list[str]:
    errors: list[str] = []
    try:
        payload = read_toml(path)
    except BuildError as exc:
        return [str(exc)]

    for key in REQUIRED_AGENT_KEYS:
        if key not in payload:
            errors.append(f"{path}: missing required key {key!r}")

    name = str(payload.get("name", "")).strip()
    if name and path.stem != name:
        errors.append(f"{path}: filename stem does not match agent name {name!r}")

    nicknames = payload.get("nickname_candidates")
    if nicknames is not None:
        if not isinstance(nicknames, list) or not nicknames:
            errors.append(f"{path}: nickname_candidates must be a non-empty list when present")
        elif len(nicknames) != len(set(nicknames)):
            errors.append(f"{path}: nickname_candidates contains duplicates")

    sandbox_mode = payload.get("sandbox_mode")
    if sandbox_mode is not None and sandbox_mode not in VALID_SANDBOX_MODES:
        errors.append(f"{path}: invalid sandbox_mode {sandbox_mode!r}")
    if expected_sandbox and sandbox_mode != expected_sandbox:
        errors.append(f"{path}: sandbox_mode {sandbox_mode!r} != expected {expected_sandbox!r}")

    instructions = str(payload.get("developer_instructions", ""))
    if instructions and "General discipline" not in instructions:
        errors.append(f"{path}: developer_instructions missing 'General discipline' section")
    if instructions and "MCP affinity" not in instructions:
        errors.append(f"{path}: developer_instructions missing 'MCP affinity' section")

    return errors


def collect_projection_validation_errors(
    profiles_root: Path,
    wiring_path: Path,
    agents_dir: Path,
    config_snippet_path: Path,
    *,
    manifest_path: Path | None = None,
) -> list[str]:
    wiring = load_wiring(wiring_path)
    profiles = load_active_profiles(profiles_root)
    errors: list[str] = []
    agent_files = sorted(agents_dir.glob("*.toml"))
    if not agent_files:
        errors.append(f"{agents_dir}: no agent files found")

    seen_names: set[str] = set()
    for agent_path in agent_files:
        try:
            payload = read_toml(agent_path)
        except BuildError as exc:
            errors.append(str(exc))
            continue
        name = str(payload.get("name", "")).strip()
        profile = profiles.get(name)
        role_key = normalize_role_key(profile) if profile is not None else name
        expected_sandbox = ((wiring.get("roles") or {}).get(role_key) or {}).get("sandbox_mode")
        errors.extend(validate_agent_file(agent_path, expected_sandbox=expected_sandbox))
        if name in seen_names:
            errors.append(f"{agent_path}: duplicate agent name {name!r}")
        seen_names.add(name)
        if name not in profiles:
            errors.append(f"{agent_path}: no matching active profile named {name!r}")

    try:
        config = read_toml(config_snippet_path)
    except BuildError as exc:
        errors.append(str(exc))
        config = {}

    agents_table = config.get("agents", {}) if isinstance(config, Mapping) else {}
    if not isinstance(agents_table, dict):
        errors.append(f"{config_snippet_path}: missing [agents] table")
        agents_table = {}

    for key in ("max_threads", "max_depth", "job_max_runtime_seconds"):
        if key not in agents_table:
            errors.append(f"{config_snippet_path}: [agents] missing {key}")

    for name, profile in sorted(profiles.items()):
        entry = agents_table.get(name)
        if entry is None:
            errors.append(f"{config_snippet_path}: missing [agents.{name}] entry")
            continue
        if not isinstance(entry, dict):
            errors.append(f"{config_snippet_path}: [agents.{name}] must be a table")
            continue
        config_file = entry.get("config_file")
        if not isinstance(config_file, str):
            errors.append(f"{config_snippet_path}: [agents.{name}] missing config_file")
        else:
            resolved = config_snippet_path.parent / config_file
            fallback = agents_dir / f"{name}.toml"
            if not resolved.exists() and not fallback.exists():
                errors.append(
                    f"{config_snippet_path}: config_file for {name!r} points at missing file {config_file!r}"
                )
        role_key = normalize_role_key(profile)
        expected_nicknames = list(((wiring.get("roles") or {}).get(role_key) or {}).get("nickname_candidates", []))
        nicknames = entry.get("nickname_candidates")
        if expected_nicknames and nicknames != expected_nicknames:
            errors.append(
                f"{config_snippet_path}: [agents.{name}] nickname_candidates do not match projection wiring"
            )

    if seen_names != set(profiles):
        missing = sorted(set(profiles) - seen_names)
        extra = sorted(seen_names - set(profiles))
        if missing:
            errors.append(f"generated agents missing active profiles: {', '.join(missing)}")
        if extra:
            errors.append(f"generated agents without matching profiles: {', '.join(extra)}")

    if manifest_path is not None:
        try:
            manifest_payload = read_json(manifest_path)
        except BuildError as exc:
            errors.append(str(exc))
        else:
            if not isinstance(manifest_payload, Mapping):
                errors.append(f"{manifest_path}: manifest must contain a JSON object")
            else:
                generated_agents = manifest_payload.get("generated_agents")
                if not isinstance(generated_agents, list):
                    errors.append(f"{manifest_path}: generated_agents must be a list")
                else:
                    config_file_prefix = str(manifest_payload.get("config_file_prefix", "agents"))
                    manifest_names = set()
                    manifest_by_name: dict[str, Mapping[str, Any]] = {}
                    for item in generated_agents:
                        if not isinstance(item, Mapping):
                            errors.append(f"{manifest_path}: generated_agents entries must be objects")
                            continue
                        name = str(item.get("name", "")).strip()
                        if not name:
                            errors.append(f"{manifest_path}: generated_agents entry missing name")
                            continue
                        manifest_names.add(name)
                        manifest_by_name[name] = item
                    if manifest_names != set(profiles):
                        errors.append(f"{manifest_path}: generated_agents do not match active profiles")
                    for name, profile in sorted(profiles.items()):
                        entry = manifest_by_name.get(name)
                        if entry is None:
                            continue
                        role_key = normalize_role_key(profile)
                        role_wiring = dict((wiring.get("roles") or {}).get(role_key, {}))
                        if entry.get("role_key") != role_key:
                            errors.append(
                                f"{manifest_path}: generated_agents[{name!r}] role_key does not match profile wiring"
                            )
                        if entry.get("sandbox_mode") != role_wiring.get("sandbox_mode"):
                            errors.append(
                                f"{manifest_path}: generated_agents[{name!r}] sandbox_mode does not match projection wiring"
                            )
                        if entry.get("nickname_candidates") != list(
                            role_wiring.get("nickname_candidates", [])
                        ):
                            errors.append(
                                f"{manifest_path}: generated_agents[{name!r}] nickname_candidates do not match projection wiring"
                            )
                        if entry.get("mcp_affinity") != list(role_wiring.get("mcp_affinity", [])):
                            errors.append(
                                f"{manifest_path}: generated_agents[{name!r}] mcp_affinity does not match projection wiring"
                            )
                        expected_config_path = f"{config_file_prefix}/{name}.toml"
                        if entry.get("config_path") != expected_config_path:
                            errors.append(
                                f"{manifest_path}: generated_agents[{name!r}] config_path must be {expected_config_path!r}"
                            )
                        expected_source = path_reference(
                            profiles_root / f"{name}.profile.json",
                            profiles_root.parent,
                        )
                        if entry.get("source_profile") != expected_source:
                            errors.append(
                                f"{manifest_path}: generated_agents[{name!r}] source_profile does not match active profile path"
                            )

    return errors


def collect_repo_projection_errors() -> list[str]:
    try:
        wiring = load_wiring(WIRING_CONFIG_PATH)
        expected = build_projection_file_texts(
            PROFILES_DIR,
            wiring,
            GENERATED_AGENTS_DIR,
            GENERATED_CONFIG_SNIPPET_PATH,
            GENERATED_MANIFEST_PATH,
        )
    except BuildError as exc:
        return [str(exc)]
    errors: list[str] = []
    for path, content in expected.items():
        if not path.exists():
            errors.append(f"missing required file: {path_reference(path, REPO_ROOT)}")
            continue
        current = path.read_text(encoding="utf-8")
        if current != content:
            errors.append(f"{path_reference(path, REPO_ROOT)} drifted from source-authored profiles and wiring")
    errors.extend(
        collect_projection_validation_errors(
            PROFILES_DIR,
            WIRING_CONFIG_PATH,
            GENERATED_AGENTS_DIR,
            GENERATED_CONFIG_SNIPPET_PATH,
            manifest_path=GENERATED_MANIFEST_PATH,
        )
    )
    return errors
