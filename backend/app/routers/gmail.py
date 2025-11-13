from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.gmail_ingest import gmail_ingestor
from ..storage.gmail_token_store import gmail_token_store
from ..storage.message_store import message_store
from ..storage.state_store import state_store

router = APIRouter(prefix="/api/gmail", tags=["gmail"])


class SyncRequest(BaseModel):
  user_id: str
  max_messages: int = Field(100, ge=1, le=500)
  query: Optional[str] = None
  label_ids: Optional[List[str]] = None


@router.get("/status")
def gmail_status(user_id: str):
  record = gmail_token_store.load(user_id)
  if not record:
    return {"connected": False}

  state = state_store.get_state(user_id)
  summary = message_store.summary(user_id)
  return {
    "connected": True,
    "email": record.get("email"),
    "google_user_id": record.get("google_user_id"),
    "history_id": record.get("history_id"),
    "scopes": record.get("scope"),
    "last_checked_at": summary.get("last_checked_at"),
    "counts": summary.get("counts"),
    "total_indexed": summary.get("total"),
    "baseline_at": state.get("baseline_at"),
    "baseline_ready": state.get("baseline_ready"),
  }


@router.post("/sync/start")
def sync_gmail(payload: SyncRequest):
  try:
    messages = gmail_ingestor.poll(
      payload.user_id,
      max_messages=payload.max_messages,
      query=payload.query,
      label_ids=payload.label_ids,
    )
  except RuntimeError as exc:
    raise HTTPException(status_code=400, detail=str(exc)) from exc

  return {"processed": len(messages)}
