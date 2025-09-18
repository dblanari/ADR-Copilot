---
# ========= Front Matter (machine-readable) =========
id: "ADR-YYYYMMDD-<slug>"
title: "<Short, imperative decision title>"
status: "proposed"   # proposed | accepted | rejected | superseded | deprecated
date: "YYYY-MM-DD"
authors: ["<name>@<org>"]
reviewers: ["<name>@<org>"]
approvers: ["<name>@<org>"]     # required to move to accepted
project: "<project or product>"
component: "<service / domain / module>"
decision_type: "<architecture|security|data|process|tooling|governance>"
related_adrs: ["ADR-YYYYMMDD-...", "ADR-YYYYMMDD-..."]
issues: ["JIRA-123", "GH-456"]
tags: ["gpt-agent","payments","openapi"]
version: "1.0"
# ===================================================
---

# Architecture Decision Record: <Short Title>

> **Summary (1–2 sentences):**  
> <One-liner that a busy exec can read and understand.>

---

## 1. Context
<!-- Why a decision is needed now. Business drivers, constraints, assumptions. -->
**Business problem**: <what outcome we need, who benefits>  
**Constraints**: <time, budget, regulatory, tech>  
**Assumptions**: <things believed true>  
**Out of scope**: <explicitly excluded items>

## 2. Requirements (Given/When/Then)
<!-- Link to /business/requirements.feature if applicable -->
- **Functional**: <bulleted list or link>
- **Non-functional**: latency, availability, cost, scalability, UX, maintainability
- **Policies**: safety/privacy/usage policies the solution must respect

## 3. Options Considered
<!-- At least 2 realistic options, 3 preferred. -->
| Option | Description | Pros | Cons | Risks | Effort (S/M/L) | Cost ($/month) |
|---|---|---|---|---|---|---|
| <Option A> | <desc> | <bullets> | <bullets> | <bullets> | M | ~$ |
| <Option B> | <desc> | <bullets> | <bullets> | <bullets> | L | ~$ |
| <Option C> | <desc> | <bullets> | <bullets> | <bullets> | S | ~$ |

> **Evaluation notes:**  
> <Why some options are not viable; proof points, benchmarks, pilots, references.>

## 4. Decision
<!-- The selected option and why it wins. -->
**Chosen option**: <Option X>  
**Primary rationale**: <top 3 reasons (business + technical)>

## 5. Consequences
**Positive**
- <benefit 1>
- <benefit 2>

**Negative / Trade-offs**
- <trade-off 1>
- <new obligations, debt, vendor lock-in, complexity>

## 6. Architecture & Design Impact
- **Scope / Components**: <what changes, what stays>
- **APIs / Contracts**: <new/changed endpoints, versioning>
- **Data / Schema**: <new tables, migrations, retention>
- **Integration points**: <upstream/downstream systems>
- **Diagrams**: `docs/architecture.puml` (updated)

## 7. Security & Privacy
- **Threat model (STRIDE)**: <key threats + mitigations>
- **AuthN/AuthZ**: <method, scopes, roles, least privilege>
- **PII/Sensitive data**: <classification, masking, redaction>
- **Compliance**: <PCI/PSD2/GDPR/SOC2 impacts>
- **Secrets**: <storage, rotation, no hardcoding>

## 8. Non-Functional Targets (SLOs)
| Attribute | Target | Measurement |
|---|---|---|
| Latency p95 | <e.g., ≤ 2s> | <grafana link> |
| Availability | <e.g., 99.9%> | <status page/dash> |
| Cost cap | <$ / month> | <FinOps dashboard> |
| Observability | <logs/metrics/traces> | <links> |

## 9. Rollout & Migration Plan
- **Phases**: <pilot → limited rollout → GA>
- **Data migration**: <plan/backfill>
- **Feature flags**: <flags and kill switches>
- **Training/comms**: <docs, enablement>

## 10. Rollback Plan
- **Trigger conditions**: <what failure causes rollback>
- **Steps**: <how to restore previous state safely>
- **Data & config**: <reconciliation strategy>

## 11. Open Questions
- <unknowns that need follow-up>  

## 12. References
- <links to tickets, PRDs, prototypes, benchmarks, vendor docs, prior ADRs>

---

### Approval
<!-- Fill when status becomes "accepted". -->
- **Decision meeting/date**: <YYYY-MM-DD>
- **Approvers**: <names>
- **Result**: accepted | rejected | superseded | deprecated

### Change Log
- YYYY-MM-DD v1.0 — Initial proposal (author)
- YYYY-MM-DD v1.1 — Reviewer updates (who/what)
- YYYY-MM-DD v2.0 — Accepted; added rollout/rollback