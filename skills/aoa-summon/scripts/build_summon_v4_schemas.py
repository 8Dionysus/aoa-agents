#!/usr/bin/env python3
"""Build evidence-complete summon v4 schemas from frozen v3 compatibility ABIs."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys
from typing import Any


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = BUNDLE_ROOT / "references"
REQUEST_V3 = REFERENCES / "summon-request-v3.schema.json"
RESULT_V3 = REFERENCES / "summon-result-v3.schema.json"
REQUEST_V4 = REFERENCES / "summon-request-v4.schema.json"
RESULT_V4 = REFERENCES / "summon-result-v4.schema.json"


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_bytes())
    if not isinstance(payload, dict):
        raise ValueError(f"schema must be an object: {path}")
    return payload


def _owner_content_ref(owner: str, schema_version: str) -> dict[str, Any]:
    return {
        "allOf": [
            {"$ref": "#/$defs/contentRef"},
            {
                "properties": {
                    "owner_repo": {"const": owner},
                    "schema_version": {"const": schema_version},
                }
            },
        ]
    }


def build_request_v4() -> dict[str, Any]:
    schema = copy.deepcopy(_load(REQUEST_V3))
    schema["$id"] = "https://example.invalid/aoa-summon/request-v4.schema.json"
    schema["title"] = "aoa-summon request v4"
    schema["$defs"]["responsibilityClassificationRef"] = _owner_content_ref(
        "aoa-agents", "responsibility-classification-v1"
    )
    schema["properties"]["responsibility_classification"] = {
        "additionalProperties": False,
        "properties": {
            "disposition": {"const": "not_independent", "type": "string"},
            "result_ref": {"$ref": "#/$defs/responsibilityClassificationRef"},
        },
        "required": ["disposition", "result_ref"],
        "type": "object",
    }
    schema["allOf"].append(
        {
            "if": {
                "properties": {
                    "summon_request": {
                        "properties": {
                            "transport_preference": {
                                "enum": ["codex_local", "either"]
                            }
                        },
                        "required": ["transport_preference"],
                    }
                },
                "required": ["summon_request"],
            },
            "then": {
                "properties": {
                    "responsibility_classification": {
                        "properties": {"disposition": {"const": "not_independent"}}
                    }
                },
                "required": ["responsibility_classification"],
            },
        }
    )
    external = schema["properties"]["external_incarnation"]
    evidence_fields = (
        "role_resolution_ref",
        "model_fit_query_result_ref",
        "model_fit_projection_ref",
        "model_realization_ref",
        "run_plan_ref",
    )
    required = external["required"]
    insertion = required.index("task_local_dag_ref")
    for field in reversed(evidence_fields):
        required.insert(insertion, field)
    external["properties"].update(
        {
            "role_resolution_ref": {"$ref": "#/$defs/roleResolutionRef"},
            "model_fit_query_result_ref": {"$ref": "#/$defs/modelFitQueryResultRef"},
            "model_fit_projection_ref": {"$ref": "#/$defs/modelFitProjectionRef"},
            "model_realization_ref": {"$ref": "#/$defs/modelRealizationRef"},
            "run_plan_ref": {"$ref": "#/$defs/runPlanRef"},
        }
    )
    schema["$defs"]["incarnationBindingRef"] = _owner_content_ref(
        "aoa-sdk", "aoa_agent_incarnation_binding_v2"
    )
    schema["$defs"].update(
        {
            "roleResolutionRef": _owner_content_ref(
                "aoa-agents", "aoa_role_resolution_v1"
            ),
            "modelFitQueryResultRef": _owner_content_ref(
                "aoa-models", "aoa_model_fit_query_result_v2"
            ),
            "modelFitProjectionRef": _owner_content_ref(
                "aoa-models", "aoa_model_fit_projection_v1"
            ),
            "modelRealizationRef": _owner_content_ref(
                "aoa-models", "aoa_model_realization_v1"
            ),
            "runPlanRef": _owner_content_ref("aoa-sdk", "aoa_control_plane_v1"),
        }
    )
    return schema


def _external_result_rule(schema: dict[str, Any]) -> dict[str, Any]:
    matches = [
        rule
        for rule in schema["allOf"]
        if rule.get("if", {}).get("properties", {}).get("lane")
        == {"const": "external_cli_reviewed"}
        and "incarnation_binding_ref"
        in rule.get("then", {})
        .get("properties", {})
        .get("binding", {})
        .get("properties", {})
    ]
    if len(matches) != 1:
        raise ValueError("v3 result must contain one external binding rule")
    return matches[0]


def build_result_v4() -> dict[str, Any]:
    schema = copy.deepcopy(_load(RESULT_V3))
    schema["$id"] = "https://example.invalid/aoa-summon/result-v4.schema.json"
    schema["title"] = "aoa-summon result v4"
    schema["$defs"]["runtimeProfileRef"] = _owner_content_ref(
        "abyss-stack", "abyss_stack_external_codex_runtime_profile_v2"
    )
    schema["$defs"]["runtimeResultRef"] = _owner_content_ref(
        "abyss-stack", "abyss_stack_external_codex_result_v2"
    )
    schema["$defs"]["incarnationBindingRef"] = _owner_content_ref(
        "aoa-sdk", "aoa_agent_incarnation_binding_v2"
    )
    schema["$defs"].update(
        {
            "roleResolutionRef": _owner_content_ref(
                "aoa-agents", "aoa_role_resolution_v1"
            ),
            "modelFitQueryResultRef": _owner_content_ref(
                "aoa-models", "aoa_model_fit_query_result_v2"
            ),
            "modelFitProjectionRef": _owner_content_ref(
                "aoa-models", "aoa_model_fit_projection_v1"
            ),
            "modelRealizationRef": _owner_content_ref(
                "aoa-models", "aoa_model_realization_v1"
            ),
            "runPlanRef": _owner_content_ref("aoa-sdk", "aoa_control_plane_v1"),
        }
    )
    binding = _external_result_rule(schema)["then"]["properties"]["binding"]
    binding["properties"].update(
        {
            "role_resolution_ref": {"$ref": "#/$defs/roleResolutionRef"},
            "model_fit_query_result_ref": {"$ref": "#/$defs/modelFitQueryResultRef"},
            "model_fit_projection_ref": {"$ref": "#/$defs/modelFitProjectionRef"},
            "model_realization_ref": {"$ref": "#/$defs/modelRealizationRef"},
            "run_plan_ref": {"$ref": "#/$defs/runPlanRef"},
        }
    )
    insertion = binding["required"].index("incarnation_binding_ref")
    for field in reversed(
        (
            "role_resolution_ref",
            "model_fit_query_result_ref",
            "model_fit_projection_ref",
            "model_realization_ref",
            "run_plan_ref",
        )
    ):
        binding["required"].insert(insertion, field)
    return schema


def _render(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = {
        REQUEST_V4: _render(build_request_v4()),
        RESULT_V4: _render(build_result_v4()),
    }
    if args.check:
        stale = [
            path
            for path, content in expected.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            for path in stale:
                print(f"ERROR: missing or stale {path.name}", file=sys.stderr)
            return 1
        print("OK: summon v4 schemas are current from frozen v3 compatibility ABIs")
        return 0
    for path, content in expected.items():
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(BUNDLE_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
