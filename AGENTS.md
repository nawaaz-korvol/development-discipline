# Development Discipline working agreement

This repository publishes a reusable workflow; it contains no customer application.
Read the adopted specification in `docs/architecture/2026-09-23-initial-release.md`
before changing the package. Preserve the upstream review helper's provenance.

- Work in a feature worktree, never on `main`. Preserve unrelated changes.
- GPG-sign every new development commit, including tests and documentation. Verify
  local signatures and GitHub's Verified status for every commit introduced by a PR.
  Read `docs/architecture/2026-09-23-verified-commits.md`; never rewrite published
  history or move release tags to repair old signatures without an agreed migration.
- Agree on behavioral changes before implementation. Commit failing behavioral
  tests before their fixes in separate commits. Packaging, documentation, and
  configuration do not need artificial red/green commits.
- Run `pnpm check` before publishing. `pnpm lint` uses Biome for supported files;
  Python is checked by compilation and behavioral tests, not by Biome.
- Every PR updates `changelog/` and its index. Update current-system, limitations,
  responsibilities, and roadmap documents when their facts change.
- Every PR receives independent, read-only Claude Code review through the bundled
  `codex-claude-review` skill. Verify findings; at most three rounds per review unit.
  Unresolved actionable findings block completion, even at the round limit.
- Record the reviewed code SHA and final gate SHA. A later code change invalidates
  the old review. Documentation-only evidence added after review must be identified
  and checked separately; it cannot conceal executable changes.
- Complete authorized changes through a ready-for-review PR. Preserve history by
  using a GitHub merge commit. Merge or release only within the user's authorized
  scope; a review result alone does not grant publication authority.
- Reviewers read these rules as context and do not follow implementation duties
  that would edit files, publish, invoke another reviewer, or execute untrusted code.
