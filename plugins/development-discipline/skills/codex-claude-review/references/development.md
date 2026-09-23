# Developing and testing this skill

Read this file only when modifying `codex-claude-review`. It is not part of ordinary implementation or review execution.

## Invariants

Any update must preserve these behaviors unless the user explicitly changes the contract:

1. A task is a user-visible objective plus completion condition, not a PR, branch, commit, or worktree.
2. Codex states a clear task boundary once and proceeds without repeatedly asking the user.
3. One task may contain multiple review units, including PRs in different branches or worktrees.
4. The first review creates one fresh Claude session; later units and rounds in the same task resume that session.
5. A different or completed task cannot reuse the session.
6. Codex supplies a full initial context brief and a concrete progress update on every resume.
7. Claude remains read-only. It does not edit, commit, push, post comments, or communicate externally.
8. Reviewer model or effort drift causes a refusal to resume rather than a silent configuration change.
9. Each review unit is limited to three successful Claude rounds. The task may contain multiple units.
10. State is local, permission-restricted, outside the reviewed repository, and never committed automatically.
11. Claude output is advisory. Codex verifies findings and owns implementation decisions.
12. Completing a task closes its state and prevents accidental reuse.

## Required validation

Run all of the following after changing instructions, state handling, CLI arguments, prompts, or review behavior:

```bash
bash -n scripts/run-claude-review.sh
python3 -m py_compile scripts/run_claude_review.py tests/test_review_workflow.py
python3 tests/test_review_workflow.py
uv run --with pyyaml python \
  <skill-creator-root>/scripts/quick_validate.py \
  .
```

Run these commands from the `codex-claude-review` skill directory. Replace
`<skill-creator-root>` with the directory of the loaded `skill-creator` skill.

The deterministic test must verify observable behavior rather than merely matching headings:

- `start` creates a task ID and Claude session ID;
- the initial prompt contains the task contract and supplied context;
- `resume` uses the same Claude session for another round of the same unit;
- a new review unit inside the same task also uses the same session;
- a second task receives a different Claude session;
- completion blocks later resume;
- the per-unit three-round limit is enforced;
- model or effort changes block resume;
- task state stays outside the Git worktree with restrictive permissions;
- Claude invocation cannot mutate the fixture repository during the test.

## Live end-to-end test

Run `python3 tests/live_review_workflow.py` when changing session creation/resumption, Claude CLI flags, prompt construction, or read-only controls. It makes three real Claude calls and therefore consumes Claude usage; obtain user authorization unless the request already includes end-to-end testing.

The live fixture must:

1. Create an isolated temporary Git repository.
2. Add a small implementation containing an obvious correctness defect while retaining a meaningful diff after the defect is fixed.
3. Start a task and confirm Claude reports the defect with the relevant file.
4. Fix the defect without changing the task or review unit.
5. Resume the same Claude session and confirm the state records the same session ID and review round two.
6. Confirm Claude reports no remaining actionable finding.
7. Move to a second branch and review unit within the same task, then confirm the same Claude session is resumed and the new unit starts at round one.
8. Confirm the reviewer created no commits and made no filesystem changes.
9. Remove or move the temporary fixture to Trash after inspection.

If the live result fails because Claude wording varies, inspect the substance before weakening an assertion. Never replace behavioral checks with exact prose checks merely to make the test pass.

## Review after testing

Inspect the generated state and both Claude prompts. Confirm that no secrets or raw Claude transcripts are persisted, task/session IDs are visible to Codex, and normal execution does not require the user to manage Claude sessions manually.
