# Test Scenario 1: Complete ADR Draft Validation

## Prompt
Please validate the following ADR draft:

---
# ADR: Payment Gateway Integration
Status: Proposed
Date: 2025-10-13
Decision ID: ADR-005

## Context
The payment system must support integration with multiple gateways to enable global transactions and redundancy.

## Decision
Integrate with Stripe, PayPal, and Adyen using a modular adapter pattern.

## Consequences
- Increased flexibility
- Higher maintenance cost

## Evidence
- Source: Exploration_Document.md, Location: Section 2, Relevance: Gateway requirements

## Assumptions
- (industry_standard) Modular adapters are widely used

---

## Expected Result
Validation summary with all checks passing (structure_compliance: pass, completeness: pass, evidence_traceability: pass, style_alignment: pass).

