from __future__ import annotations

import base64
import hashlib
import hmac
import time

from fastapi import HTTPException

from ..config import settings

STATE_TTL_SECONDS = 600


def sign_state(user_id: str) -> str:
  timestamp = str(int(time.time()))
  payload = f"{user_id}:{timestamp}"
  signature = hmac.new(
    settings.google_client_secret.encode("utf-8"),
    payload.encode("utf-8"),
    hashlib.sha256,
  ).hexdigest()
  token = f"{payload}:{signature}"
  return base64.urlsafe_b64encode(token.encode("utf-8")).decode("utf-8")


def verify_state(state: str) -> str:
  try:
    decoded = base64.urlsafe_b64decode(state.encode("utf-8")).decode("utf-8")
    user_id, timestamp, signature = decoded.split(":")
  except Exception as exc:
    raise HTTPException(status_code=400, detail="Invalid state parameter") from exc

  payload = f"{user_id}:{timestamp}"
  expected_sig = hmac.new(
    settings.google_client_secret.encode("utf-8"),
    payload.encode("utf-8"),
    hashlib.sha256,
  ).hexdigest()
  if not hmac.compare_digest(signature, expected_sig):
    raise HTTPException(status_code=400, detail="Invalid state signature")

  if time.time() - int(timestamp) > STATE_TTL_SECONDS:
    raise HTTPException(status_code=400, detail="State parameter expired")

  return user_id
