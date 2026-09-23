# Adopted specification: verified commits

The user requires GPG-signed commits and a follow-up PR proving GitHub verification.
Reuse a suitable local private key; otherwise generate one and share only its public
key so the user can register it with GitHub. This machine had no private key available.

## Contract

Every new development commit, including red tests, green implementations, and later
documentation evidence, must carry a GPG signature. Configure signing before the
first commit. The committer email must match a key identity verified by GitHub.
Local cryptographic validity and GitHub's Verified status are separate checks.

The development skill and adoption/PR templates require signing and verification.
A PR CI job checks the complete GitHub-reported PR commit list: nonempty, exact
reported count, final SHA equal to the event head, and every signature present as
OpenPGP with `verified: true` and reason `valid`. API failures, incomplete lists,
unregistered keys, unsigned commits, and stale heads fail the job. GitHub caps the
PR commits endpoint at 250; larger PRs fail closed instead of silently checking a
partial list. CI uses only the built-in read-only token.

## Scope and existing history

This change does not rewrite main or move the published v1.0.0 tag. Its first PR
contains eight unsigned historical commits; the GitHub-created initial and merge
commits are verified. A later signature cannot change an existing commit object.
Retroactive signing would replace SHAs and needs a separately agreed history and
release migration. The new gate covers commits introduced by each PR, not ancestors
already on its base. Disposable fixture commits are not published development commits.

No merge, new release, marketplace update, or branch-protection change is included
in this follow-up PR. CI reports failures; making a check required is a separate
repository setting and must never be assumed from a green workflow file.

## Evidence and failure handling

This is tooling/configuration and documentation, so no artificial red/green history
is required. Exercise the gate predicate against the unsigned first PR (reject),
complete signed current PR (accept after registration), and missing/stale evidence
(reject). Run `pnpm check`, skill validation, and independent Claude review. Verify
each new local signature and GitHub's remote status at the exact final head.

Failures surface through a nonzero CI exit and an actionable annotation. No new
application runtime or telemetry path is introduced. Never log/export private keys,
passphrases, or tokens. Do not remove passphrase protection to enable automation.

Sources: [GitHub signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
and [verified email matching](https://docs.github.com/en/authentication/troubleshooting-commit-signature-verification/using-a-verified-email-address-in-your-gpg-key).
