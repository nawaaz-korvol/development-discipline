# Component responsibilities

| Component | Owns | Must not do |
|---|---|---|
| Development skill | Workflow, project adaptation, documentation and gate requirements | Override user scope, silently replace project rules, or invent completed checks |
| Claude review skill/helper | Reviewer context, task/session continuity, bounded rounds | Edit the reviewed repository, authorize merging, or claim programmatically verified approval |
| Project working agreement | Commands, document paths, exposure/time rules, publication authority | Depend on an unspecified machine's paths or credentials |
| Marketplace/manifest | Plugin identity and bundled skill discovery | Install/authenticate Claude or synchronize review state |
| Package checks/CI | Package integrity, portable helper-state tests, POSIX integration tests, complete PR GitHub GPG verification | Claim live authenticated review from mocked tests, repair historical signatures, or imply branch protection is configured |
