"""Keep current install examples bound to manifests, not historical release IDs."""
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).parents[1]
DOCS = ("README.md", "INSTALL.md", "docs/advisor-rename-migration.md",
        "docs/harness-compatibility.md", "docs/releasing.md",
        "docs/upgrade-testing.md", "docs/releases/current.md",
        "docs/releases/0.3.0-rename-validation.md")


class InstallDocumentationTests(unittest.TestCase):
    def test_current_candidate_labels_match_version(self):
        version = (ROOT / "VERSION").read_text().strip()
        for name in ("README.md", "INSTALL.md", "docs/advisor-rename-migration.md",
                     "docs/releases/current.md"):
            text = (ROOT / name).read_text()
            label = re.search(r"0\.\d+\.\d+-rc\.\d+", text)
            self.assertIsNotNone(label, name)
            self.assertEqual(version, label.group(), name)

    def test_current_install_examples_use_manifest_identity(self):
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["name"]
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())["name"]
        for name in ("README.md", "INSTALL.md"):
            blocks = re.findall(r"```(?:text|bash)\n(.*?)```", (ROOT / name).read_text(), re.S)
            calls = [line.strip() for block in blocks for line in block.splitlines()
                     if re.match(r"(?:/plugin|claude plugin) (?:install|update) ", line.strip())]
            self.assertTrue(calls, name)
            for call in calls:
                self.assertEqual(f"{plugin}@{market}", call.split()[2 if call.startswith("/plugin") else 3], name)
            self.assertIn(f"/{plugin}:{plugin}", [line.strip() for block in blocks
                          for line in block.splitlines()], name)

    def test_local_documentation_link_targets_exist(self):
        for name in DOCS:
            document = ROOT / name
            for raw in re.findall(r"(?<!!)\[[^\]]*\]\(([^\s)]+)\)", document.read_text()):
                url = urlsplit(raw)
                if url.scheme or url.netloc or not url.path:
                    continue
                target = (document.parent / unquote(url.path)).resolve()
                self.assertTrue(target.is_relative_to(ROOT), (name, raw))
                self.assertTrue(target.is_file(), (name, raw))


if __name__ == "__main__":
    unittest.main()
