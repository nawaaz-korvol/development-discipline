# Project working agreement

Adopt and fill this template deliberately; do not overwrite existing instructions.

- Canonical agreement: [record path]. Specification authority: [record path].
- Worktree location and feature branch naming: [record convention]. Never edit main.
- Behavior follows aligned spec, failing test/red commit, implementation/green commit.
- Test runner and focused command: [record command]. Tests explain protected consequences.
- Typecheck, lint/format, full tests, acceptance gates: [record actual commands].
- Hook installation and verification: [record commands]. Never bypass gates.
- Runtime/deployment test environment: [record platform and pinned dependencies].
- Each PR receives the bundled Claude review cycle, with at most three rounds per unit.
- Registered reviewer integration, if required: [record it; otherwise bundled helper].
- Review and final gate evidence identify exact SHAs. Changed code invalidates old evidence.
- Publication command, review/merge authority, and merge method: [record policy].
- Design history, limitations, changelog/index, current system, responsibility map,
  delivery roadmap: [record actual paths or explain a genuinely inapplicable register].
- Every behavioral spec assesses failure handling and operator visibility.
- Exposure/secret rules: [record project contracts]. TypeScript time uses `@korvol/time`
  with a Biome ban on the raw `Date` global; document any agreed migration/exception.
- Preserve unrelated changes and clean up only verified clean, finished worktrees.
