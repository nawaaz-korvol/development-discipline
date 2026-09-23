# Provenance

The development discipline was generalized with the repository owner's authorization
from the Korvol Integra working agreement and aligned in the creation conversation.
No private application implementation, customer material, or account credentials are bundled.

`skills/codex-claude-review/` originates from the same user's public repository:

- https://github.com/nawaaz-housenumbers/agent-workflow
- Commit: `7cf53f149bc186bbe6267823d1b10d296f9fbb47`
- Source directory: `skills/codex-claude-review/`

The task/session protocol is preserved. This distribution removes the 2.1.259-only
permission-prompts flag for compatibility with 2.1.233 standalone print mode, and uses
explicit UTF-8 subprocess/CLI output on Windows. Packaging guidance adds the portable
Python invocation; the enclosing skill supplies mandatory per-PR/final-SHA requirements.
Future changes must retain this attribution and record their scope.

Test fixtures clear inherited Git hook variables before creating repositories. The
live fixture invokes Python directly for Windows support and decodes UTF-8 output.

No open-source license has been selected for this repository or its imported material.
Public visibility is not a representation of an MIT, Apache, or other license grant.
