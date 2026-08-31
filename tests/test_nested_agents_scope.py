from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / 'scripts' / 'validate_nested_agents.py'
SPEC = importlib.util.spec_from_file_location('validate_nested_agents_scope', VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class NestedAgentsScopeTests(unittest.TestCase):
    def test_dependency_and_tool_state_markdown_is_not_owner_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            included = root / 'docs' / 'AGENTS.md'
            included.parent.mkdir(parents=True)
            included.write_text('# AGENTS.md\n', encoding='utf-8')

            for directory in VALIDATOR.IGNORED_DIRS:
                ignored = root / directory / 'foreign' / 'AGENTS.md'
                ignored.parent.mkdir(parents=True)
                ignored.write_text('```bash\npython foreign.py\n```\n', encoding='utf-8')

            discovered = {
                path.relative_to(root).as_posix()
                for path in VALIDATOR._iter_owned_markdown(root, 'AGENTS.md')
            }

            self.assertEqual(discovered, {'docs/AGENTS.md'})

    def test_authored_dot_agents_tree_remains_in_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            authored = root / '.agents' / 'AGENTS.md'
            authored.parent.mkdir(parents=True)
            authored.write_text('# AGENTS.md\n', encoding='utf-8')

            discovered = {
                path.relative_to(root).as_posix()
                for path in VALIDATOR._iter_owned_markdown(root, 'AGENTS.md')
            }

            self.assertEqual(discovered, {'.agents/AGENTS.md'})


if __name__ == '__main__':
    unittest.main()
