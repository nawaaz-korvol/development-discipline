# Release gates

| Gate | Exit evidence | Status |
|---|---|---|
| Package | Both official skill validators, plugin validator, and `pnpm check` pass | Passed locally |
| Review helper | Portable lifecycle tests and original POSIX CI tests pass | In progress |
| Independent review | Claude reviews committed release code; findings resolved | Pending |
| Distribution | Fresh isolated Codex install resolves both bundled skills at 1.0.0 | Passed locally; remote tag pending |
| Release | Reviewed merge commit, version tag, and matching plugin archive | Pending |

Limitations belong in [NOTES.md](NOTES.md), not in duplicated gate descriptions.
