from __future__ import annotations

import json
import os

from .services.gmail_ingest import gmail_ingestor
from .services.llm import gemini_client
from .services.validator import build_validation_service
from .services.planner import build_crm_plan
from .services.zoho_client import crm_client, oauth_manager


def run_once(max_messages: int = 1, user_id: str | None = None, execute_zoho: bool = False) -> None:
  if not user_id:
    raise RuntimeError("CLI_USER_ID is required to poll Gmail")

  validation_service = build_validation_service(gemini_client)
  messages = gmail_ingestor.poll(user_id, max_messages=max_messages)

  for message in messages:
    raw_json = gemini_client.analyze_email(message)
    extraction = validation_service.validate(message, raw_json)
    plan = build_crm_plan(message, extraction)
    crm_result = None
    if execute_zoho:
      connection = oauth_manager.get_connection_info(user_id)
      if not connection:
        raise RuntimeError("Zoho is not connected for the provided user_id")
      crm_result = crm_client.execute_plan(user_id, plan, message.message_id)

    output = {
      "message_id": message.message_id,
      "extraction": extraction.model_dump(),
      "plan": plan.model_dump(),
      "crm": crm_result.model_dump() if crm_result else None,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
  user_id_env = os.getenv("CLI_USER_ID")
  execute = bool(int(os.getenv("CLI_EXECUTE_ZOHO", "0")))
  run_once(user_id=user_id_env, execute_zoho=execute)
