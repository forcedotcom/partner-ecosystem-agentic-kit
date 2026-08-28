import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def skill_text(skill_name):
    return (SKILLS / skill_name / "SKILL.md").read_text(encoding="utf-8")


def normalized(text):
    return " ".join(text.split())


class DevelopmentEnvironmentSkillTests(unittest.TestCase):
    def test_scratch_org_shape_owns_definition_guidance(self):
        content = skill_text("scratch-org-shape")
        for phrase in (
            "development purpose",
            "`sfdx-project.json`",
            "packageDirectories[].definitionFile",
            "`--definition-file`",
            "capability-to-feature/setting mapping",
            "minimal proposed JSON",
            "package-build readiness",
            "subscriber/customer-compatibility",
        ):
            self.assertIn(phrase, content)

    def test_scratch_org_assessment_is_limited_to_approved_repository_evidence(self):
        content = normalized(skill_text("scratch-org-shape"))
        for phrase in (
            "approved definition files",
            "Do not inspect a Dev Hub or scratch org unless the partner separately approves",
            "Do not write a definition file or provision an org",
        ):
            self.assertIn(phrase, content)
        self.assertIn("relevant metadata", content)

    def test_supporting_skills_have_narrow_non_competing_handoffs(self):
        portfolio = normalized(skill_text("environment-portfolio"))
        diagnostics = normalized(skill_text("org-provisioning-diagnostics"))
        self.assertIn("`scratch-org-shape`", portfolio)
        self.assertIn("persistent or longer-lived", portfolio)
        self.assertIn("return that lifecycle constraint", portfolio.lower())
        self.assertIn("`scratch-org-shape`", diagnostics)
        self.assertIn("creation, entitlement, capacity, expiration, or cleanup", diagnostics)
        self.assertIn("Do not replace the definition recommendation", diagnostics)

    def test_current_platform_claims_require_source_refresh(self):
        content = skill_text("scratch-org-shape")
        refresh = (SKILLS / "scratch-org-shape" / "references" / "source-refresh.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("advisor-capability-preflight", content)
        self.assertIn("unknown", content)
        self.assertIn("Salesforce Docs MCP", refresh)

    def test_scenario_matrix_covers_the_reviewed_partner_decisions_and_smoke_test(self):
        scenarios = (ROOT / "tests" / "scratch-org-workflow-scenarios.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "## Scenario 1 — Minimal build-ready definition",
            "## Scenario 2 — Feature and companion-setting dependency",
            "## Scenario 3 — Misleading existing definition",
            "## Approval-gated manual smoke test",
        ):
            self.assertIn(heading, scenarios)
        self.assertIn("Do not commit credentials, aliases, org IDs, or live results.", scenarios)


if __name__ == "__main__":
    unittest.main()
