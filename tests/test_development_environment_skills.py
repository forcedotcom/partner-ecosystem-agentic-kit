import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
TEMPLATE_REFERENCE = (
    SKILLS / "scratch-org-shape" / "references" / "approved-scratch-org-templates.md"
)
MERGE_FIXTURES = ROOT / "tests" / "fixtures" / "scratch-org-template-merges.json"


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
        refresh = normalized(
            (SKILLS / "scratch-org-shape" / "references" / "source-refresh.md").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("advisor-capability-preflight", content)
        self.assertIn("unknown", content)
        for phrase in (
            "Salesforce Docs MCP",
            "sfdx_dev_scratch_orgs_def_file_config_values.htm",
            "meta_settings.htm",
            "sfdx_dev_scratch_orgs_editions_and_allocations.htm",
            "specific setting reference and its field documentation",
        ):
            self.assertIn(phrase, refresh)
        self.assertNotIn("- https://developer.\n", refresh)

    def test_approved_templates_define_the_canonical_baseline_and_research_path(self):
        templates = normalized(TEMPLATE_REFERENCE.read_text(encoding="utf-8"))
        skill = skill_text("scratch-org-shape")
        for phrase in (
            '"EnableSetPasswordInApi"',
            '"enableS1DesktopEnabled": true',
            '"enableUsersAreLightningOnly": true',
            '"enableLexEndUsersNoSwitching": true',
            '"enableS1EncryptedStoragePref2": false',
            "Read selectively",
            "source-refresh.md",
        ):
            self.assertIn(phrase, templates)
        self.assertIn("approved-scratch-org-templates.md", skill)

    def test_broad_product_requests_require_verified_setting_research(self):
        templates = TEMPLATE_REFERENCE.read_text(encoding="utf-8")
        skill = normalized(skill_text("scratch-org-shape"))
        scenarios = (ROOT / "tests" / "scratch-org-workflow-scenarios.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("up to three verified candidate settings groups", skill)
        self.assertNotIn("meta_industriessettings.htm", templates)
        self.assertNotIn("meta_claimfinancialsettings.htm", templates)
        self.assertIn("IndustriesSettings", scenarios)
        self.assertIn("ClaimFinancialSettings", scenarios)
        self.assertIn("meta_industriessettings.htm", scenarios)
        self.assertIn("meta_claimfinancialsettings.htm", scenarios)
        self.assertNotIn("industriesInsuranceSettings", scenarios)

    def test_template_json_fragments_are_valid_and_do_not_depend_on_ui(self):
        templates = TEMPLATE_REFERENCE.read_text(encoding="utf-8")
        fragments = re.findall(r"```json\n(.*?)\n```", templates, flags=re.DOTALL)
        self.assertEqual(20, len(fragments))
        for fragment in fragments:
            json.loads(fragment)
        self.assertNotIn("Package Visualizer", templates)

    def test_template_merges_match_data_driven_fixtures(self):
        templates = TEMPLATE_REFERENCE.read_text(encoding="utf-8")
        baseline = json.loads(
            re.search(
                r"## Canonical baseline\n\n```json\n(.*?)\n```", templates, flags=re.DOTALL
            ).group(1)
        )
        fragments = {
            name: json.loads(fragment)
            for name, fragment in re.findall(
                r"^### (.+?)\n\n```json\n(.*?)\n```", templates, flags=re.DOTALL | re.MULTILINE
            )
        }
        fixtures = json.loads(MERGE_FIXTURES.read_text(encoding="utf-8"))

        for fixture in fixtures:
            merged = {"features": list(baseline["features"]), "settings": dict(baseline["settings"])}
            for template_name in fixture["templates"]:
                fragment = fragments[template_name]
                merged["features"].extend(
                    feature for feature in fragment["features"] if feature not in merged["features"]
                )
                merged["settings"].update(fragment["settings"])
            self.assertEqual(fixture["expected"], merged, fixture["name"])

    def test_agent_metadata_has_a_specific_external_prompt(self):
        metadata = (SKILLS / "scratch-org-shape" / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("$scratch-org-shape", metadata)
        self.assertIn("project-scratch-def.json", metadata)

    def test_scenario_matrix_covers_the_reviewed_partner_decisions_and_smoke_test(self):
        scenarios = (ROOT / "tests" / "scratch-org-workflow-scenarios.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "## Scenario 1 — Minimal build-ready definition",
            "## Scenario 2 — Feature and companion-setting dependency",
            "## Scenario 3 — Misleading existing definition",
            "## Scenario 4 — Broad capability request",
            "## Approval-gated manual smoke test",
        ):
            self.assertIn(heading, scenarios)
        self.assertIn("Do not commit credentials, aliases, org IDs, or live results.", scenarios)


if __name__ == "__main__":
    unittest.main()
