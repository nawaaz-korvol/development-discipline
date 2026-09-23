"""A push hook must never let disposable test repositories overwrite its caller."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HookIsolationTests(unittest.TestCase):
    """Exercise the real inherited Git environment against a disposable parent repo."""

    # Git exports repository selectors to hooks; fixture setup must clear them before Git writes.
    def test_fixture_suite_cannot_mutate_calling_repository(self) -> None:
        clean = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        with tempfile.TemporaryDirectory(prefix="discipline-hook-host-") as directory:
            root = Path(directory)

            def git(*args: str) -> str:
                return subprocess.run(["git", *args], cwd=root, env=clean, check=True,
                                      capture_output=True, text=True, encoding="utf-8").stdout.strip()

            git("init", "-b", "main")
            git("config", "user.name", "Hook Host")
            git("config", "user.email", "hook-host@example.invalid")
            git("config", "commit.gpgsign", "false")
            (root / "sentinel.txt").write_text("preserve the caller\n")
            git("add", ".")
            git("commit", "-m", "test: host baseline")
            head = git("rev-parse", "HEAD")
            inherited = dict(clean, GIT_DIR=str(root / ".git"), GIT_WORK_TREE=str(root),
                             GIT_INDEX_FILE=str(root / ".git/index"))
            result = subprocess.run([sys.executable, "-m", "unittest", "discover",
                                     "-s", str(ROOT / "tests"), "-p", "test_review_state.py"],
                                    cwd=ROOT, env=inherited, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(git("rev-parse", "HEAD"), head)
            self.assertEqual(git("config", "core.bare"), "false")
            self.assertEqual(git("config", "user.name"), "Hook Host")
            self.assertEqual(git("status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
