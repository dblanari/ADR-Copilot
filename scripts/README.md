# Integration API (FastAPI)

A lightweight **Integration API** that bridges a Custom GPT with an external system. It supports enqueueing prompts, leasing them for processing, and posting responses back.

---

## Features
- **POST /putPrompt** → enqueue a new task with a prompt
- **GET /getPrompt** → lease the next ready prompt for processing
- **POST /postResponse** → submit the LLM-generated output (idempotent)
- **GET /metrics** → simple in-memory metrics
- **GET /healthz** → health check

---

## Installation
```bash
pip install fastapi uvicorn pydantic
python3 -m pip install fastapi uvicorn pydantic
```

---

## Run the Server
```bash
uvicorn integration_api:app --reload
python3 -m uvicorn integration_api:app --reload
cloudflared tunnel --url http://localhost:8000
```

Default server runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

### 1. Enqueue a Prompt
`POST /putPrompt`

**Request Body:**
```json
{
  "prompt": "Translate this to French: Hello world",
  "meta": { "locale": "fr-FR" },
  "dedupeKey": "optional-string",
  "taskId": "optional-client-id"
}
```

**Response:**
```json
{
  "taskId": "uuid",
  "dedupeKey": "sha256-or-provided"
}
```

---

### 2. Fetch a Prompt
`GET /getPrompt?leaseSeconds=120`

**Response (200):**
```json
{
  "taskId": "uuid",
  "prompt": "Translate this to French: Hello world",
  "meta": { "locale": "fr-FR" },
  "dedupeKey": "sha256-or-provided"
}
```

**Response (204):**
```
No prompt available
```

---

### 3. Submit a Response
`POST /postResponse`

**Request Body:**
```json
{
  "taskId": "uuid",
  "content": "Bonjour le monde",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 5,
    "total_tokens": 15
  },
  "traceId": "trace-123"
}
```

**Response:**
```json
{
  "ok": true,
  "version": "v1"
}
```

Idempotent by `dedupeKey`.

---

### 4. Metrics & Health
- `GET /metrics` → `{ "prompts_enqueued": 1, "prompts_fetched": 1, "responses_posted": 1, "leases_expired": 0 }`
- `GET /healthz` → `{ "ok": true, "time": "..." }`

---

## Example Flow
```bash
# Enqueue a prompt
curl -X POST http://127.0.0.1:8000/putPrompt \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Summarize: The sky is blue due to Rayleigh scattering."}'

# Fetch a prompt
curl 'http://127.0.0.1:8000/getPrompt?leaseSeconds=60'

# Post response
curl -X POST http://127.0.0.1:8000/postResponse \
  -H 'Content-Type: application/json' \
  -d '{"taskId":"<from getPrompt>","content":"Short summary here"}'
```

---

## Next Steps
- Add persistence (SQLite, Redis, or message queue)
- Secure endpoints with Bearer tokens or mTLS
- Deploy behind API Gateway / reverse proxy