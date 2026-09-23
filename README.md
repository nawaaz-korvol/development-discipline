# Development Discipline

Specify the change, commit failing tests, implement it, document reality, verify the
exact commit, and have Claude Code independently review every PR.

This is a skills-only Codex plugin published by `nawaaz-korvol`. It bundles the
development workflow and `codex-claude-review` together. The TypeScript profile uses
Biome and the public [`@korvol/time`](https://www.npmjs.com/package/@korvol/time) package.

## Install on each machine

With a Codex version supporting plugin marketplaces, after the v1.0.0 release:

```sh
codex plugin marketplace add nawaaz-korvol/development-discipline --ref v1.0.0
codex plugin add development-discipline@development-discipline
```

Start a new Codex task after installation and invoke:

```text
Use $development-discipline to implement this change with the agreed spec,
test-first commits, documentation, repository gates, and Claude Code review.
```

The plugin contains both skills; do not separately install duplicate copies. Existing
project working agreements still apply. For adopting the discipline in a new project,
ask the skill to prepare the project settings and working agreement before implementation.

GitHub distribution requires a per-machine install. It does not imply automatic account
sync, cloud execution, or OpenAI public-directory publication.

## Reviewer prerequisites

- Git and Python 3.10+.
- A locally installed, authenticated Claude Code CLI supporting safe mode and plan
  permissions (live compatibility is checked with 2.1.233). Standalone print mode has
  no permission host and denies requests that would prompt.
- On Windows, Claude Code's Git Bash prerequisite. Invoke the Python entrypoint with
  `python .../scripts/run_claude_review.py`; POSIX can use the `.sh` wrapper with `python3`.
- Repository-specific build/test dependencies. This package does not install or sign
  into Claude, create a background reviewer, or grant GitHub merge authority.

Claude reviews use your configured account and consume Claude usage. The helper starts
one session per task, resumes it across PR review units, and limits each unit to three
rounds. Codex validates every finding. Missing review or unresolved findings remain
incomplete rather than becoming approval. Final review must cover committed code.

State stays under `~/.local/state/codex-claude-review` by default; it does not travel with
the plugin. Keep that directory private. See [limitations](docs/NOTES.md) for platform
permissions, review controls, and exact-SHA enforcement boundaries.

## Update or roll back

Re-register the same repository at the desired published tag, then reinstall the plugin:

```sh
codex plugin marketplace add nawaaz-korvol/development-discipline --ref v1.0.0
codex plugin add development-discipline@development-discipline
```

Replace the tag with the desired release and start a new task. Pinning a release makes
updates deliberate. Advanced users can track `main` and refresh with
`codex plugin marketplace upgrade development-discipline`, then reinstall, but `main`
can contain unreleased changes. Never assume installing a new version migrates an
in-progress Claude session.

## Package contents

- [Development skill](plugins/development-discipline/skills/development-discipline/SKILL.md)
  and its project settings, documentation, verification, and time/Biome references.
- [Claude review skill](plugins/development-discipline/skills/codex-claude-review/SKILL.md)
  and its Python helper, POSIX launcher, and original tests.
- Templates for an adopted working agreement, specification, PR, and Biome time rule.
- A repository marketplace and `.codex-plugin/plugin.json` compatibility manifest.

The source exists once under `plugins/development-discipline/`; release archives contain
that same tree. No MCP server or hosted backend is required.

## Develop and verify

Use a feature worktree and read [AGENTS.md](AGENTS.md). With Python, Node, and pnpm:

```sh
pnpm install --frozen-lockfile
pnpm check
```

The prepare script installs the pre-push gate. Checks cover Python syntax, Biome,
portable task/session tests, actual Biome time-rule behavior, and package integrity.
CI also runs the original subprocess integration tests on Linux/macOS. These simulated
tests do not claim authenticated Claude review; live evidence is recorded separately.

Official skill/plugin validators are used when preparing releases. A release requires
clean-install validation, Claude review, the reviewed PR's merge commit, and a matching
tag/archive. See [release gates](docs/ROADMAP.md) and [current behavior](docs/SYSTEM.md).

## Provenance and license

The workflow was generalized from the owner's Integra development discipline. The
review skill comes from the owner's `nawaaz-housenumbers/agent-workflow` repository at
a recorded commit. See [provenance](plugins/development-discipline/PROVENANCE.md).

No open-source license has been selected for this repository. The separate npm package
`@korvol/time` has its own published license. Credentials, customer material, and raw
review transcripts are not part of this distribution.
