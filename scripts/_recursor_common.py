from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FORBIDDEN = {
    "global": {
        "spawn_agent",
        "open_arena_session",
        "issue_verdict",
        "write_scar",
        "mutate_rank",
        "promote_to_tree_of_sophia",
        "hidden_scheduler_action",
    },
    "recursor.witness": {
        "close_review_decision",
        "apply_patch",
    },
    "recursor.executor": {
        "execute_without_approved_plan",
        "self_verify_final_truth",
    },
}

STOP_LINES = [
    "no_arena_session",
    "no_verdict",
    "no_scar_write",
    "no_rank_mutation",
    "no_assistant_contestant_drift",
    "no_hidden_scheduler",
    "no_tos_promotion",
    "no_codex_projection_absorption",
]

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def min_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n", encoding="utf-8")

def stable_hash(payload: Any) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()

def role_map(role_set: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    roles = role_set.get("roles", [])
    return {role.get("recursor_id", ""): role for role in roles if isinstance(role, dict)}

def validate_role_contract(role: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors: List[Dict[str, Any]] = []
    rid = role.get("recursor_id", "<missing>")
    def add(kind: str, message: str, severity: str = "critical") -> None:
        errors.append({"kind": kind, "severity": severity, "recursor_id": rid, "message": message})

    if role.get("schema_version") != "recursor-role-contract/v1":
        add("invalid_schema_version", "Role must use recursor-role-contract/v1.")
    if role.get("owner_repo") != "aoa-agents":
        add("invalid_owner", "Role owner_repo must be aoa-agents.")
    if role.get("readiness_status") != "candidate":
        add("not_readiness_candidate", "This seed allows only readiness_status=candidate.")
    form = role.get("default_form", {})
    if form.get("kind") != "assistant":
        add("not_assistant_default_form", "Recursor default form must be assistant in this seed.")
    if form.get("arena_eligible") is not False:
        add("assistant_arena_eligible", "Assistant recursors must not be arena eligible.")
    future = role.get("future_agonic_candidate", {})
    if future.get("enabled") is not False or future.get("live_authority") is not False:
        add("agonic_candidate_enabled", "Future agonic candidate must be disabled and non-live.")
    projection = role.get("codex_projection", {})
    if projection.get("status") != "candidate_only":
        add("projection_not_candidate_only", "Codex projection must be candidate_only.")
    if projection.get("install_by_default") is not False:
        add("projection_install_by_default", "Codex projection candidates must not install by default.")
    if projection.get("requires_owner_review") is not True:
        add("projection_lacks_owner_review", "Codex projection candidate requires owner review.")
    if role.get("receipts_required") is not True:
        add("receipts_not_required", "Recursor role must require receipts.")
    memory = role.get("memory_policy", {})
    if memory.get("direct_durable_write_allowed") is not False:
        add("durable_memory_write_allowed", "Recursor cannot directly write durable memory.")
    forbidden = set(role.get("forbidden_actions", []))
    missing = REQUIRED_FORBIDDEN["global"] - forbidden
    missing |= REQUIRED_FORBIDDEN.get(rid, set()) - forbidden
    if missing:
        add("missing_forbidden_actions", f"Missing forbidden actions: {sorted(missing)}")
    stop_lines = set(role.get("stop_lines", []))
    if "projection_candidate_is_not_install" not in stop_lines:
        add("missing_projection_stop_line", "Missing projection_candidate_is_not_install stop-line.")
    if "assistant_is_not_contestant" not in stop_lines:
        add("missing_assistant_stop_line", "Missing assistant_is_not_contestant stop-line.")
    return errors

def validate_pair_contract(pair: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors: List[Dict[str, Any]] = []
    def add(kind: str, message: str, severity: str = "critical") -> None:
        errors.append({"kind": kind, "severity": severity, "message": message})
    if pair.get("schema_version") != "recursor-pair-contract/v1":
        add("invalid_pair_schema", "Pair must use recursor-pair-contract/v1.")
    roles = pair.get("roles", {})
    if roles.get("witness") != "recursor.witness" or roles.get("executor") != "recursor.executor":
        add("invalid_pair_roles", "Pair must bind recursor.witness and recursor.executor.")
    if pair.get("activation_status") != "readiness_only":
        add("pair_not_readiness_only", "Pair activation must remain readiness_only.")
    required = set(pair.get("required_separation", []))
    must = {
        "witness_cannot_apply_mutations",
        "executor_cannot_close_review",
        "executor_cannot_self_verify_without_external_check",
        "neither_can_spawn_additional_agents",
    }
    missing = must - required
    if missing:
        add("missing_pair_separation", f"Missing pair separation law: {sorted(missing)}")
    return errors

def validate_projection_candidate(projection: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors: List[Dict[str, Any]] = []
    def add(kind: str, message: str, severity: str = "critical") -> None:
        errors.append({"kind": kind, "severity": severity, "message": message})
    if projection.get("schema_version") != "codex-recursor-projection-candidate/v1":
        add("invalid_projection_schema", "Projection must use codex-recursor-projection-candidate/v1.")
    if projection.get("projection_status") != "candidate_only":
        add("projection_not_candidate_only", "Projection status must stay candidate_only.")
    if projection.get("install_by_default") is not False:
        add("projection_install_by_default", "Projection candidates must not install by default.")
    if projection.get("requires_owner_review") is not True:
        add("projection_lacks_owner_review", "Projection candidate requires owner review.")
    agents = projection.get("candidate_agents", [])
    if len(agents) < 2:
        add("missing_candidate_agents", "Projection candidate should include witness and executor.")
    by_id = {agent.get("recursor_id"): agent for agent in agents if isinstance(agent, dict)}
    for rid in ("recursor.witness", "recursor.executor"):
        if rid not in by_id:
            add("missing_projection_agent", f"Missing projection candidate for {rid}.")
            continue
        agent = by_id[rid]
        forbidden = set(agent.get("forbidden", []))
        required_tokens = {"agent_spawn", "arena_session", "verdict", "scar_write", "hidden_scheduler"}
        missing = required_tokens - forbidden
        if missing:
            add("projection_missing_forbidden", f"{rid} projection missing forbidden tokens: {sorted(missing)}")
        if agent.get("activation_status") != "candidate_only":
            add("projection_agent_not_candidate_only", f"{rid} must remain candidate_only.")
    return errors

def build_readiness_index(root: Path = ROOT) -> Dict[str, Any]:
    roles = read_json(root / "config" / "recursor_roles.seed.json")
    pair = read_json(root / "config" / "recursor_pair.seed.json")
    projection = read_json(root / "config" / "codex_recursor_projection.candidate.json")
    role_errors = []
    for role in roles.get("roles", []):
        role_errors.extend(validate_role_contract(role))
    pair_errors = validate_pair_contract(pair)
    projection_errors = validate_projection_candidate(projection)
    all_errors = role_errors + pair_errors + projection_errors
    index = {
        "schema_version": "recursor-readiness-index/v1",
        "generated_at": utc_now(),
        "owner_repo": "aoa-agents",
        "readiness_status": "candidate",
        "roles": [
            {
                "recursor_id": role["recursor_id"],
                "readiness_status": role.get("readiness_status"),
                "default_kind": role.get("default_form", {}).get("kind"),
                "arena_eligible": role.get("default_form", {}).get("arena_eligible"),
                "future_agonic_candidate_enabled": role.get("future_agonic_candidate", {}).get("enabled"),
                "codex_projection_status": role.get("codex_projection", {}).get("status"),
                "install_by_default": role.get("codex_projection", {}).get("install_by_default"),
                "forbidden_action_count": len(role.get("forbidden_actions", [])),
                "stop_lines": role.get("stop_lines", []),
            }
            for role in roles.get("roles", [])
        ],
        "pair_ref": pair.get("pair_ref"),
        "pair_activation_status": pair.get("activation_status"),
        "projection_status": projection.get("projection_status"),
        "projection_install_by_default": projection.get("install_by_default"),
        "boundary": {
            "status": "fail" if all_errors else "pass",
            "violations": all_errors,
            "checked_stop_lines": STOP_LINES,
        },
        "source_hashes": {
            "roles": stable_hash(roles),
            "pair": stable_hash(pair),
            "projection": stable_hash(projection),
        },
    }
    return index

def build_boundary_report(root: Path = ROOT) -> Dict[str, Any]:
    roles = read_json(root / "config" / "recursor_roles.seed.json")
    pair = read_json(root / "config" / "recursor_pair.seed.json")
    projection = read_json(root / "config" / "codex_recursor_projection.candidate.json")
    violations: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    for role in roles.get("roles", []):
        violations.extend(validate_role_contract(role))
    violations.extend(validate_pair_contract(pair))
    violations.extend(validate_projection_candidate(projection))

    if projection.get("install_by_default") is False:
        warnings.append({
            "kind": "projection_candidate_not_installed",
            "severity": "info",
            "message": "Expected: recursor projection remains disabled by default."
        })

    generated_trial = root / "generated" / "agent_formation_trial.min.json"
    if generated_trial.exists():
        try:
            trial = read_json(generated_trial)
            warnings.append({
                "kind": "formation_trial_seen",
                "severity": "info",
                "message": "Existing formation-trial index was observed but not consumed as recursor runtime truth.",
                "source": str(generated_trial.relative_to(root)),
                "source_hash": stable_hash(trial)
            })
        except SystemExit:
            warnings.append({
                "kind": "formation_trial_unreadable",
                "severity": "warning",
                "message": "Formation trial file exists but could not be read."
            })

    report = {
        "schema_version": "recursor-boundary-report/v1",
        "generated_at": utc_now(),
        "owner_repo": "aoa-agents",
        "status": "fail" if violations else "pass",
        "violations": violations,
        "warnings": warnings,
        "checked_stop_lines": STOP_LINES,
        "forbidden_effects": sorted(REQUIRED_FORBIDDEN["global"]),
        "summary": {
            "role_count": len(roles.get("roles", [])),
            "projection_status": projection.get("projection_status"),
            "pair_activation_status": pair.get("activation_status"),
            "readiness_only": pair.get("activation_status") == "readiness_only",
        },
    }
    return report
