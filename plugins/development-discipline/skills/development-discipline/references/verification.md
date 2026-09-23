# Verification and publication

## Gate sequence

1. Confirm the intended red test fails for the claimed reason; do not count dependency,
   syntax, or environment failures as behavioral red evidence.
2. After implementation, run focused tests and the relevant type/lint checks.
3. Commit a coherent green change and run independent review. Repair through regression
   tests where appropriate; record finding dispositions and resume the same review unit.
4. Run the complete required final gates on a clean feature-branch HEAD. Record the SHA,
   commands, results, test environment, relevant image digest/platform, and skipped checks.
5. Publish through the repository's approved command. Verify the remote head equals the
   tested/reviewed code. If code changes, refresh both gates and review. Check CI on the
   actual PR commit, not merely a branch's last green badge.

The pre-push hook must be installed and fail closed on its checks. Frozen-lockfile
installation, typecheck, lint/format, full unit tests, and relevant production-shaped
acceptance tests make up the complete gate. Never bypass a hook, waive a failed gate
because hosted CI quota is unavailable, or call a skipped test a pass.

Use ordinary automatic PR CI unless the repository explicitly adopts another arrangement.
Integra's manual-dispatch CI and its `pnpm pr:open`/`pnpm pr:push` implementation are local
project choices. A new project needs equivalent evidence, not a dependency on those tools.

## Reproducibility and flaky tests

Pin package tooling, preserve lockfiles, and use `--frozen-lockfile` or its equivalent.
Separate fast behavior tests from slower integration/browser/process gates. A required
test must fail when its required browser/service is unavailable, rather than silently skip.

When deployment is Linux amd64, explicitly run browser/process proof on `linux/amd64`,
verify `x86_64`, and record the resolved image digest. A native Apple Silicon pass is not
that proof. For another deployment target, verify that target explicitly.

If the exact test passes locally on the required surface and fails in CI, rerun the
unchanged failed job once. A second unchanged rerun needs objective progress and no
deterministic defect. Do not continue rerunning until green. Replace/remove unreliable
proof only while recording the missing guarantee in limitations and roadmap; do not
mark the affected release criterion complete until replacement evidence exists.

## PR evidence

Use [the PR template](../assets/pr-template.md) or the project's established template.
Keep Summary, Details, and Testing; remove genuine non-applicable sections and explain
omitted required checks. Record risk/rollback when relevant, the documentation updates,
Claude findings/dispositions, reviewed code SHA, final gate SHA, and remote head.

Preserve separate red/green commits and use merge commits. Every development commit
must be GPG-signed and GitHub-verified; follow [commit signing](commit-signing.md) before
the first commit and verify the complete PR commit list before handoff. Include the
checked head, commit count, and verification result. GitHub's merge-commit identity
is expected, but its signature does not verify unsigned commits inside the PR.
