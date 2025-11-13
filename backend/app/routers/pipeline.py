from __future__ import annotations

import logging
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.gmail_ingest import gmail_ingestor
from ..services.llm import gemini_client
from ..services.validator import validator_service
from ..services.planner import build_crm_plan
from ..services.hubspot_client import hubspot_client, oauth_manager
from ..storage.message_store import message_store

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])
logger = logging.getLogger(__name__)


class PipelineRequest(BaseModel):
  user_id: str = Field(..., description="Clerk user id / tenant id")
  max_messages: int = Field(3, ge=1, le=500)
  execute_hubspot: bool = False


@router.post("/run")
def run_pipeline(payload: PipelineRequest):
  start = time.perf_counter()
  try:
    messages = gmail_ingestor.poll(payload.user_id, max_messages=payload.max_messages)
  except RuntimeError as exc:
    raise HTTPException(status_code=400, detail=str(exc)) from exc

  results = []
  for message in messages:
    message_start = time.perf_counter()
    try:
      raw_json = gemini_client.analyze_email(message)
      extraction = validator_service.validate(message, raw_json)
      plan = build_crm_plan(message, extraction)

      hubspot_result = None
      portal_id = None
      if payload.execute_hubspot:
        connection = oauth_manager.get_connection(payload.user_id)
        if not connection:
          raise HTTPException(status_code=400, detail="HubSpot is not connected for this user")
        portal_id = connection.get("portal_id")
        hubspot_result = hubspot_client.execute_plan(payload.user_id, plan)

      message_store.update_status(
        payload.user_id,
        message.message_id,
        status="processed",
        crm_contact_id=(hubspot_result or {}).get("contact_id") if hubspot_result else None,
        crm_note_id=(hubspot_result or {}).get("note_id"),
        hubspot_portal_id=portal_id,
      )

      results.append(
        {
          "message_id": message.message_id,
          "extraction": extraction.model_dump(),
          "plan": plan.model_dump(),
          "hubspot": hubspot_result,
          "latency_ms": round((time.perf_counter() - message_start) * 1000, 2),
        }
      )
    except Exception as exc:
      logger.exception("Pipeline failed", extra={"message_id": message.message_id})
      message_store.update_status(payload.user_id, message.message_id, status="error", error=str(exc))

  return {"processed": len(results), "latency_ms": round((time.perf_counter() - start) * 1000, 2), "results": results}
