# ADR 003: Adopt Event-Driven Architecture for Payment Notifications

**Status:** Accepted  
**Date:** 2025-09-24  
**Authors:** Denis Blanari

## Context
Our current monolithic payment system processes notifications synchronously. This causes:
- Increased latency for downstream services
- Tight coupling between components
- Difficulty scaling under peak loads

Regulatory requirements also mandate reliable audit trails of notification delivery.

## Decision
We will adopt an **event-driven architecture** using **Kafka** as the backbone for payment notifications.
- Producers (payment services) will publish events.
- Consumers (notification, reporting, fraud detection) will subscribe asynchronously.

## Alternatives Considered
- **Continue synchronous REST callbacks:** Simple, but brittle and hard to scale.
- **RabbitMQ:** Familiar to team, but lacks replay and partition scalability needed.
- **Kafka (chosen):** Strong support for partitioning, ordering, and replay, aligns with long-term roadmap.

## Consequences
- **Positive:**
    - Decoupling services reduces maintenance costs.
    - Scalable event processing pipeline.
    - Built-in reliability (replay, durability).

- **Negative:**
    - Increased infrastructure complexity.
    - Team requires training in Kafka operations.
    - Higher operational overhead.

## Mitigation
- Provide training sessions for developers.
- Use managed Kafka (Confluent Cloud) to reduce ops burden.

## References
- [System Architecture Diagram v2](./docs/system-arch-v2.png)
- [Regulatory Compliance Guidelines](./docs/compliance.md)
- Related ADRs: ADR-001 (Service Decomposition), ADR-002 (API Gateway Adoption)  