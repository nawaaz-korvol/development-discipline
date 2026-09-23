# Require verified GPG commits

## What

- Require GPG signing before the first development commit and verify every introduced
  PR commit on GitHub; cover red/green and documentation commits in the reusable skill.
- Add a PR CI gate for complete, current-head OpenPGP verification evidence.
- Document safe key setup, public-only sharing, and the unsigned initial PR history.

## Verified

Validation and independent-review results are recorded in the follow-up PR at its
exact committed head. No existing commit or released tag is rewritten by this change.
