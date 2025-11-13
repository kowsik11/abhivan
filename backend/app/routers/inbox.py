from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from ..storage.message_store import message_store

router = APIRouter(prefix="/api/inbox", tags=["inbox"])


@router.get("/summary")
def inbox_summary(user_id: str):
  if not user_id:
    raise HTTPException(status_code=400, detail="Missing user_id")
  return message_store.summary(user_id)


@router.get("/messages")
def inbox_messages(
  user_id: str,
  status: str = Query("new", description="new | processed | error | all"),
  query: str | None = None,
  limit: int = Query(50, ge=1, le=200),
):
  status = status.lower()
  status_filter = None if status == "all" else status
  if status_filter and status_filter not in {"new", "processed", "error"}:
    raise HTTPException(status_code=400, detail="Invalid status filter")
  messages = message_store.list_messages(user_id, status=status_filter, query=query, limit=limit)
  return {"status": status, "count": len(messages), "messages": messages}


@router.get("/messages/{message_id}")
def inbox_message_detail(user_id: str, message_id: str):
  record = message_store.get(user_id, message_id)
  if not record:
    raise HTTPException(status_code=404, detail="Message not found")
  return record
