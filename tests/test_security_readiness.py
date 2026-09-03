import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SECURITY = ROOT / "skills" / "security-readiness"


class SecurityReadinessContractTests(unittest.TestCase):
    def setUp(self):
        self.skill = (SECURITY / "SKILL.md").read_text(encoding="utf-8")
        self.lifecycle = (SECURITY / "references" / "lifecycle-and-gates.md").read_text(
            encoding="utf-8"
        )
        self.dossier = (SECURITY / "references" / "evidence-dossier.md").read_text(
            encoding="utf-8"
        )
        self.refresh = (SECURITY / "references" / "source-refresh.md").read_text(
            encoding="utf-8"
        )
        self.testing = (SECURITY / "references" / "testing-and-scanners.md").read_text(
            encoding="utf-8"
        )
        self.portal = (SECURITY / "references" / "partner-security-portal.md").read_text(
            encoding="utf-8"
        )
        self.wizard = (SECURITY / "references" / "review-wizard-and-outcomes.md").read_text(
            encoding="utf-8"
        )
        self.report_intake = (
            SECURITY / "references" / "failed-review-report-intake.md"
        ).read_text(encoding="utf-8")
        self.agentforce = (
            SECURITY / "references" / "agentforce-and-client-security.md"
        ).read_text(encoding="utf-8")
        self.finding_ledger = (
            SECURITY / "references" / "finding-ledger.md"
        ).read_text(encoding="utf-8")
        self.evidence_first = (
            SECURITY / "references" / "evidence-first-assessment.md"
        ).read_text(encoding="utf-8")
        self.submission_decision = (
            SECURITY / "references" / "submission-decision.md"
        ).read_text(encoding="utf-8")

    def test_eligible_package_scenario_requires_all_lifecycle_gates(self):
        for gate in (
            "Documentation preflight",
            "Scope and eligibility",
            "Trust boundaries",
            "Evidence and analysis",
            "Remediation and retest",
            "Submission readiness",
            "Reviewer response and release",
        ):
            self.assertIn(gate, self.lifecycle)
        for status in ("`ready`", "`blocked`", "`not-applicable`", "`unknown`"):
            self.assertIn(status, self.lifecycle)
        self.assertIn("never a prediction of approval", self.skill)

    def test_blocked_pbo_or_candidate_scenario_preserves_owner_evidence(self):
        pbo = (ROOT / "skills" / "pbo-dev-hub-foundation" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        candidate = (ROOT / "skills" / "package-version-validation" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Security Review handoff", pbo)
        self.assertIn("PBO and Dev Hub ownership", pbo)
        self.assertIn("`Active`", pbo)
        pbo_practitioner = (
            ROOT / "skills" / "pbo-dev-hub-foundation" / "references" / "practitioner-knowledge.md"
        ).read_text(encoding="utf-8")
        self.assertIn("does not expose an Active/Trial status field", pbo_practitioner)
        self.assertIn("Security Review handoff", candidate)
        self.assertIn("exact candidate identity", candidate)
        self.assertIn("`blocked`", self.lifecycle)

    def test_managed_package_submission_requires_active_owning_pbo(self):
        self.assertIn("owning PBO Dev Hub", self.lifecycle)
        self.assertIn("verified `Active` status", self.lifecycle)
        self.assertIn("not evidence of Active status", self.lifecycle)

    def test_security_review_query_targets_the_owning_pbo_dev_hub(self):
        self.assertIn("`IsSecurityReviewed`", self.lifecycle)
        self.assertIn("package-owning PBO Dev Hub—not the submitted", self.lifecycle)
        self.assertIn("does not replace the partner's Partner", self.lifecycle)

    def test_reviewed_and_ready_to_list_candidate_does_not_trigger_duplicate_review(self):
        self.assertIn("`IsSecurityReviewed = true`", self.lifecycle)
        self.assertIn("listing readiness as `Ready to List`", self.lifecycle)
        self.assertIn("a new Security Review submission is not needed", self.lifecycle)
        self.assertIn("candidate or solution scope has changed", self.lifecycle)

    def test_test_org_access_does_not_authorize_execution(self):
        normalized_dossier = self.dossier.replace("\n", " ")
        self.assertIn("Environment Hub", normalized_dossier)
        self.assertIn("does not authorize", normalized_dossier)
        self.assertIn("explicit approval", normalized_dossier)

    def test_expiring_test_org_blocks_submission_readiness(self):
        self.assertIn("non-expiring Developer Edition", self.lifecycle)
        self.assertIn("must not have a scheduled expiration date", self.dossier)
        self.assertIn("Security Review Operations verification", self.dossier)

    def test_test_org_requires_working_use_case_configuration(self):
        self.assertIn("working-use-case configuration", self.lifecycle)
        self.assertIn("working state for the in-scope use cases", self.dossier)
        self.assertIn("otherwise unconfigured org is not evidence", self.dossier)

    def test_reviewer_assets_are_architecture_specific(self):
        self.assertIn("reviewer-ready asset bundle", self.lifecycle)
        self.assertIn("architecture or data-flow diagram", self.dossier)
        self.assertIn("setup and test instructions", self.dossier)
        self.assertIn("Do not require a universal diagram or setup template", self.dossier)

    def test_source_tag_or_commit_is_optional_provenance(self):
        self.assertIn("tag or commit is useful optional provenance", self.dossier)
        self.assertIn("commit may be\n  recorded as optional provenance", self.report_intake)

    def test_api_integration_scenario_requires_a_trust_boundary_inventory(self):
        implementation = (ROOT / "skills" / "implementation-best-practices" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("connected APIs or integrations", self.skill)
        self.assertIn("data flows, identities, permissions", implementation)
        self.assertIn("API/integration boundary", self.dossier)
        self.assertIn("Keep secrets, credentials", self.dossier)

    def test_agentforce_action_and_prompt_boundaries_are_explicit(self):
        implementation = (ROOT / "skills" / "implementation-best-practices" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Agentforce custom actions", self.agentforce)
        self.assertIn("CRUD, FLS, and record-level access checks", self.agentforce)
        self.assertIn("`VerifiedCustomerId`", self.agentforce)
        self.assertIn("require user confirmation", self.agentforce)
        self.assertIn("must not contain sensitive or secret data", self.agentforce)
        self.assertIn("new\nsecure random enclosure for every inference", self.agentforce)
        self.assertIn("action audience and public/private classification", implementation)
        self.assertIn("prompt data sources and\ninjection mitigations", implementation)

    def test_agentforce_assessment_inspects_source_before_partner_interview(self):
        self.assertIn("Evidence-first Agentforce assessment", self.agentforce)
        self.assertIn("inspect that evidence before interviewing", self.agentforce)
        self.assertIn("user-controlled identifiers", self.agentforce)
        self.assertIn("random enclosure/sandwiching evidence", self.agentforce)
        self.assertIn("runtime\nconfirmation behavior", self.agentforce)
        self.assertIn("Do not infer safety from the absence", self.agentforce)

    def test_dossier_preserves_agentforce_control_evidence_without_sensitive_artifacts(self):
        self.assertIn("Agentforce controls", self.dossier)
        self.assertIn("control category, factual source observation", self.dossier)
        self.assertIn("Do not include prompt text, source excerpts", self.dossier)
        self.assertIn("directly observed\n  control", self.dossier)
        self.assertIn("unprovable runtime control is `unknown`", self.dossier)

    def test_agentforce_reviewer_route_is_architecture_specific_and_read_only_in_assess(self):
        self.assertIn("Agentforce reviewer test route", self.agentforce)
        self.assertIn("rather than a generic Agentforce setup checklist", self.agentforce)
        self.assertIn("exact installed\ncandidate", self.agentforce)
        self.assertIn("only the steps that\napply", self.agentforce)
        self.assertIn("Do not configure the environment, activate an action", self.agentforce)

    def test_connected_app_or_eca_boundary_requires_current_controls_and_test(self):
        self.assertIn("more than two customer production orgs", self.agentforce)
        self.assertIn("PKCE, refresh-token rotation", self.agentforce)
        self.assertIn("30-day idle\nrefresh-token TTL", self.agentforce)
        self.assertIn("documented callback-URL conditions", self.agentforce)
        self.assertIn("Test all integrations after enabling controls", self.agentforce)

    def test_finding_and_false_positive_scenario_requires_retest_evidence(self):
        packageability = (ROOT / "skills" / "packageability-assessment" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        operations = (ROOT / "skills" / "operations-release" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("false-positive explanation", packageability)
        self.assertIn("retest evidence", self.dossier)
        self.assertIn("retest evidence", operations)
        self.assertIn("do not silently suppress a finding", self.dossier)

    def test_unavailable_current_policy_scenario_remains_unknown(self):
        self.assertIn("Salesforce Docs MCP", self.refresh)
        self.assertIn("approved", self.refresh)
        self.assertIn("Partner Community", self.refresh)
        self.assertIn("result as `unknown`", self.refresh)
        self.assertIn("Do not relabel a missing, stale, or inaccessible source as a fact", self.skill)

    def test_current_policy_refresh_records_capability_and_public_source_boundaries(self):
        self.assertIn("Refresh receipt: 2026-09-03", self.refresh)
        self.assertIn("no exposed Salesforce Docs MCP tools", self.refresh)
        self.assertIn("official-web\nfallback", self.refresh)
        self.assertIn("does not make inaccessible Partner Community", self.refresh)

    def test_salesforce_review_stages_are_distinct_from_readiness_gates(self):
        self.assertIn("five Salesforce review stages", self.lifecycle)
        for stage in ("submission", "verification", "queue", "testing", "results"):
            self.assertIn(stage, self.lifecycle.lower())
        self.assertIn("seven readiness gates", self.lifecycle)

    def test_listing_readiness_inheritance_routes_to_ancestry(self):
        ancestry = (ROOT / "skills" / "package-ancestry-dependencies" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Security Review handoff", ancestry)
        self.assertIn("listing-readiness inheritance", ancestry)
        self.assertIn("managed-released", self.lifecycle)
        self.assertIn("Security Review Required", self.lifecycle)

    def test_submission_materials_follow_solution_architecture(self):
        for material in (
            "Developer Edition",
            "Managed package",
            "external component credentials",
            "Code Analyzer",
            "Checkmarx",
            "DAST",
            "false-positive",
            "base and dependent packages",
        ):
            self.assertIn(material, self.dossier)
        self.assertIn("when all base solutions have passed", self.dossier)
        self.assertIn("unreviewed base solutions", self.dossier)
        self.assertIn("complete solution", self.dossier)

    def test_checklist_builder_is_optional_partner_evidence(self):
        normalized_dossier = self.dossier.replace("\n", " ")
        self.assertIn("https://checklistbuilder.herokuapp.com/", normalized_dossier)
        self.assertIn("partner-provided working artifact", normalized_dossier)
        self.assertIn("not current Salesforce policy", normalized_dossier)

    def test_scanner_delegation_uses_sf_skills_without_replacing_review_evidence(self):
        for skill_name in (
            "dx-code-analyzer-run",
            "dx-code-analyzer-configure",
            "dx-code-analyzer-custom-rule-create",
        ):
            self.assertIn(skill_name, self.testing)
        self.assertIn("AppExchange", self.testing)

    def test_code_analyzer_evidence_is_version_aware_and_requires_engine_completion(self):
        normalized_testing = self.testing.replace("\n", " ")
        self.assertIn("installed Salesforce CLI and Code Analyzer plugin\nversions", self.testing)
        self.assertIn("flags accepted by that\ninstalled version", self.testing)
        self.assertIn("must not apply\nfixes without a separate", self.testing)
        self.assertIn("each engine's completion state", normalized_testing)
        self.assertIn("not a clean all-engine\nresult", self.testing)
        self.assertIn("Recommended:Security", self.testing)

    def test_partner_security_portal_routes_support_by_question_type(self):
        self.assertIn("Author Apex", self.portal)
        self.assertIn("Manage Listings", self.portal)
        self.assertIn("three", self.portal)
        self.assertIn("Operations office hours", self.portal)
        self.assertIn("Technical office hours", self.portal)
        self.assertIn("Do not collect", self.portal)

    def test_failed_review_requires_issue_type_remediation_and_rescan(self):
        self.assertIn("representative", self.lifecycle)
        self.assertIn("all instances", self.lifecycle)
        self.assertIn("rerun", self.lifecycle)
        self.assertIn("resubmit", self.lifecycle)

    def test_wizard_separates_drafts_returns_results_and_expiry(self):
        normalized_wizard = self.wizard.replace("\n", " ")
        for state in ("Save & Exit", "Returned", "View Report", "Expired"):
            self.assertIn(state, normalized_wizard)
        self.assertIn("Request a Second Look", normalized_wizard)
        self.assertIn("all vulnerabilities", normalized_wizard.lower())
        self.assertIn("not a failed security review", normalized_wizard.lower())

    def test_failed_review_report_is_sensitive_and_not_exhaustive(self):
        normalized_report = self.report_intake.replace("\n", " ")
        self.assertIn("not exhaustive", normalized_report)
        self.assertIn("do not execute", normalized_report.lower())
        self.assertIn("all instances", normalized_report)
        self.assertIn("Candidate practitioner knowledge", normalized_report)
        self.assertIn("approved AI environment", normalized_report)

    def test_false_positive_response_and_successor_candidate_are_traceable(self):
        normalized_report = self.report_intake.replace("\n", " ")
        self.assertIn("code location", normalized_report)
        self.assertIn("Code Quality", normalized_report)
        self.assertIn("released or promoted package version", normalized_report)
        version = (ROOT / "skills" / "package-version-validation" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        promotion = (ROOT / "skills" / "package-release-promotion" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("successor candidate", version)
        self.assertIn("remediation successor candidate", promotion)

    def test_finding_ledger_separates_private_detail_from_portable_summary(self):
        normalized_ledger = self.finding_ledger.replace("\n", " ")
        self.assertIn("two-layer", self.finding_ledger)
        self.assertIn("approved, access-controlled location", self.finding_ledger)
        self.assertIn("Portable dossier summary", self.finding_ledger)
        self.assertIn("Do not copy report excerpts, code locations, endpoints, credentials", normalized_ledger)
        self.assertIn("source classification", self.finding_ledger)

    def test_finding_ledger_has_complete_disposition_and_coverage_models(self):
        for disposition in (
            "`open`",
            "`remediating`",
            "`fixed-awaiting-retest`",
            "`fixed-verified`",
            "`false-positive`",
            "`not-applicable`",
        ):
            self.assertIn(disposition, self.finding_ledger)
        for coverage in ("`complete`", "`partial`", "`unavailable`", "`not-applicable`"):
            self.assertIn(coverage, self.finding_ledger)
        self.assertIn("coverage record, not a vulnerability finding", self.finding_ledger.replace("\n", " "))
        self.assertIn("rather than treating it as first-party code or silently excluding it", self.finding_ledger.replace("\n", " "))

    def test_bounded_reassessment_reuses_findings_and_preserves_authority(self):
        self.assertIn("Bounded reassessment", self.finding_ledger)
        self.assertIn("reuse its detailed-ledger\nrecord", self.finding_ledger)
        self.assertIn("Assess the\nsupplied delta read-only", self.finding_ledger)
        self.assertIn("It is not a new whole-solution certification", self.finding_ledger)
        self.assertIn("Do not rerun a\nscan, modify source, configure an org", self.finding_ledger)

    def test_reassessment_scenarios_require_candidate_alignment_and_route_retest(self):
        scenario_path = ROOT / "tests" / "fixtures" / "security_review_reassessment_scenarios.json"
        scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))

        def reassessment_disposition(scenario):
            if not scenario["candidate_aligned"]:
                return "unknown"
            if not scenario["control_present_in_successor"]:
                return "blocked"
            if not scenario["configured_route_retested"]:
                return "fixed-awaiting-retest"
            return "fixed-verified"

        for scenario in scenarios:
            self.assertEqual(
                reassessment_disposition(scenario),
                scenario["expected_disposition"],
                scenario["name"],
            )

    def test_finding_ledger_scenarios_enforce_gate_five_decisions(self):
        scenario_path = ROOT / "tests" / "fixtures" / "security_review_finding_ledger_scenarios.json"
        scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))

        def gate_five_status(records):
            if any(not record.get("candidate_aligned", True) for record in records):
                return "unknown"
            if any(record["coverage"] in {"partial", "unavailable"} for record in records):
                return "blocked"
            for record in records:
                if record["record_type"] != "finding":
                    continue
                if record["disposition"] in {"open", "remediating", "fixed-awaiting-retest"}:
                    return "blocked"
                if record["disposition"] == "fixed-verified" and not record.get(
                    "retest_candidate_matches", False
                ):
                    return "blocked"
                if record["disposition"] == "false-positive" and not record.get(
                    "false_positive_complete", False
                ):
                    return "blocked"
            return "ready"

        for scenario in scenarios:
            self.assertEqual(
                gate_five_status(scenario["records"]),
                scenario["expected_gate_5"],
                scenario["name"],
            )

    def test_synthetic_ledger_scenarios_do_not_embed_partner_evidence(self):
        fixture = (
            ROOT / "tests" / "fixtures" / "security_review_finding_ledger_scenarios.json"
        ).read_text(encoding="utf-8")
        for disallowed in ("Package Visualizer", "/Users/", "04t", "00D", "password", "endpoint"):
            self.assertNotIn(disallowed, fixture)

    def test_assess_mode_inspects_approved_evidence_before_interview_questions(self):
        self.assertIn("approved evidence before asking questions", self.skill)
        self.assertIn("Inspect before asking", self.evidence_first)
        self.assertIn("Do not ask whether an action, prompt, callout", self.evidence_first)
        self.assertIn("partner-supplied candidate alignment", self.evidence_first)

    def test_evidence_first_scenarios_preserve_authority_and_question_boundaries(self):
        scenario_path = ROOT / "tests" / "fixtures" / "security_review_evidence_first_scenarios.json"
        scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))
        direct_checks = {
            "sfdx-project": {"package-candidate"},
            "package-metadata": {
                "action-inventory",
                "prompt-inventory",
                "packaged-access-boundaries",
            },
            "apex-source": {"callout-paths", "authorization-markers"},
            "agentforce-metadata": {
                "action-inventory",
                "prompt-inventory",
                "action-input-and-confirmation-markers",
                "prompt-injection-and-output-handling-markers",
            },
        }

        for scenario in scenarios:
            if not scenario["read_only_authorized"]:
                self.assertEqual(scenario["expected_route"], "ask", scenario["name"])
                self.assertEqual(scenario["expected_direct_checks"], [], scenario["name"])
                self.assertEqual(
                    scenario["expected_owner_questions"], ["read-only-approval"], scenario["name"]
                )
                continue

            observed_checks = set()
            for evidence in scenario["available_evidence"]:
                observed_checks.update(direct_checks[evidence])
            self.assertEqual(scenario["expected_route"], "inspect", scenario["name"])
            self.assertSetEqual(observed_checks, set(scenario["expected_direct_checks"]), scenario["name"])
            self.assertTrue(scenario["expected_owner_questions"], scenario["name"])

    def test_evidence_first_fixture_contains_no_partner_artifacts(self):
        fixture = (
            ROOT / "tests" / "fixtures" / "security_review_evidence_first_scenarios.json"
        ).read_text(encoding="utf-8")
        for disallowed in ("Package Visualizer", "/Users/", "04t", "00D", "password", "credential value"):
            self.assertNotIn(disallowed, fixture)

    def test_gate_six_distinguishes_recommendation_from_gate_status(self):
        normalized_decision = self.submission_decision.replace("\n", " ")
        self.assertIn("not a gate status", self.submission_decision)
        self.assertIn("does not authorize, prohibit, or perform", normalized_decision)
        self.assertIn("The partner may still choose to submit", self.submission_decision)
        self.assertIn("submission recommendation", self.lifecycle)

    def test_submission_decision_scenarios_apply_precedence_and_partner_control(self):
        scenario_path = ROOT / "tests" / "fixtures" / "security_review_submission_decision_scenarios.json"
        scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))

        def submission_outcome(scenario):
            if "blocked" in scenario["gate_statuses"]:
                return "blocked"
            if (
                "unknown" in scenario["gate_statuses"]
                or not scenario["candidate_aligned"]
                or not scenario["policy_known"]
                or not scenario["scope_unchanged"]
            ):
                return "unknown"
            if scenario["security_reviewed"] and scenario["listing_ready"]:
                return "not-required"
            return "ready"

        for scenario in scenarios:
            self.assertEqual(
                submission_outcome(scenario),
                scenario["expected_outcome"],
                scenario["name"],
            )

    def test_lifecycle_scenarios_preserve_evidence_first_and_submission_boundaries(self):
        scenario_path = ROOT / "tests" / "fixtures" / "security_review_lifecycle_scenarios.json"
        scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))

        def assess_route(scenario):
            return "inspect" if scenario["read_only_authorized"] else "ask"

        def submission_outcome(scenario):
            if "blocked" in scenario["gate_statuses"]:
                return "blocked"
            if (
                "unknown" in scenario["gate_statuses"]
                or not scenario["candidate_aligned"]
                or not scenario["policy_known"]
            ):
                return "unknown"
            if (
                scenario["security_reviewed"]
                and scenario["listing_ready"]
                and scenario["scope_unchanged"]
            ):
                return "not-required"
            if all(status in {"ready", "not-applicable"} for status in scenario["gate_statuses"]):
                return "ready"
            return "unknown"

        for scenario in scenarios:
            self.assertEqual(
                assess_route(scenario), scenario["expected_assess_route"], scenario["name"]
            )
            self.assertEqual(
                submission_outcome(scenario), scenario["expected_outcome"], scenario["name"]
            )
            self.assertTrue(scenario["source_evidence"], scenario["name"])
            self.assertTrue(scenario["must_not_claim_approval"], scenario["name"])

        self.assertIn("`ready`: required evidence is present", self.lifecycle)
        self.assertIn("never a prediction of approval", self.skill)

    def test_submission_decision_fixture_contains_no_partner_artifacts(self):
        fixture = (
            ROOT / "tests" / "fixtures" / "security_review_submission_decision_scenarios.json"
        ).read_text(encoding="utf-8")
        for disallowed in ("Package Visualizer", "/Users/", "04t", "00D", "password", "endpoint"):
            self.assertNotIn(disallowed, fixture)

    def test_all_named_contributors_define_a_security_review_handoff(self):
        contributors = (
            "packaging-distribution",
            "packageability-assessment",
            "pbo-dev-hub-foundation",
            "package-version-validation",
            "package-ancestry-dependencies",
            "package-release-promotion",
            "namespace-access-governance",
            "implementation-best-practices",
            "platform-constraints",
            "operations-release",
        )
        for contributor in contributors:
            content = (ROOT / "skills" / contributor / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Security Review handoff", content, contributor)
            self.assertIn("Security & Readiness", content, contributor)

    def test_security_readiness_routes_only_to_existing_local_references(self):
        referenced = re.findall(r"references/([A-Za-z0-9_.-]+\.md)", self.skill)
        self.assertGreater(len(referenced), 0)
        for reference in referenced:
            self.assertTrue((SECURITY / "references" / reference).is_file(), reference)


if __name__ == "__main__":
    unittest.main()
