# ADR-Copilot

## Custom GPT Agent – Project Structure

This repository is a **best-practice scaffold** for creating and tracking a Custom GPT agent, covering the entire lifecycle: design → build → integrate → evaluate → govern → iterate.

> **Project comments (what/why):**
> - Keep prompts, docs, specs, and governance artifacts **separated** and **versioned** for auditability.
> - Treat OpenAPI/Swagger specs as first-class assets; they define the agent's **capabilities boundary**.
> - Governance CSVs act as a **lightweight system of record** until you wire a proper DB.
> - Evaluations prevent **quality drift**; include red-team datasets and regression suites.
> - Never commit secrets; use environment variables or your platform’s secret store.

## Folder Overview

- `docs/` – Architecture, setup, and policy documentation.
- `prompt/` – System prompt and operator notes, with a dated `changelog/` for traceability.
- `openapi/` – Swagger/OpenAPI specs for external services (e.g., GitHub).
- `src/` – Example client and utilities (`auth.py`, `logging.py`).
- `evaluations/` – Datasets, run logs, and reports for reproducible testing.
- `governance/` – CSV logs for registry, prompt changes, evals, and incidents.
- `business/` – Business analysis artifacts:
    - `ba_overview.md`: Goals, scope, stakeholders, risks
    - `user_stories.md`: High-level user stories
    - `non_functional.md`: NFRs (latency, cost, privacy, availability)
    - `requirements.feature`: Acceptance criteria in Given/When/Then format
- `scripts/` – Automation helpers (diagram rendering, metric export).
- `tests/` – Optional unit/integration tests.
- `.gitignore`, `LICENSE`, `README.md` – Repo hygiene.

## Quick Start

1. **Clone** this repo or unzip the scaffold.
2. Configure a virtualenv (optional) and install any client deps in `src/`.
3. Upload `docs/` and `openapi/` to your Custom GPT as knowledge & actions.
4. Paste `prompt/system_prompt.txt` into your GPT **Instructions**.
5. Track changes in `governance/*.csv`; automate exports via `scripts/`.

## Governance Tables

See `governance/*.csv` for **Agent Registry**, **Prompt Changelog**, **Evaluation Runs**, and **Incidents** column definitions.

## Security & Privacy

- Enforce **least privilege** on every API (`openapi/` scopes).
- Mask/avoid PII; align with your **data retention** policy.
- Refuse destructive actions; log and review incidents in `governance/incidents.csv`.

## Extending

- Add more specs under `openapi/` (payments, search, internal services).
- Generate clients into `src/` (e.g., `openapi-generator`).
- Add CI to lint prompts/specs and run evals on PR.
