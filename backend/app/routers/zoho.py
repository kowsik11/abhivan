from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from httpx import QueryParams

from ..config import settings
from ..services.zoho_client import oauth_manager, ZohoTokenPayload

router = APIRouter(prefix="/api/zoho", tags=["zoho"])


@router.get("/connect")
def connect_zoho(user_id: str):
  if not user_id:
    raise HTTPException(status_code=400, detail="Missing user_id")

  state = oauth_manager.sign_state(user_id)
  params = QueryParams(
    {
      "scope": settings.zoho_scope,
      "client_id": settings.zoho_client_id,
      "response_type": "code",
      "access_type": "offline",
      "redirect_uri": str(settings.zoho_redirect_uri),
      "prompt": "consent",
      "state": state,
    }
  )

  url = f"{str(settings.zoho_accounts_url).rstrip('/')}/oauth/v2/auth?{params}"
  return RedirectResponse(url=url)


@router.get("/callback")
def zoho_callback(code: str, state: str):
  user_id = oauth_manager.verify_state(state)
  payload = oauth_manager.exchange_code(user_id, code)
  redirect_url = f"{str(settings.frontend_url).rstrip('/')}/home?connected=zoho"
  return RedirectResponse(url=redirect_url)


@router.get("/status")
def zoho_status(user_id: str):
  if not user_id:
    raise HTTPException(status_code=400, detail="Missing user_id")
  payload = oauth_manager.get_connection_info(user_id)
  if not payload:
    return {"connected": False}

  connected_payload: ZohoTokenPayload = payload
  return {"connected": True, "email": connected_payload.email}


def _encode(value: str) -> str:
  from urllib.parse import quote

  return quote(value, safe="")
