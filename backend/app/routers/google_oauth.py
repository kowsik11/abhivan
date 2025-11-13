from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from urllib.parse import urljoin

from ..config import settings
from ..services.google_oauth_state import sign_state, verify_state
from ..storage.gmail_token_store import gmail_token_store
from ..storage.message_store import message_store
from ..storage.state_store import state_store
from pydantic import BaseModel

router = APIRouter(prefix="/api/google", tags=["google"])


@router.get("/connect")
async def connect_google(user_id: str):
  if not user_id:
    raise HTTPException(status_code=400, detail="Missing user_id")

  state = sign_state(user_id)
  params = {
    "client_id": settings.google_client_id,
    "redirect_uri": str(settings.google_redirect_uri),
    "response_type": "code",
    "scope": " ".join(settings.google_scopes),
    "access_type": "offline",
    "prompt": "consent",
    "state": state,
  }
  url = "https://accounts.google.com/o/oauth2/v2/auth"
  query = httpx.QueryParams(params)
  return RedirectResponse(url=f"{url}?{query}")


@router.get("/callback")
async def google_callback(request: Request):
  code = request.query_params.get("code")
  state = request.query_params.get("state")
  if not code or not state:
    raise HTTPException(status_code=400, detail="Missing authorization code or state")

  user_id = verify_state(state)

  token_url = "https://oauth2.googleapis.com/token"
  payload = {
    "code": code,
    "client_id": settings.google_client_id,
    "client_secret": settings.google_client_secret,
    "redirect_uri": str(settings.google_redirect_uri),
    "grant_type": "authorization_code",
  }

  async with httpx.AsyncClient(timeout=30) as client:
    response = await client.post(token_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})

  if response.status_code >= 400:
    raise HTTPException(status_code=500, detail=f"Failed to exchange code: {response.text}")

  tokens = response.json()
  refresh_token = tokens.get("refresh_token")
  existing = gmail_token_store.load(user_id) or {}
  if not refresh_token:
    refresh_token = existing.get("refresh_token")
  if not refresh_token:
    raise HTTPException(status_code=400, detail="Google did not return a refresh token")

  scope_value = tokens.get("scope")
  scopes = scope_value
  if isinstance(scope_value, str):
    scopes = [scope.strip() for scope in scope_value.split() if scope.strip()]

  expires_in = int(tokens.get("expires_in", 3600))
  expires_at = gmail_token_store.compute_expiry(expires_in)

  profile = await _fetch_gmail_profile(tokens["access_token"])
  record = {
    "google_user_id": profile.get("emailAddress"),
    "email": profile.get("emailAddress"),
    "history_id": profile.get("historyId"),
    "access_token": tokens["access_token"],
    "refresh_token": refresh_token,
    "expires_at": expires_at,
    "scope": scopes or [],
    "retrieved_at": datetime.utcnow().isoformat(),
    "token_type": tokens.get("token_type"),
  }
  gmail_token_store.save(user_id, record)
  baseline_at = datetime.now(timezone.utc).isoformat()
  state_store.set_baseline(user_id, baseline_at)
  message_store.reset_user(user_id)

  frontend_base = str(settings.frontend_url).rstrip("/")
  redirect_path = "home?connected=google"
  redirect_url = urljoin(f"{frontend_base}/", redirect_path)

  return RedirectResponse(url=redirect_url)


class DisconnectRequest(BaseModel):
  user_id: str


@router.post("/disconnect")
async def disconnect_google(payload: DisconnectRequest):
  user_id = payload.user_id
  if not user_id:
    raise HTTPException(status_code=400, detail="Missing user_id")

  gmail_token_store.delete(user_id)
  state_store.reset_user(user_id)
  message_store.reset_user(user_id)

  return {"disconnected": True}


async def _fetch_gmail_profile(access_token: str) -> Dict[str, Optional[str]]:
  profile_url = "https://gmail.googleapis.com/gmail/v1/users/me/profile"
  headers = {"Authorization": f"Bearer {access_token}"}
  async with httpx.AsyncClient(timeout=30) as client:
    response = await client.get(profile_url, headers=headers)
  if response.status_code >= 400:
    raise HTTPException(status_code=500, detail=f"Failed to fetch Gmail profile: {response.text}")
  return response.json()
