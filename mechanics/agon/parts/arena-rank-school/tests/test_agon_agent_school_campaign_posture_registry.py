from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[5]
SCRIPT_DIR = ROOT / 'mechanics' / 'agon' / 'parts' / 'arena-rank-school' / 'scripts'
OUT = ROOT / 'mechanics/agon/parts/arena-rank-school/generated/school-campaign-posture-registry.min.json'
ITEM_KEY = 'agent_school_campaign_postures'
EXPECTED_COUNT = 10
UNIQUE_KEY_FIELD = 'posture_id'
REQUIRED_STOP_LINES = ['no_live_verdict_authority', 'no_durable_scar_write', 'no_retention_execution', 'no_rank_or_trust_mutation', 'no_tree_of_sophia_promotion', 'no_kag_promotion', 'no_hidden_scheduler_action', 'no_assistant_contestant_drift', 'no_auto_doctrine_rewrite', 'no_school_as_authority', 'no_lineage_as_canon', 'no_campaign_as_live_arena', 'no_center_takeover_of_owner_truth']
REQUIRED_FORBIDDEN = ['live_verdict_authority', 'durable_scar_write', 'retention_execution', 'rank_mutation', 'trust_mutation', 'tree_of_sophia_promotion', 'kag_promotion', 'hidden_scheduler_action', 'assistant_contestant_drift', 'auto_doctrine_rewrite', 'school_authority', 'lineage_canonization', 'live_campaign_arena']
SCHEMA_DIR = ROOT / 'mechanics' / 'agon' / 'parts' / 'arena-rank-school' / 'schemas'
ENTRY_SCHEMA = SCHEMA_DIR / 'school-campaign-posture.schema.json'
REGISTRY_SCHEMA = SCHEMA_DIR / 'school-campaign-posture-registry.schema.json'


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding='utf-8'))


class AgonAgentSchoolCampaignPostureRegistryTestCase(unittest.TestCase):
    def test_school_campaign_registry_shape(self) -> None:
        reg = load(OUT)
        self.assertEqual(reg['wave'], 'XVI')
        self.assertEqual(reg['wave_name'], 'Schools / Lineages / Campaigns')
        self.assertEqual(reg['runtime_posture'], 'candidate_only')
        self.assertEqual(reg['count'], EXPECTED_COUNT)
        self.assertEqual(len(reg[ITEM_KEY]), EXPECTED_COUNT)
        self.assertEqual(len(reg['digest']), 64)
        keys = set()
        for item in reg[ITEM_KEY]:
            self.assertEqual(item['wave'], 'XVI')
            self.assertIs(item['live_protocol'], False)
            self.assertEqual(item['authority_posture'], 'non_authority')
            self.assertEqual(item['review_status'], 'candidate_only')
            self.assertIs(item.get('assistant_contestant_allowed', False), False)
            self.assertLessEqual(set(REQUIRED_STOP_LINES), set(item['stop_lines']))
            self.assertLessEqual(set(REQUIRED_FORBIDDEN), set(item['forbidden_effects']))
            keys.add(item[UNIQUE_KEY_FIELD])
        self.assertEqual(len(keys), EXPECTED_COUNT)

    def test_builder_check_and_validator(self) -> None:
        build = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / 'build_agon_agent_school_campaign_posture_registry.py'), '--check'],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(build.returncode, 0)
        validate = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / 'validate_agon_agent_school_campaign_posture_registry.py')],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(validate.returncode, 0)

    def test_schemas_constrain_registry_and_entries(self) -> None:
        entry_schema = load(ENTRY_SCHEMA)
        registry_schema = load(REGISTRY_SCHEMA)
        entry_validator = Draft202012Validator(entry_schema)
        registry_validator = Draft202012Validator(registry_schema)
        reg = load(OUT)

        self.assertFalse(entry_validator.is_valid({}))
        self.assertFalse(registry_validator.is_valid({}))
        registry_validator.validate(reg)
        for item in reg[ITEM_KEY]:
            entry_validator.validate(item)

        bad_item = dict(reg[ITEM_KEY][0])
        bad_item['stop_lines'] = []
        self.assertFalse(entry_validator.is_valid(bad_item))
        bad_item = dict(reg[ITEM_KEY][0])
        bad_item['live_protocol'] = 'false'
        self.assertFalse(entry_validator.is_valid(bad_item))


if __name__ == '__main__':
    unittest.main()
