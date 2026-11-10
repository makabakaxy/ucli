from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ucli.installer.skill_sync import _copy_skill
from ucli.remover.cleaner import safe_remove_skill_dir


class SkillProtectionTests(unittest.TestCase):
    def test_copy_skill_preserves_target_scripts_and_users(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            target = root / "target"

            (source / "reference").mkdir(parents=True)
            (source / "scripts").mkdir()
            (source / "users").mkdir()
            (source / "SKILL.md").write_text("new skill\n", encoding="utf-8")
            (source / "reference" / "cmd.md").write_text("new ref\n", encoding="utf-8")
            (source / "scripts" / "generated.sh").write_text("managed\n", encoding="utf-8")
            (source / "users" / "skill.md").write_text("source user\n", encoding="utf-8")

            (target / "reference").mkdir(parents=True)
            (target / "scripts").mkdir()
            (target / "users").mkdir()
            (target / "SKILL.md").write_text("old skill\n", encoding="utf-8")
            (target / "reference" / "old.md").write_text("old ref\n", encoding="utf-8")
            (target / "scripts" / "local.sh").write_text("local\n", encoding="utf-8")
            (target / "users" / "skill.md").write_text("target user\n", encoding="utf-8")

            _copy_skill(source, target)

            self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "new skill\n")
            self.assertTrue((target / "reference" / "cmd.md").exists())
            self.assertFalse((target / "reference" / "old.md").exists())
            self.assertTrue((target / "scripts" / "local.sh").exists())
            self.assertFalse((target / "scripts" / "generated.sh").exists())
            self.assertEqual(
                (target / "users" / "skill.md").read_text(encoding="utf-8"),
                "target user\n",
            )

    def test_safe_remove_skill_dir_preserves_nonempty_protected_dirs(self) -> None:
        with TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "demo"
            (skill_dir / "reference").mkdir(parents=True)
            (skill_dir / "scripts").mkdir()
            (skill_dir / "users").mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo\n---\n# Demo\n",
                encoding="utf-8",
            )
            (skill_dir / "reference" / "cmd.md").write_text("ref\n", encoding="utf-8")
            (skill_dir / "scripts" / "local.sh").write_text("local\n", encoding="utf-8")
            (skill_dir / "users" / "skill.md").write_text("notes\n", encoding="utf-8")

            self.assertTrue(safe_remove_skill_dir(skill_dir, "demo"))

            self.assertFalse((skill_dir / "SKILL.md").exists())
            self.assertFalse((skill_dir / "reference").exists())
            self.assertTrue((skill_dir / "scripts" / "local.sh").exists())
            self.assertTrue((skill_dir / "users" / "skill.md").exists())


if __name__ == "__main__":
    unittest.main()
