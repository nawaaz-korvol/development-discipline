# Release gates

| Gate | Exit evidence | Status |
|---|---|---|
| Package | Both official skill validators, plugin validator, and `pnpm check` pass | Passed locally |
| Review helper | Portable lifecycle tests, original POSIX CI tests, three-call authenticated fixture | Passed; final-SHA gates repeat before release |
| Independent review | Claude reviews committed release code; findings resolved | Round 1 complete; three verified P3 findings repaired, re-review pending |
| Distribution | Fresh isolated local and GitHub installs resolve both skills; ref replacement tested | Passed; final release tag pending |
| Release | Reviewed merge commit, version tag, and matching plugin archive | Pending |

Limitations belong in [NOTES.md](NOTES.md), not in duplicated gate descriptions.
