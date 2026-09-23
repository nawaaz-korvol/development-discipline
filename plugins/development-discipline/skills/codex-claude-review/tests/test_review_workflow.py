#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
REVIEW_SCRIPT = SKILL_ROOT / "scripts" / "run-claude-review.sh"


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(f"command failed: {command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


def metadata(stderr: str) -> dict[str, str]:
    return dict(re.findall(r"^([A-Z_]+)=(.+)$", stderr, flags=re.MULTILINE))


class ReviewWorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="codex-claude-review-test-")
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        run(["git", "init", "-b", "main"], cwd=self.repo)
        run(["git", "config", "user.name", "Skill Test"], cwd=self.repo)
        run(["git", "config", "user.email", "skill-test@example.invalid"], cwd=self.repo)
        (self.repo / "calculator.js").write_text(
            "export function multiply(left, right) {\n  return left * right;\n}\n",
            encoding="utf-8",
        )
        run(["git", "add", "calculator.js"], cwd=self.repo)
        run(["git", "commit", "-m", "test: initial fixture"], cwd=self.repo)
        (self.repo / "calculator.js").write_text(
            "export function multiply(left, right) {\n  return left * right;\n}\n\n"
            "export function add(left, right) {\n  return left - right;\n}\n",
            encoding="utf-8",
        )

        self.brief = self.root / "brief.md"
        self.brief.write_text(
            "Add an addition helper. Acceptance: add(2, 3) returns 5. Tests have not yet been added.",
            encoding="utf-8",
        )
        self.update = self.root / "update.md"
        self.update.write_text("The first finding was fixed and the implementation should be reviewed again.", encoding="utf-8")
        self.state_dir = self.root / "state"
        self.log = self.root / "claude-calls.jsonl"
        self.fake_claude = self.root / "fake-claude.py"
        self.fake_claude.write_text(
            textwrap.dedent(
                """\
                #!/usr/bin/env python3
                import json
                import os
                from pathlib import Path
                import sys

                log = Path(os.environ["FAKE_CLAUDE_LOG"])
                with log.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(sys.argv[1:]) + "\\n")
                print("P1 calculator.js:5 fake reviewer result")
                """
            ),
            encoding="utf-8",
        )
        self.fake_claude.chmod(0o755)
        self.env = os.environ.copy()
        self.env.update(
            {
                "CLAUDE_BIN": str(self.fake_claude),
                "CLAUDE_REVIEW_EFFORT": "low",
                "CODEX_CLAUDE_REVIEW_STATE_DIR": str(self.state_dir),
                "FAKE_CLAUDE_LOG": str(self.log),
            }
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def start_task(self, title: str = "Review calculator work", unit: str = "PR #1") -> subprocess.CompletedProcess[str]:
        return run(
            [
                str(REVIEW_SCRIPT),
                "start",
                "--task-title",
                title,
                "--objective",
                "Deliver a correct calculator helper",
                "--completion",
                "The helper is correct and the review is clean",
                "--unit",
                unit,
                "--brief-file",
                str(self.brief),
                "--base",
                "main",
            ],
            cwd=self.repo,
            env=self.env,
        )

    def resume_task(self, task_id: str, unit: str = "PR #1", *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return run(
            [
                str(REVIEW_SCRIPT),
                "resume",
                "--task-id",
                task_id,
                "--unit",
                unit,
                "--update-file",
                str(self.update),
                "--base",
                "main",
            ],
            cwd=self.repo,
            env=self.env,
            check=check,
        )

    def calls(self) -> list[list[str]]:
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def test_task_session_lifecycle_and_multi_unit_reuse(self) -> None:
        original_status = run(["git", "status", "--porcelain"], cwd=self.repo).stdout
        started = self.start_task()
        start_meta = metadata(started.stderr)
        task_id = start_meta["TASK_ID"]
        session_id = start_meta["CLAUDE_SESSION_ID"]
        state_path = Path(start_meta["STATE_FILE"])

        self.assertTrue(state_path.is_file())
        self.assertFalse(str(state_path).startswith(str(self.repo)))
        self.assertEqual(stat.S_IMODE(state_path.stat().st_mode), 0o600)
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["taskTitle"], "Review calculator work")
        self.assertEqual(state["reviewUnits"]["PR #1"]["rounds"], 1)

        first_call = self.calls()[0]
        self.assertIn("--session-id", first_call)
        self.assertEqual(first_call[first_call.index("--session-id") + 1], session_id)
        first_prompt = first_call[-1]
        self.assertIn("Review calculator work", first_prompt)
        self.assertIn("Acceptance: add(2, 3) returns 5", first_prompt)

        resumed = self.resume_task(task_id)
        self.assertEqual(metadata(resumed.stderr)["CLAUDE_SESSION_ID"], session_id)
        second_call = self.calls()[1]
        self.assertIn("--resume", second_call)
        self.assertEqual(second_call[second_call.index("--resume") + 1], session_id)

        new_unit = self.resume_task(task_id, unit="PR #2")
        self.assertEqual(metadata(new_unit.stderr)["CLAUDE_SESSION_ID"], session_id)
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["reviewUnits"]["PR #1"]["rounds"], 2)
        self.assertEqual(state["reviewUnits"]["PR #2"]["rounds"], 1)
        self.assertIn("new review unit", self.calls()[2][-1])
        self.assertEqual(run(["git", "status", "--porcelain"], cwd=self.repo).stdout, original_status)

        completed = run(
            [str(REVIEW_SCRIPT), "complete", "--task-id", task_id],
            cwd=self.repo,
            env=self.env,
        )
        self.assertIn("Completed task", completed.stdout)
        refused = self.resume_task(task_id, check=False)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("task is not active", refused.stderr)

        second_task = self.start_task(title="A different calculator task", unit="PR #3")
        self.assertNotEqual(metadata(second_task.stderr)["CLAUDE_SESSION_ID"], session_id)

    def test_round_limit_and_configuration_drift(self) -> None:
        started = self.start_task()
        task_id = metadata(started.stderr)["TASK_ID"]
        self.resume_task(task_id)
        self.resume_task(task_id)
        refused = self.resume_task(task_id, check=False)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("3-round limit", refused.stderr)

        other = self.start_task(title="Configuration task", unit="PR #4")
        other_task_id = metadata(other.stderr)["TASK_ID"]
        changed_env = self.env.copy()
        changed_env["CLAUDE_REVIEW_MODEL"] = "opus"
        drift = run(
            [
                str(REVIEW_SCRIPT),
                "resume",
                "--task-id",
                other_task_id,
                "--unit",
                "PR #4",
                "--update-file",
                str(self.update),
                "--base",
                "main",
            ],
            cwd=self.repo,
            env=changed_env,
            check=False,
        )
        self.assertNotEqual(drift.returncode, 0)
        self.assertIn("reviewer configuration changed", drift.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
