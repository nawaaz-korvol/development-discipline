# Initial release

## What

Package the agreed development discipline and existing task-scoped Claude review
workflow as one Codex plugin. Add repository marketplace discovery, project adoption
templates, versioned distribution instructions, and portable package validation.
Repair the live-discovered Claude 2.1.233 invocation incompatibility and preserve
Unicode reviewer output on Windows, with separate red/green commits.
Isolate test fixture repositories from inherited Git hook selectors, with a regression
that verifies the caller's HEAD, configuration, and working tree remain unchanged.

## Verified

- `pnpm check`: Python syntax, Biome, thirteen portable behavioral tests, and package
  identity/reference integrity passed on Windows.
- Official Skill Creator validators accepted both skills; Plugin Creator validator
  accepted the manifest. The POSIX launcher passed `bash -n`.
- A fresh isolated Codex installation discovered the marketplace and installed both
  skills at plugin version 1.0.0.
- Biome rejected both `Date.now()` and `new Date()` and accepted `@korvol/time` usage.
- The published `@korvol/time@0.1.1` README and metadata confirmed the documented API.
- Live authenticated Claude fixture passed: seeded defect detection, same-session repair
  review, and a second review unit in the same session.
- Linux, macOS, and Windows CI passed on the first reviewed code snapshot; final-SHA
  results and review disposition are tracked in the PR and roadmap.
- GitHub-source installation and remove/re-add at another pinned ref passed in an
  isolated Codex profile.
- Independent Claude review completed in two rounds. Three P3 findings were verified
  and repaired; the second review of `ccede2c7ebb6cf5889a57fe1a1c0a2b9cfc1c785`
  returned no actionable findings. See the retained review record and PR for exact
  final gate/publication evidence.
