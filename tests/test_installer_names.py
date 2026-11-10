from __future__ import annotations

import unittest
from unittest.mock import patch

from click.testing import CliRunner

from ucli.converter.config_extractor import ServerNotFoundError
from ucli.installer.names import resolve_install_spec
from ucli.main import cli


class InstallNameTests(unittest.TestCase):
    def test_github_https_url_uses_last_segment_as_local_name(self) -> None:
        spec = resolve_install_spec("https://github.com/zereight/gitlab-mcp")

        self.assertEqual(spec.local_name, "gitlab-mcp")
        self.assertEqual(
            spec.lookup_names,
            (
                "https://github.com/zereight/gitlab-mcp",
                "zereight/gitlab-mcp",
                "zereight-gitlab-mcp",
                "gitlab-mcp",
            ),
        )

    def test_git_ssh_url_strips_git_suffix(self) -> None:
        spec = resolve_install_spec("git@github.com:zereight/gitlab-mcp.git")

        self.assertEqual(spec.local_name, "gitlab-mcp")
        self.assertIn("zereight-gitlab-mcp", spec.lookup_names)

    def test_plain_name_is_unchanged(self) -> None:
        spec = resolve_install_spec("mcp-atlassian")

        self.assertEqual(spec.local_name, "mcp-atlassian")
        self.assertEqual(spec.lookup_names, ("mcp-atlassian",))

    def test_owner_repo_keeps_owner_repo_lookup(self) -> None:
        spec = resolve_install_spec("zereight/gitlab-mcp")

        self.assertEqual(spec.local_name, "gitlab-mcp")
        self.assertEqual(
            spec.lookup_names,
            ("zereight/gitlab-mcp", "zereight-gitlab-mcp", "gitlab-mcp"),
        )


class InstallCommandNameTests(unittest.TestCase):
    def test_url_install_tries_preset_lookup_names_before_ai_search(self) -> None:
        runner = CliRunner()

        with (
            patch(
                "ucli.converter.config_extractor.extract_server_config",
                side_effect=ServerNotFoundError,
            ),
            patch(
                "ucli.main._try_preset_install",
                side_effect=[False, True],
            ) as preset_install,
            patch("ucli.installer.ai_search.ai_search_server") as ai_search,
        ):
            result = runner.invoke(
                cli,
                ["mcp", "install", "https://github.com/zereight/gitlab-mcp", "--yes"],
            )

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            [call.args[0] for call in preset_install.call_args_list],
            [
                "https://github.com/zereight/gitlab-mcp",
                "zereight/gitlab-mcp",
            ],
        )
        ai_search.assert_not_called()


if __name__ == "__main__":
    unittest.main()
