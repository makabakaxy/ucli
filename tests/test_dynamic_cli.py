from __future__ import annotations

import unittest
from unittest.mock import patch

from click.testing import CliRunner

from ucli.main import cli


class DynamicCliTests(unittest.TestCase):
    def test_unknown_top_level_command_falls_back_to_dynamic_handler(self) -> None:
        runner = CliRunner()

        with patch("ucli.main._handle_dynamic_command") as handler:
            result = runner.invoke(cli, ["jira", "project", "list"])

        self.assertEqual(result.exit_code, 0)
        handler.assert_called_once_with(["jira", "project", "list"])


if __name__ == "__main__":
    unittest.main()
