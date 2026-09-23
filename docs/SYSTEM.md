# Current system

The repository is a Git-backed Codex marketplace containing one skills-only plugin.
The plugin exposes the development workflow and its bundled Claude review skill.
No MCP server, service, background automation, or account synchronization is installed.

The development skill routes project settings, documentation, and verification through
supporting references. It requires the bundled review cycle for each PR and records
exact-commit evidence. The review helper starts/resumes/completes local task-scoped
Claude sessions. It records HEAD but does not itself enforce exact-SHA approval;
the skill and repository publication gates own that requirement.

The helper supports native Windows Claude launchers, resolves the executable once,
rejects batch shims, and preserves Unicode output. Standalone print mode with no
permission host keeps prompted requests denied without depending on a newer CLI flag.

`pnpm check` runs Python syntax compilation, Biome, portable state-machine tests,
and real Biome fixtures rejecting raw `Date` while allowing `@korvol/time`,
and package integrity checks. `check:python` is syntax validation, not static type
analysis; the package contains no TypeScript application. CI additionally
runs the original POSIX integration tests on Linux/macOS. Live Claude reviews require
local authentication and are not run in GitHub Actions.

Every new development commit is GPG-signed. The PR-only `verified-commits` CI job
requires GitHub-valid OpenPGP signatures for the complete introduced commit list
at the event head; API failures, incomplete evidence, or unverified commits fail.
It does not scan preexisting base history or configure branch protection. See the
[signing specification](architecture/2026-09-23-verified-commits.md).

See [limitations](NOTES.md), [responsibilities](COMPONENT_RESPONSIBILITIES.md), and
[release gates](ROADMAP.md) for their separate authorities.
