# Release gates

This register tracks source readiness. Publication receipts (merge SHA, immutable tag,
archive, and exact-tag installation result) are recorded in
[GitHub Releases](https://github.com/nawaaz-korvol/development-discipline/releases).

| Gate | Exit evidence | Status |
|---|---|---|
| Package | Both official skill validators, plugin validator, and `pnpm check` pass | Passed locally |
| Review helper | Thirteen portable tests, original POSIX CI tests, three-call authenticated fixture | Passed; CI receipts remain tied to the PR SHA |
| Independent review | Claude reviews committed release code; findings resolved | Approved at ccede2c7ebb6cf5889a57fe1a1c0a2b9cfc1c785; see review record |
| Distribution | Fresh isolated local and GitHub installs resolve both skills; ref replacement tested | Passed |
| Release | Reviewed merge commit, version tag, matching archive, exact-tag install | Source ready; publication receipts live in GitHub Releases |

Limitations belong in [NOTES.md](NOTES.md), not in duplicated gate descriptions.
