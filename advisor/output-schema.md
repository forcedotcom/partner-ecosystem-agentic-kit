# Shared output schema

Use this response shape for a partner-facing advisor result. Omit fields that
do not apply, but preserve the evidence labels and approval boundary.

```yaml
partner_response: "Exact response shown to the partner."
objective: "..."
mode: ask|assess|act
primary_skill: solution-discovery|packaging-distribution|development-environment|implementation-best-practices|platform-constraints|security-readiness|operations-release
supporting_skills: [] # canonical skill IDs only
recommendation: "..."
confidence: high|medium|low
evidence:
  - source_id: "..."
    type: fact|practitioner_knowledge|repository|inference|recommendation|assumption|unknown
    finding: "..."
assumptions: []
unknowns: []
risks: []
proposed_actions: []
approval_required: true|false
validation: []
```
