# Initial release

## What

Package the agreed development discipline and existing task-scoped Claude review
workflow as one Codex plugin. Add repository marketplace discovery, project adoption
templates, versioned distribution instructions, and portable package validation.
Repair the live-discovered Claude 2.1.233 invocation incompatibility and preserve
Unicode reviewer output on Windows, with separate red/green commits.

## Verified

- `pnpm check`: Python syntax, Biome, seven portable behavioral tests, and package
  identity/reference integrity passed on Windows.
- Official Skill Creator validators accepted both skills; Plugin Creator validator
  accepted the manifest. The POSIX launcher passed `bash -n`.
- A fresh isolated Codex installation discovered the marketplace and installed both
  skills at plugin version 1.0.0.
- Biome rejected both `Date.now()` and `new Date()` and accepted `@korvol/time` usage.
- The published `@korvol/time@0.1.1` README and metadata confirmed the documented API.
- Hosted CI, independent review, and release evidence are tracked in the PR and roadmap.
