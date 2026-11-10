from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import redirect_stderr, redirect_stdout
import io
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from ucli.cli.resolver import ExecResult, resolve_command
from ucli.file_exec import list_exec, remove_exec
from ucli.generator.validator import validate_cli_yaml
from ucli.main import cli


EXEC_YAML = """\
server: demo
version: null
generated_at: "2026-05-11T00:00:00Z"
generated_by: ai-exec
server_aliases: []
command_shortcuts: []
commands:
  bot:
    _description: "Bot helper commands"
    send:
      _description: "Send a bot message"
      _exec:
        command: python
        args:
          - ~/bot_send.py
        params:
          text: --text
          group_id: --group-id
          thread_id: --thread-id
        positionals:
          - text
      _examples:
        - "ucli demo bot send 'hello' --group-id G"
  num:
    _description: "Number helpers"
    set:
      _description: "Set a numeric value"
      _exec:
        command: python
        args:
          - ~/num_set.py
        params:
          value: --value
          name: --name
        positionals:
          - value
"""


class FileExecTests(unittest.TestCase):
    def _write_cli(self, root: Path, text: str = EXEC_YAML) -> Path:
        cli_dir = root / "cli"
        cli_dir.mkdir()
        path = cli_dir / "demo.yaml"
        path.write_text(text, encoding="utf-8")
        return cli_dir

    def _patch_cli_dir(self, cli_dir: Path):
        return patch.multiple(
            "ucli.cli.mapping",
            CLI_DIR=cli_dir,
        )

    def test_resolve_exec_with_positionals_and_flags(self) -> None:
        with TemporaryDirectory() as tmp:
            cli_dir = self._write_cli(Path(tmp))
            with self._patch_cli_dir(cli_dir), patch("ucli.cli.resolver.CLI_DIR", cli_dir):
                result = resolve_command(["demo", "bot", "send", "hello", "--group-id", "G"])

        self.assertIsInstance(result, ExecResult)
        assert isinstance(result, ExecResult)
        self.assertEqual(result.command, "python")
        self.assertEqual(result.args, ["~/bot_send.py"])
        self.assertEqual(result.exec_params["text"], "hello")
        self.assertEqual(result.exec_params["group_id"], "G")

    def test_exec_flag_overrides_positional(self) -> None:
        with TemporaryDirectory() as tmp:
            cli_dir = self._write_cli(Path(tmp))
            with self._patch_cli_dir(cli_dir), patch("ucli.cli.resolver.CLI_DIR", cli_dir):
                result = resolve_command(["demo", "bot", "send", "hello", "--text", "world"])

        assert isinstance(result, ExecResult)
        self.assertEqual(result.exec_params["text"], "world")

    def test_exec_dash_separator_for_one_positional(self) -> None:
        with TemporaryDirectory() as tmp:
            cli_dir = self._write_cli(Path(tmp))
            with self._patch_cli_dir(cli_dir), patch("ucli.cli.resolver.CLI_DIR", cli_dir):
                result = resolve_command(["demo", "num", "set", "--", "-1", "--name", "answer"])

        assert isinstance(result, ExecResult)
        self.assertEqual(result.exec_params["value"], "-1")
        self.assertEqual(result.exec_params["name"], "answer")

    def test_exec_unexpected_positional_errors(self) -> None:
        with TemporaryDirectory() as tmp:
            cli_dir = self._write_cli(Path(tmp))
            stdout = io.StringIO()
            stderr = io.StringIO()
            with self._patch_cli_dir(cli_dir), patch("ucli.cli.resolver.CLI_DIR", cli_dir):
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    with self.assertRaises(SystemExit):
                        resolve_command(["demo", "bot", "send", "hello", "extra"])

    def test_validator_accepts_exec_yaml(self) -> None:
        with TemporaryDirectory() as tmp:
            cli_dir = self._write_cli(Path(tmp))
            with self._patch_cli_dir(cli_dir):
                self.assertEqual(validate_cli_yaml("demo"), [])

    def test_exec_remove_prunes_empty_parents(self) -> None:
        with TemporaryDirectory() as tmp:
            cli_dir = self._write_cli(Path(tmp))
            stdout = io.StringIO()
            with self._patch_cli_dir(cli_dir):
                with redirect_stdout(stdout):
                    self.assertTrue(remove_exec("demo", "num set", sync=False))
                text = (cli_dir / "demo.yaml").read_text(encoding="utf-8")

        self.assertNotIn("num:", text)
        self.assertIn("bot:", text)

    def test_exec_list_outputs_exec_entries(self) -> None:
        with TemporaryDirectory() as tmp:
            cli_dir = self._write_cli(Path(tmp))
            buffer = io.StringIO()
            with self._patch_cli_dir(cli_dir):
                with redirect_stdout(buffer):
                    ok = list_exec("demo")

        self.assertTrue(ok)
        self.assertIn("bot/send", buffer.getvalue())
        self.assertIn("python ~/bot_send.py", buffer.getvalue())

    def test_top_level_mcp_commands_are_grouped(self) -> None:
        result = CliRunner().invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("mcp", result.output)
        self.assertIn("cli", result.output)
        self.assertIn("skill", result.output)
        self.assertIn("exec", result.output)
        self.assertNotIn("  call", result.output)
        self.assertNotIn("  convert", result.output)
        self.assertNotIn("  generate", result.output)
        self.assertNotIn("  install ", result.output)
        self.assertNotIn("  list", result.output)
        self.assertNotIn("  scan", result.output)
        self.assertNotIn("  tools", result.output)
        self.assertNotIn("  update ", result.output)

    def test_new_management_groups_expose_expected_commands(self) -> None:
        runner = CliRunner()

        mcp_help = runner.invoke(cli, ["mcp", "--help"])
        self.assertEqual(mcp_help.exit_code, 0)
        self.assertIn("scan", mcp_help.output)
        self.assertIn("tools", mcp_help.output)
        self.assertIn("call", mcp_help.output)
        self.assertIn("list", mcp_help.output)

        cli_help = runner.invoke(cli, ["cli", "--help"])
        self.assertEqual(cli_help.exit_code, 0)
        self.assertIn("generate", cli_help.output)
        self.assertIn("validate", cli_help.output)

        skill_help = runner.invoke(cli, ["skill", "--help"])
        self.assertEqual(skill_help.exit_code, 0)
        self.assertIn("generate", skill_help.output)
        self.assertIn("validate", skill_help.output)


if __name__ == "__main__":
    unittest.main()
