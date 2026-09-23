# Project settings and adoption

Resolve settings from the working agreement, package scripts, Git hooks, and CI files.
Do not run an assumed command or silently weaken an existing gate. Distinguish written
policy from actual enforcement; report drift with the concrete configuration evidence.

| Setting | TypeScript/pnpm starting point | Adaptation rule |
|---|---|---|
| Worktree | `worktree/<task>/` | Respect existing location/branch conventions |
| Branch | A task-scoped feature branch | Never modify the default branch directly |
| Test | Vitest, `*.spec.ts` | Use the native framework for another language |
| Typecheck | `pnpm typecheck` with strict TypeScript | Require the real project equivalent; do not label syntax checks as static typing |
| Lint | `pnpm lint` using Biome | Preserve the configured tool outside Biome-supported languages |
| Formatter | `pnpm format` | Formatting is part of the quality gate, not optional cleanup |
| Hook | Versioned pre-push, installed through `prepare` | Verify effective `core.hooksPath`; preserve existing hooks |
| Publish | Existing `pr:open`/`pr:push` or equivalent | Never assume Integra's coordinator exists |
| Runtime tests | Production-representative integration/acceptance checks | Require Docker/browser/database only when relevant |
| Review | Bundled Claude review skill | Preserve registered-session rules in integrated repositories |
| Time | `@korvol/time` for TypeScript | See time/Biome reference; preserve agreed existing migrations |

For an adopted TypeScript profile, enable `strict`, `noUncheckedIndexedAccess`,
`noImplicitOverride`, and filename-case consistency. Preserve correct module settings.
Use Biome's recommended rules plus errors for explicit `any`, non-null assertions,
banned types, and missing `const`. The preferred format is tabs, 100 columns, double
quotes, semicolons, and organized imports. Adapt to an established repository convention
rather than reformatting unrelated files. Pin compatible tool versions and commit the
lockfile; select a Biome schema matching the installed major version.

Ban the raw JavaScript `Date` global in application code through Biome. With the published
`@korvol/time` dependency, consumers normally need no local exception: dependency source
is outside the application lint scope. See [time and Biome](time-and-biome.md) for the
verified API and mergeable rule. Review any adapter/presentation exception explicitly.

For a new repository, use [the working-agreement template](../assets/AGENTS.template.md)
as an adoption checklist. Fill real commands and paths, remove inapplicable entries,
and align the result before implementing behavior. Do not leave placeholders as policy.
For an existing repository, propose the smallest additive change needed for adoption.
