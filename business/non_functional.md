# Non-Functional Requirements

- **Latency:** Responses must complete within 2 seconds p95.
- **Cost:** Average token cost must not exceed budget thresholds ($300/month).
- **Availability:** 99.9% uptime target for API integrations.
- **Privacy:** No storage of PII; all responses must redact sensitive data.
- **Security:** Use least-privilege API scopes and encrypted tokens.

- **ADR Validation:** ≥95% of generated ADRs must pass automated validation for completeness (drivers, options, decision, consequence, traceability).
- **Traceability:** All ADRs must be linked to source signals (emails, chats, issues, PRs, RFCs) and supersession history.
- **Compliance:** ADRs must strictly adhere to MADR format and section requirements.
- **Integration:** Must support GitHub workflows for ADR branching, PRs, and tagging.
- **Supersession:** Never overwrite existing ADRs; only create new superseding records.
- **Auditability:** Weekly automated audits and incident triage workflow must be in place.
