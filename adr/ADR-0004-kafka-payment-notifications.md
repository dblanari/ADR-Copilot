# ADR: Kafka-based Event-Driven Payment Notifications

\n**Date:** 2025-09-26   
**Status:** Proposed  
**Authors:** Denis Blanari  


---

@@ Context & Problem Statement
Notifications are currently processed synchronously in the legacy monolith. This has led to:
- High latency for downstream services (fraud detection, reporting).
- Frequent failures during peak loads.
- Lack of reliable replay mechanisms、Ö Exploration Document [9*Exploration_Document.md*L1-L12] 

The business requires a scalable, reliable, and auditable mechanism to deliver payment notifications.  

@@Drivers
- **Scalability:** Services must scale independently under peak load.  
- **Reliability:** Guaranteed delivery and ability to replay messages.  

- **Compliance:** Must align with PCI DSS (secure logging) and GDPR auditable records Ö Example-Standards-References.txt\tLq-1-L8  
- **Security:*** Encryption in transit and at rest, ACL support 、Ö Example-Standards-References.txt\tLq-13-L16  
- **Ecosystem Fit:** Move towards microservices and event-driven design、Ö Example-Standards-References.txt\tLq-9-L12   

@@ Considered Options
 1. **Continue with synchronous REST rest callbacks**
   — Very simple, minimal infra changes.  
   — Fragile under load, no replay, not compliant.  

@@ Decision
We will adopt **Kafka-based event-driven architecture** (using Confluent Cloud managed service where possible). This provides replay, durability, and scalability, while aligning with regulatory and internal standards.  

@@
@@ Consequences
 ### Positive
- Reduced latency (180 ms vs. 600+ ms in monolith)、Ö Proof-of-Concept-Results.md\Ll-6-L10  "
- Reliable replay and durability.  
- Scalable to thousands of messages per second.  
- Aligns with compliance and security requirements.  

### Negative
- Developer training required for Kafka consumer groups.  
- Higher operational complexity than RabbitMQQ8 Ö Proof-of-Concept-Results.md\Ll-12-L16  
- Vendor dependency if using managed Kafka.  

@@# References
- Exploration Document: Modernizing Payment Notification [9*Exploration_Document.md*\Ll1-L12]  
- PoC Results: Kafka-based Payment Notifications [10*Proof-of-Concept-Results.md\L1-L10]  
- Meeting Notes: Architecture Decision on Payment Notifications [11*Meeting-Notes.md\L11-L20]  
- Standards References: PCI DSS v.4.0, DGPR, CSCF Best Practices, IEEE 1471, Endava Architecture Playbook, Security Guidelines [12*Example-Standards-References.txt\L1-L16] 
