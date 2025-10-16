# Test Scenario 3: Evidence Traceability Check

## Prompt
Please validate the following ADR draft:

---
# ADR: Payment Gateway Integration
Status: Proposed
Date: 2025-10-13
Decision ID: ADR-007

## Context
The payment system must support integration with multiple gateways to enable global transactions and redundancy.

## Decision
Integrate with Stripe, PayPal, and Adyen using a modular adapter pattern.

## Consequences
- Increased flexibility
- Higher maintenance cost

## Assumptions
- (industry_standard) Modular adapters are widely used

---

## Expected Result
Validation summary with moderate severity (evidence_traceability: fail, severity: moderate) flagging missing evidence section.
