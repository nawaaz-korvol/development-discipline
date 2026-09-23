# GPG signing and GitHub verification

Configure signing before the first development commit, including red tests and
documentation. Inspect effective Git identity, signing configuration, and local
GPG secret-key metadata. Reuse a valid signing-capable key whose identity matches
the committer email and a verified email on the intended GitHub account. A public
key on GitHub alone cannot sign locally.

If no suitable key exists and key creation is authorized, generate a signing key
in the user's GPG keyring. Let the user enter any passphrase directly into GPG's
secure prompt; never request it in chat, store it in scripts, or remove protection
to make automation work. Share only an armored public export and its fingerprint
for GitHub registration. Private keys and revocation certificates stay outside
repositories, release archives, CI artifacts, and chat. Do not copy private keys
between machines as part of plugin installation.

Use repository-local settings unless broader changes are requested:

```sh
git config --local gpg.format openpgp
git config --local user.signingkey <full-signing-key-fingerprint>
git config --local user.email <verified-key-email>
git config --local commit.gpgsign true
git commit -S -m "<message>"
git verify-commit HEAD
```

Set `gpg.program` to the actual executable when needed; never copy another machine's
absolute path. Preserve the intended user identity. A missing key, locked key, or
failed signature is a prerequisite failure, not permission to commit unsigned.
Disposable test repositories may create unsigned synthetic fixtures when those
commits are never published as development history.

Before handoff, enumerate **all commits introduced by the PR**, including red/green
and evidence commits. Verify local signatures, push through the normal gates, and
check GitHub's commit API for each SHA: `verification.verified` must be true,
`reason` must be `valid`, and the signature must be OpenPGP. Confirm the remote head
equals the reviewed/tested final head. Record the count and result in PR evidence.
A locally valid signature is not proof of GitHub verification; an unregistered key
or mismatched email keeps this gate incomplete until corrected and rechecked.

Use a CI verification check and the repository's required-signature/required-check
settings where adopted. Distinguish a reporting CI job from an enforced merge rule;
do not claim branch protection is configured without inspecting it. For GitHub PR
commit pagination, compare the returned count with the PR's reported total and
check the expected head; the endpoint's 250-commit cap must fail closed.

Signatures are part of commit identity. Adding one changes the SHA and invalidates
old review/test evidence. Never rewrite shared history or move published tags to
retroactively sign commits without an explicitly agreed migration. Preserve existing
red/green history and GitHub merge commits; verify the merge SHA if merging is authorized.

See [GitHub's signing guide](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
and [email matching rules](https://docs.github.com/en/authentication/troubleshooting-commit-signature-verification/using-a-verified-email-address-in-your-gpg-key).
