"""Exercise task/session state with real Git fixtures and a simulated Claude response.

These portable tests do not authenticate Claude or prove its runtime permissions.
The upstream POSIX subprocess tests and a real review provide separate evidence.
"""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / (
    "plugins/development-discipline/skills/codex-claude-review/scripts/run_claude_review.py"
)
SPEC = importlib.util.spec_from_file_location("review_helper", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class ReviewStateTests(unittest.TestCase):
    """Lost session identity or a reset round budget would invalidate independent review."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="discipline-review-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.previous_cwd = Path.cwd()
        os.chdir(self.repo)
        self.addCleanup(os.chdir, self.previous_cwd)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Workflow Test")
        self.git("config", "user.email", "workflow-test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        (self.repo / "calculator.py").write_text("def add(a, b): return a + b\n")
        self.git("add", ".")
        self.git("commit", "-m", "test: baseline")
        self.git("checkout", "-b", "feature")
        (self.repo / "calculator.py").write_text("def add(a, b): return a - b\n")
        self.brief = self.root / "brief.md"
        self.brief.write_text("Deliver addition: add(2, 3) must equal 5.")
        self.environment = patch.dict(os.environ, {
            "CODEX_CLAUDE_REVIEW_STATE_DIR": str(self.root / "state"),
            "CLAUDE_REVIEW_MODEL": "configured-default",
            "CLAUDE_REVIEW_EFFORT": "high",
            "CLAUDE_BIN": sys.executable,
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.calls: list[dict[str, object]] = []

        def simulated_review(**arguments: object) -> str:
            self.calls.append(arguments)
            return "P1: calculator.py subtracts instead of adding.\n"

        self.reviewer = patch.object(helper, "invoke_claude", side_effect=simulated_review)
        self.reviewer.start()
        self.addCleanup(self.reviewer.stop)

    def git(self, *arguments: str) -> str:
        return subprocess.run(["git", *arguments], check=True, capture_output=True,
                              text=True, encoding="utf-8").stdout.strip()

    def execute(self, *arguments: str) -> tuple[str, str]:
        parsed = helper.parser().parse_args(arguments)
        output, error = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(error):
            parsed.handler(parsed)
        return output.getvalue(), error.getvalue()

    def start(self, unit: str = "PR #1") -> dict[str, object]:
        self.execute("start", "--task-title", "Calculator", "--objective", "Correct addition",
                     "--completion", "Verified addition and clean review", "--unit", unit,
                     "--brief-file", str(self.brief), "--base", "main")
        return json.loads(max((self.root / "state").glob("*.json"),
                              key=lambda path: path.stat().st_mtime_ns).read_text())

    def resume(self, state: dict[str, object], unit: str = "PR #1") -> None:
        self.execute("resume", "--task-id", str(state["taskId"]), "--unit", unit,
                     "--update-file", str(self.brief), "--base", "main")

    # Each PR keeps its own budget while related work retains the same reviewer context.
    def test_session_continuity_and_per_unit_round_limit(self) -> None:
        before = self.git("status", "--porcelain")
        state = self.start()
        self.resume(state)
        self.resume(state, "PR #2")
        self.assertEqual({call["session_id"] for call in self.calls}, {state["claudeSessionId"]})
        self.assertEqual([call["resume"] for call in self.calls], [False, True, True])
        self.assertIn("add(2, 3)", self.calls[0]["prompt"])
        self.resume(state)
        with self.assertRaisesRegex(helper.ReviewError, "3-round limit"):
            self.resume(state)
        persisted, path = helper.load_state(str(state["taskId"]))
        self.assertEqual(persisted["reviewUnits"]["PR #2"]["rounds"], 1)
        self.assertFalse(path.is_relative_to(self.repo))
        if os.name != "nt":
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.git("status", "--porcelain"), before)

    # Completed work cannot silently donate its review authority to a later task.
    def test_completion_refuses_resume_and_new_task_changes_identity(self) -> None:
        state = self.start()
        self.execute("complete", "--task-id", str(state["taskId"]))
        with self.assertRaisesRegex(helper.ReviewError, "not active"):
            self.resume(state)
        second = self.start("PR #3")
        self.assertNotEqual(state["claudeSessionId"], second["claudeSessionId"])

    # Reviewer changes require a new contract rather than mixing models or effort mid-review.
    def test_model_and_effort_drift_refuse_before_invocation(self) -> None:
        state = self.start()
        for key, value in (("CLAUDE_REVIEW_MODEL", "different"), ("CLAUDE_REVIEW_EFFORT", "low")):
            with self.subTest(setting=key), patch.dict(os.environ, {key: value}):
                with self.assertRaisesRegex(helper.ReviewError, "configuration changed"):
                    self.resume(state)
        self.assertEqual(len(self.calls), 1)

    # A failed external call must not consume a successful round or silently switch sessions.
    def test_failed_review_preserves_last_successful_round(self) -> None:
        state = self.start()
        with patch.object(helper, "invoke_claude", side_effect=helper.ReviewError("unavailable")):
            with self.assertRaisesRegex(helper.ReviewError, "unavailable"):
                self.resume(state)
        persisted, _ = helper.load_state(str(state["taskId"]))
        self.assertEqual(persisted["reviewUnits"]["PR #1"]["rounds"], 1)

    # Command construction must not acquire edit tools or bypass the review permission controls.
    def test_reviewer_command_retains_read_controls(self) -> None:
        command = helper.claude_command(session_id="test-session", resume=True, prompt="Review",
                                        model="configured-default", effort="high")
        self.assertIn("--safe-mode", command)
        self.assertIn("--no-chrome", command)
        self.assertEqual(command[command.index("--permission-mode") + 1], "plan")
        self.assertNotIn("--permission-prompt-tool", command)
        self.assertEqual(command[command.index("--tools") + 1], "Read,Grep,Glob,Bash")
        self.assertNotIn("--dangerously-skip-permissions", command)

    # Installed Claude 2.1.233 rejects a newer flag before any review can start.
    def test_standalone_print_supports_pre_2_1_259_cli(self) -> None:
        command = helper.claude_command(session_id="test-session", resume=False, prompt="Review",
                                        model="configured-default", effort="high")
        self.assertNotIn("--permission-prompts", command)
        self.assertIn("--print", command)
        self.assertIn("--safe-mode", command)
        self.assertNotIn("--permission-prompt-tool", command)

    # UTF-8 reviewer output must survive Windows codepages without corruption or lost results.
    def test_unicode_subprocess_output_is_preserved(self) -> None:
        result = helper.run([sys.executable, "-c",
                             "import sys; sys.stdout.buffer.write(bytes.fromhex('e29c9320e28094'))"])
        self.assertEqual(result.stdout, "\u2713 \u2014")


if __name__ == "__main__":
    unittest.main(verbosity=2)
