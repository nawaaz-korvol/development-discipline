# Adopted specification: Development Discipline 1.0

The user approved extracting Integra's development discipline, adding mandatory
Claude Code review per PR, and distributing it as a plugin through a new public
repository owned by `nawaaz-korvol`.

## Contract and scope

Inputs: an authorized repository development task and its working agreement.
Output: a specified, tested, documented, independently reviewed change with a
complete authorized PR handoff. The skill does not grant merge, deployment, or
external-message authority. Read-only questions remain read-only.

Package two skills: `development-discipline` and `codex-claude-review`. Keep skill
content once under `plugins/development-discipline/skills/`. A repository marketplace
points at that plugin. A release archive contains the same plugin tree.

Preserve the agreed 21 disciplines: reliability, specification, experiments,
replaceable contracts, functional core, separate TDD commits, meaningful test intent,
strict types, Biome, active Git hooks, reproducibility, layered tests, exact-commit
gates, flake policy, worktrees, six documentation registers, complete PRs, review and
merge history, operational visibility, security/time boundaries, and Claude review.

Generalize Integra-specific commands, package names, account routing, and relay rules
into project settings. Do not export private project content. Do not automatically
create all documentation registers in a small repository or overwrite existing rules.

## Review and authority

One Claude session belongs to one user-visible task; each PR is a review unit with
at most three rounds. Codex verifies findings. An unresolved finding is not approval.
The final review must cover committed code; changes to executable content require
fresh review. Preserve registered reviewer sessions in repositories that require them;
the bundled helper cannot adopt an arbitrary existing relay session.

The existing helper is imported from the user's source at a fixed commit, with
attribution. This first slice changes packaging and workflow guidance, not its session
protocol. Windows uses the Python entrypoint; POSIX may use the shell wrapper.

### User-aligned addendum: public time package

The user specified `@korvol/time` on npm for the TypeScript time discipline. Its public
0.1.1 API and runtime requirements were checked. Include a Biome Date-ban fragment and
consumer guidance; no local Integra time-package exception is needed in consumers.

## Verification and limits

Validate both skills and the plugin with the official local validators. Run package
checks, meaningful review-state tests, and original POSIX tests in CI. Test a clean
Codex install and a real read-only Claude review. Document unverified surfaces.
Hosted CI runs automatically on PRs/main for this repository; Integra's manual CI
exception does not transfer here. No browser or TypeScript application is invented
to justify unrelated gates.

Publishing to GitHub does not publish to OpenAI's public directory or synchronize
Claude credentials/session state between machines. No open-source license has been
selected. Future public-directory submission is outside this release.

## Telemetry and error handling

No new application runtime path is introduced by this packaging slice. The imported
helper reports command failures on stderr/nonzero exit and keeps local task metadata.
It does not provide an application telemetry service, validate review verdicts, or
enforce repository immutability through an OS sandbox. These limits remain explicit.
