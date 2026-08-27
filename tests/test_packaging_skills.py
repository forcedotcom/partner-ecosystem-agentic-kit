import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PACKAGING_SKILLS = (
    "packaging-strategy",
    "packageability-assessment",
    "managed-2gp-foundation",
    "package-version-validation",
    "package-ancestry-dependencies",
    "package-release-promotion",
    "package-migration-transfer",
)


class PackagingSkillTests(unittest.TestCase):
    def test_packaging_source_refresh_guides_have_complete_official_urls(self):
        for skill_name in PACKAGING_SKILLS:
            path = ROOT / "skills" / skill_name / "references" / "source-refresh.md"
            content = path.read_text(encoding="utf-8")
            self.assertIn("## Required official sources", content, skill_name)
            urls = re.findall(r"https://[^)\s]+", content)
            self.assertGreaterEqual(len(urls), 1, skill_name)
            for url in urls:
                self.assertNotRegex(url, r"https?://(?:developer|trailhead|help)\\.$")
                self.assertNotIn("...", url)

    def test_packaging_skill_files_are_portable_partner_content(self):
        for skill_name in PACKAGING_SKILLS:
            for path in (
                ROOT / "skills" / skill_name / "SKILL.md",
                *(ROOT / "skills" / skill_name / "references").glob("*.md"),
            ):
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("/Users/", content, str(path))
                self.assertNotIn("peak-testing", content, str(path))
                self.assertNotIn("<!-- peak:", content, str(path))

    def test_packaging_skills_preserve_lifecycle_boundaries(self):
        required_phrases = {
            "packaging-strategy": (
                "my-unpackaged-directory",
                "Named Credentials",
                "sfdx-project.json",
                "agent-script-package-boundary.md",
            ),
            "packageability-assessment": (
                "Named Credentials",
                "External Credentials",
                "unpackaged metadata",
            ),
            "managed-2gp-foundation": ("unpackaged metadata", "Dev Hub"),
            "package-version-validation": ("ancestorVersion", "skip-validation"),
            "package-ancestry-dependencies": ("ancestorVersion",),
            "package-release-promotion": ("terminal `Success`",),
            "package-migration-transfer": ("unlocked-package transfer", "Security Review"),
        }
        for skill_name, phrases in required_phrases.items():
            content = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8").lower()
            for phrase in phrases:
                self.assertIn(phrase.lower(), content, f"{skill_name}: {phrase}")

    def test_named_credential_source_set_is_complete_in_strategy_and_packageability(self):
        expected_urls = (
            "nc-package-credentials.md",
            "nc-populate-external-credentials.md",
            "nc-test-credentials.md",
            "nc-upgrade-package.md",
            "nc-oauth-dev-guide.md",
            "nc-create-oauth-cred.md",
            "nc-manage-oauth-cred.md",
            "nc-update-delete-oauth-cred.md",
            "nc-use-oauth-cred-in-callout.md",
        )
        for skill_name in ("packaging-strategy", "packageability-assessment"):
            content = (
                ROOT / "skills" / skill_name / "references" / "source-refresh.md"
            ).read_text(encoding="utf-8")
            for filename in expected_urls:
                self.assertIn(filename, content, f"{skill_name}: {filename}")


if __name__ == "__main__":
    unittest.main()
