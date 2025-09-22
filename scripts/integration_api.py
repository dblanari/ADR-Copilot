# integration_api.py
"""
Python (FastAPI) Integration API with three endpoints:
  - POST /putPrompt: enqueue a prompt to be later fetched by the LLM
  - GET  /getPrompt: fetch/lease the next prompt to be processed
  - POST /postResponse: submit the LLM output back to the system (idempotent)

Notes:
- In-memory storage for demo purposes (swap with DB/queue in prod).
- No console enqueue anymore (replaced by /putPrompt).
- Swagger UI: http://127.0.0.1:8000/docs
Run:
  pip install fastapi uvicorn pydantic
  uvicorn integration_api:app --reload
"""
from __future__ import annotations

import hashlib
import logging
import threading
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# ---------------------------
# In-memory stores (demo)
# ---------------------------
class Task(BaseModel):
    taskId: str
    prompt: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    dedupeKey: Optional[str] = None
    leaseUntil: Optional[datetime] = None
    completed: bool = False

class ResponseUsage(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

class ResponseEnvelope(BaseModel):
    taskId: str
    content: str
    usage: Optional[ResponseUsage] = None
    traceId: Optional[str] = None
    dedupeKey: Optional[str] = None

class PromptEnvelope(BaseModel):
    taskId: str
    prompt: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    dedupeKey: Optional[str] = None

class PutPromptRequest(BaseModel):
    prompt: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    dedupeKey: Optional[str] = None
    taskId: Optional[str] = None  # optional client-provided id

class PutPromptResponse(BaseModel):
    taskId: str
    dedupeKey: str

# Thread-safe in-memory queues
_TASKS: List[Task] = []
_RESPONSES: Dict[str, ResponseEnvelope] = {}
_LOCK = threading.RLock()

# Metrics (very simple)
METRICS = {
    "prompts_enqueued": 0,
    "prompts_fetched": 0,
    "responses_posted": 0,
    "leases_expired": 0,
}

# ---------------------------
# Helpers
# ---------------------------

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _sha256(s: str) -> str:
    import hashlib as _h
    return _h.sha256(s.encode("utf-8")).hexdigest()


def enqueue_prompt(prompt: str, meta: Optional[Dict[str, Any]] = None, dedupe_key: Optional[str] = None, task_id: Optional[str] = None) -> Task:
    with _LOCK:
        task = Task(
            taskId=task_id or str(uuid.uuid4()),
            prompt=prompt.strip(),
            meta=meta or {},
        )
        task.dedupeKey = dedupe_key or _sha256(task.taskId)
        _TASKS.append(task)
        METRICS["prompts_enqueued"] += 1
        logging.info("Enqueued task %s", task.taskId)
        return task


def _pick_next_ready_task() -> Optional[int]:
    """Return index of a ready (not completed, not leased or lease expired) task."""
    now = _now()
    expired_count = 0
    with _LOCK:
        for i, t in enumerate(_TASKS):
            if t.completed:
                continue
            if t.leaseUntil and t.leaseUntil > now:
                # still leased
                continue
            if t.leaseUntil and t.leaseUntil <= now:
                expired_count += 1
            return i
    if expired_count:
        with _LOCK:
            METRICS["leases_expired"] += expired_count
    return None

# ---------------------------
# FastAPI app
# ---------------------------
app = FastAPI(title="Custom GPT ↔ Integration API", version="1.1.0")

@app.get("/healthz")
def healthz():
    return {"ok": True, "time": _now().isoformat()}

@app.get("/metrics")
def get_metrics():
    with _LOCK:
        return dict(METRICS)

@app.post("/putPrompt", response_model=PutPromptResponse)
def put_prompt(body: PutPromptRequest):
    if not body.prompt or not body.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt is required")
    task = enqueue_prompt(body.prompt, meta=body.meta, dedupe_key=body.dedupeKey, task_id=body.taskId)
    return PutPromptResponse(taskId=task.taskId, dedupeKey=task.dedupeKey or _sha256(task.taskId))

@app.get("/getPrompt", response_model=PromptEnvelope, responses={204: {"description": "No prompt available"}})
def get_prompt(leaseSeconds: int = Query(120, ge=10, le=600)):
    idx = _pick_next_ready_task()
    if idx is None:
        return _no_content()

    with _LOCK:
        task = _TASKS[idx]
        task.leaseUntil = _now() + timedelta(seconds=leaseSeconds)
        METRICS["prompts_fetched"] += 1
        payload = PromptEnvelope(taskId=task.taskId, prompt=task.prompt, meta=task.meta, dedupeKey=task.dedupeKey)
        logging.info("Leased task %s until %s", task.taskId, task.leaseUntil.isoformat())
        return payload


def _no_content():
    from fastapi.responses import Response
    return Response(status_code=204)

@app.post("/postResponse")
def post_response(body: ResponseEnvelope):
    with _LOCK:
        # Validate task exists
        task = next((t for t in _TASKS if t.taskId == body.taskId), None)
        if task is None:
            raise HTTPException(status_code=404, detail="Unknown taskId")

        # Idempotency: drop duplicates by dedupeKey
        if body.dedupeKey and body.dedupeKey in _RESPONSES:
            logging.info("Duplicate response for dedupeKey=%s dropped", body.dedupeKey)
            return {"ok": True, "version": "idem"}

        # Mark completed and store response
        task.completed = True
        key = body.dedupeKey or task.dedupeKey or _sha256(body.taskId)
        body.dedupeKey = key
        _RESPONSES[key] = body
        METRICS["responses_posted"] += 1
        logging.info("Response stored for task %s (key=%s)", body.taskId, key)
        return {"ok": True, "version": "v1"}
