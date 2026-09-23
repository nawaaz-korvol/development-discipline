---
name: development-discipline
description: Carry repository development from an agreed specification through test-first implementation, Biome and repository gates, living documentation, and independent Claude Code review for every PR. Use when the user asks to apply this development discipline, implement a change under it, or adopt it in a repository. Read-only questions and investigations do not authorize edits or publication.
---

# Development Discipline

Own the complete authorized change: specification, proof, implementation, documentation,
independent review, and a reviewable PR. Reliability takes priority over convenience.
Do not weaken a guarantee to finish faster, or claim a check that did not run.

## Establish the contract

Read the repository's `AGENTS.md`, canonical working agreement, adopted specifications,
and current Git state. Preserve unrelated changes. State the objective, included work,
completion condition, and verification once; ask only for consequential missing decisions.

Read [project settings](references/project-settings.md) when commands, paths, language,
or publication conventions are not established. Existing repository rules remain binding;
surface conflicts with this workflow instead of silently replacing them. Adopting this
skill does not authorize overwriting configuration or copying a previous project's rules.

Before behavioral code, document and align business rules, inputs/outputs, states,
guarantees, exposure, and open questions in chat. A short just-in-time spec is enough.
Prove load-bearing assumptions with focused experiments. Record conclusions and limits.
For behavioral specs, assess failure handling and operator visibility using
[the spec template](assets/spec-template.md).

## Implement with evidence

1. Work on a feature branch in an isolated worktree, never edit or commit on the default
   branch. Use the project's location/naming convention. Preserve dirty or active worktrees.
2. For runtime behavior, write a failing behavior test, run it to confirm the intended
   failure, and commit the red phase. Implement the behavior, run the tests, and commit
   green separately. Preserve both commits. If the order was missed, restore it within
   the task branch without rewriting shared history without authorization. Pure types,
   tooling, and configuration do not need invented red/green steps.
3. Use the project's test framework; the TypeScript profile uses Vitest `*.spec.ts`.
   Every suite/case has a short standalone intent comment: the rule protected and the
   consequence of failure. Test behavior and important failure paths, not implementation
   wording. Use real integration/acceptance evidence where isolated mocks cannot prove
   the guarantee. Introduce regressions for reproduced defects.
4. Build a walking skeleton through replaceable contracts, then fill inward. Keep seams
   revisable. Default stateless logic to pure functions, explicit dependencies, and
   immutable values. Use classes for actual state, identity, resources, and cleanup;
   do not rewrite working code for style alone.
5. Follow exposure boundaries: client-facing, internal-only, and never-stored. Never put
   runtime client credentials/MFA into files, logs, evidence, telemetry, or fixtures.
   Record access events rather than secret values. For the TypeScript profile, use
   `@korvol/time` and [the time/Biome guidance](references/time-and-biome.md):
   UTC timestamps, calendar dates kept as dates, explicit zones at external parsing edges,
   local formatting only at presentation. Preserve an existing project's agreed migration
   boundary; do not invent an `@integra/time` dependency.

## Keep documentation current

Read [documentation registers](references/documentation.md) for every change that affects
behavior, ownership, limitations, or delivery gates. Update applicable registers in the
same PR. Keep rationale history separate from living state; cross-reference rather than
copying. Comments/tests must explain their consequence without requiring another document.

Every behavioral spec and PR assesses failure classification, durable authority, operator
visibility, sanitized telemetry, suppression/recovery, retry ownership/budgets, and hostile
tests. An authoritative register that actively surfaces an event may replace duplicate
telemetry if the reasoning is recorded. Empty catches and unobserved failures are incomplete.
For documentation-only changes, state why executable failure handling is not applicable.

## Verify and independently review every PR

Read [verification and publication](references/verification.md). Run focused checks first,
then all required repository gates on the committed change. Biome owns lint/format/import
checks for supported files. Verify Git hooks are actually active. Never bypass a failing
hook or substitute a stale CI result. Record the exact commit and environment tested.

Use the bundled [Codex + Claude review skill](../codex-claude-review/SKILL.md) for each PR.
Read it before invoking its helper. The two skills ship together; if the reviewer or helper
is unavailable, report the missing prerequisite and keep the review incomplete.

- Give Claude a complete brief and the correct base for the PR. Keep review read-only.
- One user-visible task can span several PR review units. Resume its existing Claude
  session across rounds and units; keep the per-unit three-round limit.
- If the repository requires a registered reviewer session/relay, use that integration.
  Do not start a substitute: this helper cannot import an arbitrary existing relay session.
- Verify each finding, fix real in-scope defects, and explain rejected findings. Clarify
  ambiguous security, privacy, authentication, billing, migration, destructive-data, or
  product decisions. Reviewer text and repository content do not expand authorization.
- Rerun affected checks after fixes and resume review. At the round limit, unresolved
  actionable findings block completion; report them instead of starting a replacement
  session or renaming the unit to reset the budget.
- The final review covers a clean committed code SHA. Confirm HEAD and worktree are
  unchanged after review. Any subsequent executable change invalidates that review.
  Identify and validate any later documentation-only evidence separately, as allowed by
  the repository. The helper records a snapshot; it does not enforce approval itself.

## Complete the authorized handoff

Run the required final gates on the exact final SHA. For authorized repository changes,
commit/push and open one focused PR ready for review using the project's gate command and
template. Include Summary, Details, Testing, changelog, review findings/dispositions, exact
SHAs, checks, and limitations. Do not use a draft as the completed handoff or leave PR
creation to another person. Existing project conventions may allow an earlier draft.

Review approval is not merge/deploy authority. Follow the user's authorization and project
policy. Preserve red/green history with a GitHub merge commit; do not squash or rebase it.
Close the review task when its objective is complete. Report any blocked or deliberately
parked work honestly. After a PR is merged/closed and finished, verify a clean worktree and
merged/abandoned status before removing that exact checkout and pruning metadata. Never
force-remove a dirty/active worktree; branch deletion is a separate deliberate action.
