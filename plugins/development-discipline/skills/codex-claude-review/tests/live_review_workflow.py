#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


SKILL_ROOT = Path(__file__).resolve().parents[1]
REVIEW_SCRIPT = SKILL_ROOT / "scripts" / "run-claude-review.sh"


def run(command: list[str], *, cwd: Path, env: dict[str, str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed: {command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


def metadata(stderr: str) -> dict[str, str]:
    return dict(re.findall(r"^([A-Z_]+)=(.+)$", stderr, flags=re.MULTILINE))


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="codex-claude-review-live-") as temporary:
        root = Path(temporary)
        repo = root / "repo"
        repo.mkdir()
        env = os.environ.copy()
        env.update(
            {
                "CLAUDE_REVIEW_EFFORT": "low",
                "CODEX_CLAUDE_REVIEW_STATE_DIR": str(root / "state"),
            }
        )
        run(["git", "init", "-b", "main"], cwd=repo, env=env)
        run(["git", "config", "user.name", "Skill Live Test"], cwd=repo, env=env)
        run(["git", "config", "user.email", "skill-live-test@example.invalid"], cwd=repo, env=env)
        source = repo / "calculator.js"
        source.write_text("export function multiply(a, b) {\n  return a * b;\n}\n", encoding="utf-8")
        run(["git", "add", "calculator.js"], cwd=repo, env=env)
        run(["git", "commit", "-m", "test: initial fixture"], cwd=repo, env=env)
        source.write_text(
            "export function multiply(a, b) {\n  return a * b;\n}\n\n"
            "export function add(a, b) {\n  return a - b;\n}\n",
            encoding="utf-8",
        )
        brief = root / "brief.md"
        brief.write_text(
            "Implement add(a, b). Acceptance: add(2, 3) returns 5. No tests have been added yet.",
            encoding="utf-8",
        )
        original_status = run(["git", "status", "--porcelain"], cwd=repo, env=env).stdout
        started = run(
            [
                str(REVIEW_SCRIPT),
                "start",
                "--task-title",
                "Live reviewer session test",
                "--objective",
                "Implement a correct addition helper",
                "--completion",
                "Claude reports the defect, the defect is fixed, and the resumed review is clean",
                "--unit",
                "calculator implementation",
                "--brief-file",
                str(brief),
                "--base",
                "main",
            ],
            cwd=repo,
            env=env,
        )
        start_meta = metadata(started.stderr)
        if "calculator.js" not in started.stdout or "No actionable findings" in started.stdout:
            raise RuntimeError(f"Claude did not identify the seeded defect:\n{started.stdout}")
        if run(["git", "status", "--porcelain"], cwd=repo, env=env).stdout != original_status:
            raise RuntimeError("Claude modified the fixture during the first review")

        source.write_text(
            "export function multiply(a, b) {\n  return a * b;\n}\n\n"
            "export function add(a, b) {\n  return a + b;\n}\n",
            encoding="utf-8",
        )
        update = root / "update.md"
        update.write_text(
            "Accepted the correctness finding and changed add(a, b) from subtraction to addition. No other behavior changed.",
            encoding="utf-8",
        )
        fixed_status = run(["git", "status", "--porcelain"], cwd=repo, env=env).stdout
        resumed = run(
            [
                str(REVIEW_SCRIPT),
                "resume",
                "--task-id",
                start_meta["TASK_ID"],
                "--unit",
                "calculator implementation",
                "--update-file",
                str(update),
                "--base",
                "main",
            ],
            cwd=repo,
            env=env,
        )
        resume_meta = metadata(resumed.stderr)
        if resume_meta["CLAUDE_SESSION_ID"] != start_meta["CLAUDE_SESSION_ID"]:
            raise RuntimeError("resume used a different Claude session")
        if resume_meta["REVIEW_ROUND"] != "2":
            raise RuntimeError("resume did not record review round two")
        if "No actionable findings" not in resumed.stdout:
            raise RuntimeError(f"resumed review was not clean:\n{resumed.stdout}")
        if run(["git", "status", "--porcelain"], cwd=repo, env=env).stdout != fixed_status:
            raise RuntimeError("Claude modified the fixture during the resumed review")
        if len(run(["git", "log", "--format=%H"], cwd=repo, env=env).stdout.splitlines()) != 1:
            raise RuntimeError("Claude created a commit during review")

        run(["git", "add", "calculator.js"], cwd=repo, env=env)
        run(["git", "commit", "-m", "feat: add calculator helper"], cwd=repo, env=env)
        run(["git", "checkout", "main"], cwd=repo, env=env)
        run(["git", "checkout", "-b", "second-review-unit"], cwd=repo, env=env)
        formatter = repo / "formatter.js"
        formatter.write_text(
            "export function label(value) {\n  return `Value: ${value}`;\n}\n",
            encoding="utf-8",
        )
        second_update = root / "second-unit.md"
        second_update.write_text(
            "The calculator review unit is clean. Begin the formatter review unit, which belongs to the same user-visible task.",
            encoding="utf-8",
        )
        second_status = run(["git", "status", "--porcelain"], cwd=repo, env=env).stdout
        commits_before_second_unit = run(["git", "log", "--format=%H"], cwd=repo, env=env).stdout.splitlines()
        second_unit = run(
            [
                str(REVIEW_SCRIPT),
                "resume",
                "--task-id",
                start_meta["TASK_ID"],
                "--unit",
                "formatter PR",
                "--update-file",
                str(second_update),
                "--base",
                "main",
            ],
            cwd=repo,
            env=env,
        )
        second_meta = metadata(second_unit.stderr)
        if second_meta["CLAUDE_SESSION_ID"] != start_meta["CLAUDE_SESSION_ID"]:
            raise RuntimeError("second review unit used a different Claude session")
        if second_meta["REVIEW_ROUND"] != "1":
            raise RuntimeError("second review unit did not start at round one")
        if run(["git", "status", "--porcelain"], cwd=repo, env=env).stdout != second_status:
            raise RuntimeError("Claude modified the fixture during the second review unit")
        if run(["git", "log", "--format=%H"], cwd=repo, env=env).stdout.splitlines() != commits_before_second_unit:
            raise RuntimeError("Claude created a commit during the second review unit")

        state = json.loads(Path(resume_meta["STATE_FILE"]).read_text(encoding="utf-8"))
        if state["reviewUnits"]["calculator implementation"]["rounds"] != 2:
            raise RuntimeError("persisted state did not record two rounds")
        if state["reviewUnits"]["formatter PR"]["rounds"] != 1:
            raise RuntimeError("persisted state did not record the second review unit")
        print("Live end-to-end test passed")
        print(f"Task ID: {start_meta['TASK_ID']}")
        print(f"Claude session ID: {start_meta['CLAUDE_SESSION_ID']}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
