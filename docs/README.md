# ADR Automation Solution Architecture

## Overview
This document describes the solution architecture for the ADR Automation system, which automates the creation, review, and management of Architecture Decision Records (ADRs) by integrating with tools like Jira, GitHub, and documentation sources. The system leverages event-driven processing, AI-powered content generation, and human-in-the-loop review via GitHub Pull Requests.

## Key Components

- **Producers / Sources**: Jira, Git/CI, and Docs/Wikis provide the initial data and triggers for ADR creation.
- **Input Gateway API**: Ingests and normalizes events and data from producers.
- **Topic (Kafka)**: Decouples producers and consumers, ensuring reliable event delivery.
- **Ingestion & Embedding**: Processes and embeds documents for semantic retrieval.
- **Vector DB (Pinecone/Weaviate/Chroma)**: Stores vector embeddings for semantic search and is the final destination for approved ADRs.
- **Metadata Store (PostgreSQL)**: Stores structured metadata about ADRs.
- **ADR Trigger Service (rules + classifier + OPA)**: Applies business rules and policies to trigger ADR proposals.
- **Retrieval Service (Vector kNN + filters + re-ranker)**: Retrieves relevant context for ADR generation.
- **LLM Orchestrator (ADR Generator)**: Uses LLMs to generate draft ADRs.
- **Workflow Engine (Temporal/Cadence)**: Orchestrates the ADR lifecycle and review process.
- **Review UI (GitHub Web UI)**: Human review and approval via GitHub Pull Requests.
- **Notifications (Email/Teams)**: Notifies stakeholders of review and publication events.

## Workflow Summary

1. **Event Ingestion**: Events from Jira, Git, or Docs are ingested and published to Kafka.
2. **Processing**: Data is processed and stored in the Vector DB and Metadata Store.
3. **Triggering**: Business rules and policies determine if an ADR proposal is needed.
4. **Context Retrieval**: Relevant context is gathered for ADR generation.
5. **Draft Generation**: LLM generates a draft ADR.
6. **Workflow Orchestration**: Review task is created as a GitHub Pull Request.
7. **Human Review**: Reviewers approve or reject the ADR draft in GitHub.
8. **Indexing**: Approved ADRs are indexed directly into the Vector DB.
9. **Notification**: Stakeholders are notified of review and publication status.

## Benefits
- Automation reduces manual effort and errors.
- All ADRs are indexed and auditable in the Vector DB.
- Event-driven, decoupled architecture supports scalability.
- Human-in-the-loop review ensures quality and consensus.
- Modular design allows easy integration of new sources and policies.
