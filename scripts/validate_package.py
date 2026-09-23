"""Reject an incomplete or undiscoverable release before it can be published."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def validate(root: Path) -> None:
    catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    if catalog["name"] != "development-discipline":
        raise ValueError("Unexpected marketplace identity")
    entries = catalog["plugins"]
    if len(entries) != 1:
        raise ValueError("This release must contain exactly one plugin")
    entry = entries[0]
    plugin = (root / entry["source"]["path"]).resolve()
    if not plugin.is_relative_to(root.resolve()) or not plugin.is_dir():
        raise ValueError("Plugin source must exist inside the marketplace")
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if entry["name"] != manifest["name"] or plugin.name != manifest["name"]:
        raise ValueError("Plugin identities disagree")
    if manifest["version"] != json.loads((root / "package.json").read_text())["version"]:
        raise ValueError("Release versions disagree")
    if manifest["skills"] != "./skills/":
        raise ValueError("Skills must ship inside the plugin")
    skill_root = plugin / "skills"
    expected = {"development-discipline", "codex-claude-review"}
    if {path.name for path in skill_root.iterdir() if path.is_dir()} != expected:
        raise ValueError("Both bundled skills must be present")
    for name in expected:
        skill = skill_root / name
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        if not text.startswith(f"---\nname: {name}\n") or "\ndescription: " not in text:
            raise ValueError(f"Invalid skill identity: {name}")
        if not (skill / "agents/openai.yaml").is_file():
            raise ValueError(f"Missing skill UI metadata: {name}")
    for document in plugin.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            path = (document.parent / target.split("#", 1)[0]).resolve()
            if not path.is_relative_to(plugin.resolve()) or not path.exists():
                raise ValueError(f"Broken or external package reference: {document}: {target}")
    for required in ("scripts/run_claude_review.py", "scripts/run-claude-review.sh"):
        if not (skill_root / "codex-claude-review" / required).is_file():
            raise ValueError(f"Missing reviewer helper: {required}")
    print("Package identity, versions, skills, references, and reviewer helpers validated.")


if __name__ == "__main__":
    validate(ROOT)
