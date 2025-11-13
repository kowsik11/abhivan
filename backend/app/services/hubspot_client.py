from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException

from ..config import settings
from ..storage.hubspot_token_store import hubspot_token_store
from .planner import CrmUpsertPlan

logger = logging.getLogger(__name__)


class HubSpotOAuthManager:
  STATE_TTL_SECONDS = 600

  def sign_state(self, user_id: str) -> str:
    timestamp = str(int(time.time()))
    payload = f"{user_id}:{timestamp}"
    signature = hmac.new(
      settings.hubspot_client_secret.encode("utf-8"),
      payload.encode("utf-8"),
      hashlib.sha256,
    ).hexdigest()
    token = f"{payload}:{signature}"
    return base64.urlsafe_b64encode(token.encode("utf-8")).decode("utf-8")

  def verify_state(self, state: str) -> str:
    try:
      decoded = base64.urlsafe_b64decode(state.encode("utf-8")).decode("utf-8")
      user_id, timestamp, signature = decoded.split(":")
    except Exception as exc:
      raise HTTPException(status_code=400, detail="Invalid state parameter") from exc

    payload = f"{user_id}:{timestamp}"
    expected_sig = hmac.new(
      settings.hubspot_client_secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_sig):
      raise HTTPException(status_code=400, detail="Invalid state signature")

    if time.time() - int(timestamp) > self.STATE_TTL_SECONDS:
      raise HTTPException(status_code=400, detail="State expired")

    return user_id

  def exchange_code(self, user_id: str, code: str) -> Dict[str, Any]:
    token_url = f"{str(settings.hubspot_api_base).rstrip('/')}/oauth/v1/token"
    data = {
      "grant_type": "authorization_code",
      "client_id": settings.hubspot_client_id,
      "client_secret": settings.hubspot_client_secret,
      "redirect_uri": str(settings.hubspot_redirect_uri),
      "code": code,
    }

    with httpx.Client(timeout=30) as client:
      response = client.post(token_url, data=data)
    if response.status_code != 200:
      raise HTTPException(status_code=400, detail=f"HubSpot code exchange failed: {response.text}")

    payload = response.json()
    return self._persist_tokens(user_id, payload)

  def refresh_access_token(self, user_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
    token_url = f"{str(settings.hubspot_api_base).rstrip('/')}/oauth/v1/token"
    data = {
      "grant_type": "refresh_token",
      "client_id": settings.hubspot_client_id,
      "client_secret": settings.hubspot_client_secret,
      "refresh_token": record["refresh_token"],
    }
    with httpx.Client(timeout=30) as client:
      response = client.post(token_url, data=data)
    if response.status_code != 200:
      raise HTTPException(status_code=400, detail=f"HubSpot token refresh failed: {response.text}")

    payload = response.json()
    payload["refresh_token"] = record["refresh_token"]
    return self._persist_tokens(user_id, payload)

  def _persist_tokens(self, user_id: str, token_json: Dict[str, Any]) -> Dict[str, Any]:
    expires_in = int(token_json.get("expires_in", 3600))
    expires_at = (datetime.now(timezone.utc) + timedelta(seconds=expires_in - 60)).isoformat()
    stored = {
      "access_token": token_json["access_token"],
      "refresh_token": token_json.get("refresh_token"),
      "expires_at": expires_at,
      "user_email": token_json.get("user", {}).get("email"),
      "portal_id": token_json.get("hub_id"),
    }
    if not stored["refresh_token"]:
      raise HTTPException(status_code=400, detail="HubSpot did not return refresh_token")

    hubspot_token_store.save(user_id, stored)
    return stored

  def get_connection(self, user_id: str) -> Optional[Dict[str, Any]]:
    return hubspot_token_store.load(user_id)

  def get_valid_access_token(self, user_id: str) -> str:
    record = self.get_connection(user_id)
    if not record:
      raise HTTPException(status_code=400, detail="HubSpot is not connected")
    if datetime.fromisoformat(record["expires_at"]) <= datetime.now(timezone.utc):
      record = self.refresh_access_token(user_id, record)
    return record["access_token"]


oauth_manager = HubSpotOAuthManager()


class HubSpotClient:
  def __init__(self, oauth: HubSpotOAuthManager):
    self.oauth = oauth

  def execute_plan(self, user_id: str, plan: CrmUpsertPlan) -> Dict[str, Any]:
    access_token = self.oauth.get_valid_access_token(user_id)
    contact_id = None
    company_id = None

    if plan.contact:
      contact_id = self._upsert_contact(access_token, plan.contact)
    if plan.company:
      company_id = self._upsert_company(access_token, plan.company)
    if contact_id and company_id:
      self._associate_contact_company(access_token, contact_id, company_id)

    note_id = None
    if contact_id:
      note_id = self._create_note(access_token, contact_id, plan.note)

    return {"contact_id": contact_id, "company_id": company_id, "note_id": note_id}

  def _headers(self, token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

  def _upsert_contact(self, token: str, contact_plan) -> str:
    existing = None
    if contact_plan.email:
      existing = self._search_contact(token, contact_plan.email)

    payload = {
      "properties": {
        "firstname": contact_plan.full_name.split(" ")[0],
        "lastname": contact_plan.full_name.split(" ")[-1],
      }
    }
    if contact_plan.email:
      payload["properties"]["email"] = contact_plan.email

    if existing:
      contact_id = existing["id"]
      self._request(
        "patch",
        f"/crm/v3/objects/contacts/{contact_id}",
        token,
        json=payload,
      )
      return contact_id

    response = self._request("post", "/crm/v3/objects/contacts", token, json=payload)
    return response["id"]

  def _search_contact(self, token: str, email: str) -> Optional[Dict[str, Any]]:
    body = {
      "filterGroups": [{"filters": [{"value": email, "propertyName": "email", "operator": "EQ"}]}],
      "limit": 1,
    }
    response = self._request("post", "/crm/v3/objects/contacts/search", token, json=body, allow_404=True)
    results = (response or {}).get("results") if response else None
    return results[0] if results else None

  def _upsert_company(self, token: str, company_plan) -> str:
    existing = None
    if company_plan.domain:
      existing = self._search_company(token, "domain", company_plan.domain)
    if not existing:
      existing = self._search_company(token, "name", company_plan.name)

    payload = {"properties": {"name": company_plan.name}}
    if company_plan.domain:
      payload["properties"]["domain"] = company_plan.domain

    if existing:
      company_id = existing["id"]
      self._request("patch", f"/crm/v3/objects/companies/{company_id}", token, json=payload)
      return company_id

    response = self._request("post", "/crm/v3/objects/companies", token, json=payload)
    return response["id"]

  def _search_company(self, token: str, property_name: str, value: str) -> Optional[Dict[str, Any]]:
    body = {
      "filterGroups": [{"filters": [{"value": value, "propertyName": property_name, "operator": "EQ"}]}],
      "limit": 1,
    }
    response = self._request("post", "/crm/v3/objects/companies/search", token, json=body, allow_404=True)
    results = (response or {}).get("results") if response else None
    return results[0] if results else None

  def _associate_contact_company(self, token: str, contact_id: str, company_id: str) -> None:
    path = f"/crm/v3/objects/contacts/{contact_id}/associations/companies/{company_id}/contact_to_company"
    self._request("put", path, token)

  def _create_note(self, token: str, contact_id: str, note_plan) -> str:
    payload = {
      "properties": {
        "hs_note_title": note_plan.title,
        "hs_note_body": note_plan.body,
        "hs_timestamp": datetime.now(timezone.utc).isoformat(),
      }
    }
    response = self._request("post", "/crm/v3/objects/notes", token, json=payload)
    note_id = response["id"]
    assoc_path = f"/crm/v3/objects/notes/{note_id}/associations/contacts/{contact_id}/note_to_contact"
    self._request("put", assoc_path, token)
    return note_id

  def create_blog_post(self, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    token = self.oauth.get_valid_access_token(user_id)
    response = self._request("post", "/cms/v3/blogs/posts", token, json=payload)
    if response is None:
      raise HTTPException(status_code=502, detail="Empty response from HubSpot")
    return response

  def _request(
    self,
    method: str,
    path: str,
    token: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    allow_404: bool = False,
  ) -> Optional[Dict[str, Any]]:
    url = f"{str(settings.hubspot_api_base).rstrip('/')}{path}"
    try:
      with httpx.Client(timeout=20) as client:
        response = client.request(method.upper(), url, headers=self._headers(token), params=params, json=json)
    except httpx.HTTPError as exc:
      raise HTTPException(status_code=500, detail=f"HubSpot request failed: {exc}") from exc

    if allow_404 and response.status_code == 404:
      return None
    if response.status_code >= 400:
      raise HTTPException(status_code=response.status_code, detail=response.text)
    if response.content:
      return response.json()
    return None


hubspot_client = HubSpotClient(oauth_manager)
