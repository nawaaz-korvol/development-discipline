"""Prove the shipped Biome rule distinguishes forbidden clocks from package use."""

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "plugins/development-discipline/skills/development-discipline/assets/biome-time-rule.json"
BIOME = ROOT / "node_modules/@biomejs/biome/bin/biome"


class TimeRuleTests(unittest.TestCase):
    """A broken rule would silently reintroduce machine-local time into application code."""

    def check(self, source: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="discipline-biome-") as directory:
            root = Path(directory)
            config = json.loads(RULE.read_text())
            config["linter"]["rules"]["recommended"] = False
            (root / "biome.json").write_text(json.dumps(config))
            target = root / "clock.ts"
            target.write_text(source)
            return subprocess.run(["node", str(BIOME), "lint", "--config-path", str(root), str(target)],
                                  capture_output=True, text=True, encoding="utf-8")

    # Direct Date construction and wall-clock reads must both fail the consumer's lint gate.
    def test_raw_date_is_rejected(self) -> None:
        for source in ("export const timestamp = Date.now();", "export const timestamp = new Date();"):
            with self.subTest(source=source):
                result = self.check(source)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("noRestrictedGlobals", result.stdout + result.stderr)

    # The approved dependency must remain usable without exempting the entire consumer app.
    def test_korvol_time_import_is_allowed(self) -> None:
        result = self.check('import { nowUtc } from "@korvol/time"; export const timestamp = nowUtc();')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
