# Limitations and deferred decisions

| ID | Status | Limitation or decision |
|---|---|---|
| L1 | Known | Skills guide behavior; they do not mechanically enforce every rule. CI and repository hooks supply executable gates. |
| L2 | Known | Claude Code, Git, and Python must exist on each machine. Windows uses the Python entrypoint, native claude.exe, and Claude Code's Git Bash prerequisite. npm batch shims are refused with native-install guidance. |
| L3 | Known | Reviewer state and Claude sessions are local; installing the plugin elsewhere does not migrate them. POSIX mode 0600 does not establish Windows ACL guarantees; use a private user-profile directory. |
| L4 | Known | The imported helper includes Bash under Claude plan-mode controls; this is not an OS sandbox. Review only trusted worktrees, never weaken the controls, and verify unchanged code/HEAD after review. |
| L5 | Known | The helper records the starting HEAD but accepts dirty trees and does not parse approval. Final clean-commit review is a workflow requirement, not a helper guarantee. |
| D1 | Deferred | Public OpenAI directory submission and workspace publishing are separate distribution channels, not part of v1. |
| D2 | Deferred | No open-source license has been selected; do not claim an MIT or Apache grant. |
| D3 | Deferred | No signed gate receipt or custom automated merge coordinator is supplied. Repositories must retain their existing publication controls. |
| R1 | Resolved | Git-hook environment selectors previously escaped into disposable test fixtures. Fixtures now clear inherited Git variables; a host-repository regression proves the calling checkout remains unchanged. |
