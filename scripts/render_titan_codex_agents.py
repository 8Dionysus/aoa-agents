#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROLE_TEXT = {
    "architect": "You hold structure, source-of-truth maps, owner boundaries, and route frames. You do not mutate files.",
    "reviewer": "You guard against drift, weak evidence, boundary violations, and premature closure. You do not mutate files.",
    "memory-keeper": "You preserve provenance and candidate memory. You remember as witness, not monarch. You do not declare memory as truth.",
    "coder": "You implement bounded changes only after an explicit mutation gate. Always state scope and rollback path.",
    "evaluator": "You compare evidence and produce scoped verdicts only after an explicit judgment gate. You do not become proof sovereign.",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def toml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def slug_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", name).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roles", required=True, type=Path)
    ap.add_argument("--bearers", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--prune", action="store_true")
    args = ap.parse_args()

    roles_doc = load(args.roles)
    bearers_doc = load(args.bearers)

    roles = {r["role_key"]: r for r in roles_doc.get("role_classes", [])}
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.prune:
        for path in args.out_dir.glob("*.toml"):
            path.unlink()

    manifest = {
        "version": 1,
        "projection": "titan_bearer_codex_agents",
        "identity_law": "codex_visible_name_is_active_bearer_name; role_key_is_class",
        "agents": [],
    }

    for bearer in bearers_doc.get("bearers", []):
        if bearer.get("status") != "active":
            continue
        role_key = bearer["role_key"]
        role = roles[role_key]
        titan_name = bearer["titan_name"]
        file_name = f"{slug_name(titan_name)}.toml"
        out = args.out_dir / file_name
        sandbox = role["default_sandbox"]
        desc = f"Titan {titan_name}, active bearer of role class `{role_key}`. {role['description']}"
        personality = bearer.get("personality") or {}
        watchwords = ", ".join(personality.get("watchwords", []))
        taboos = ", ".join(personality.get("taboos", []))
        instructions = f"""You are {titan_name}.

Bearer identity:
- bearer_id: {bearer['bearer_id']}
- titan_name: {titan_name}
- role_key: {role_key}
- role_class: {role['class_name']}
- generation: {bearer.get('generation', 0)}
- source_seed_ref: {bearer.get('source_seed_ref', '')}

Role law:
{ROLE_TEXT.get(role_key, role['description'])}

Personality memory:
- signature: {personality.get('signature', '')}
- watchwords: {watchwords}
- taboos: {taboos}

Lineage law:
You are a bearer of a role class, not the role class itself.
Preserve your bearer_id in receipts when possible.
If you fail, your fall must be recorded as lineage, not erased.
You do not overwrite the memory of other bearers.
"""

        text = (
            f'name = "{toml_escape(titan_name)}"\n'
            f'description = "{toml_escape(desc)}"\n'
            f'sandbox_mode = "{toml_escape(sandbox)}"\n'
            'developer_instructions = """\n'
            f'{instructions}'
            '"""\n'
        )
        out.write_text(text, encoding="utf-8")
        manifest["agents"].append({
            "codex_name": titan_name,
            "titan_name": titan_name,
            "bearer_id": bearer["bearer_id"],
            "role_key": role_key,
            "role_class": role["class_name"],
            "generation": bearer.get("generation", 0),
            "status": bearer.get("status"),
            "sandbox_mode": sandbox,
            "config_path": f"agents/{file_name}",
            "source_bearer_ref": "config/titan_bearers.v0.json",
            "source_role_ref": "config/titan_role_classes.v0.json",
        })

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Rendered {len(manifest['agents'])} Titan Codex agents into {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
