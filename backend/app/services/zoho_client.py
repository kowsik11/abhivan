from __future__ import annotations

import base64
import hmac
import hashlib
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import logging

import httpx
from fastapi import HTTPException
from pydantic import BaseModel

from ..config import settings
from ..storage.zoho_token_store import zoho_token_store

logger = logging.getLogger(__name__)


class ZohoTokenPayload(BaseModel):
  access_token: str
  refresh_token: str
  expires_at: str
  api_domain: str
  email: Optional[str] = None


class CrmWriteResult(BaseModel):
  contact_id: Optional[str] = None
  account_id: Optional[str] = None
  note_id: Optional[str] = None
  contact_created: bool = False
  account_created: bool = False
  note_created: bool = False


class ZohoOAuthManager:
  STATE_TTL_SECONDS = 600

  def sign_state(self, user_id: str) -> str:
    timestamp = int(time.time())
    payload = f"{user_id}:{timestamp}"
    signature = hmac.new(
      settings.zoho_client_secret.encode("utf-8"),
      payload.encode("utf-8"),
      hashlib.sha256,
    ).hexdigest()
    token = f"{payload}:{signature}"
    return base64.urlsafe_b64encode(token.encode("utf-8")).decode("utf-8")

  def verify_state(self, state: str) -> str:
    try:
      decoded = base64.urlsafe_b64decode(state.encode("utf-8")).decode("utf-8")
      user_id, timestamp_str, signature = decoded.split(":")
    except Exception as exc:  # pragma: no cover - defensive
      raise HTTPException(status_code=400, detail="Invalid state parameter") from exc

    payload = f"{user_id}:{timestamp_str}"
    expected_sig = hmac.new(
      settings.zoho_client_secret.encode("utf-8"),
      payload.encode("utf-8"),
      hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, signature):
      raise HTTPException(status_code=400, detail="Invalid state signature")

    timestamp = int(timestamp_str)
    if time.time() - timestamp > self.STATE_TTL_SECONDS:
      raise HTTPException(status_code=400, detail="State parameter expired")

    return user_id

  def exchange_code(self, user_id: str, code: str) -> ZohoTokenPayload:
    accounts_base = str(settings.zoho_accounts_url).rstrip("/")
    token_url = f"{accounts_base}/oauth/v2/token"
    data = {
      "grant_type": "authorization_code",
      "client_id": settings.zoho_client_id,
      "client_secret": settings.zoho_client_secret,
      "redirect_uri": str(settings.zoho_redirect_uri),
      "code": code,
    }

    with httpx.Client(timeout=20) as client:
      response = client.post(token_url, data=data)
    if response.status_code != 200:
      raise HTTPException(status_code=400, detail=f"Failed to exchange Zoho code: {response.text}")

    token_json = response.json()
    payload = self._build_token_payload(token_json, existing=zoho_token_store.load(user_id))

    email = self._fetch_user_email(payload.access_token)
    payload.email = email

    zoho_token_store.save(user_id, payload.model_dump())
    return payload

  def _fetch_user_email(self, access_token: str) -> Optional[str]:
    info_url = f"{str(settings.zoho_accounts_url).rstrip('/')}/oauth/user/info"
    try:
      with httpx.Client(timeout=20) as client:
        response = client.get(info_url, headers={"Authorization": f"Zoho-oauthtoken {access_token}"})
      if response.status_code == 200:
        data = response.json()
        return data.get("Email")
    except httpx.HTTPError:
      pass
    return None

  def _build_token_payload(self, token_json: Dict[str, Any], existing: Optional[Dict[str, Any]]) -> ZohoTokenPayload:
    refresh_token = token_json.get("refresh_token") or (existing or {}).get("refresh_token")
    if not refresh_token:
      raise HTTPException(status_code=400, detail="Zoho did not return a refresh token")

    expires_in = int(token_json.get("expires_in", 3600))
    expires_at = (datetime.now(timezone.utc) + timedelta(seconds=expires_in - 60)).isoformat()

    api_domain = token_json.get("api_domain") or (existing or {}).get("api_domain") or str(settings.zoho_api_url)

    return ZohoTokenPayload(
      access_token=token_json["access_token"],
      refresh_token=refresh_token,
      expires_at=expires_at,
      api_domain=api_domain,
      email=(existing or {}).get("email"),
    )

  def get_valid_access_token(self, user_id: str) -> str:
    record = zoho_token_store.load(user_id)
    if not record:
      raise HTTPException(status_code=400, detail="Zoho is not connected")

    payload = ZohoTokenPayload.model_validate(record)
    expires_at = datetime.fromisoformat(payload.expires_at)
    if expires_at <= datetime.now(timezone.utc) + timedelta(seconds=60):
      payload = self.refresh_token(user_id, payload)

    return payload.access_token

  def refresh_token(self, user_id: str, payload: ZohoTokenPayload) -> ZohoTokenPayload:
    token_url = f"{settings.zoho_accounts_url.rstrip('/')}/oauth/v2/token"
    data = {
      "grant_type": "refresh_token",
      "refresh_token": payload.refresh_token,
      "client_id": settings.zoho_client_id,
      "client_secret": settings.zoho_client_secret,
    }

    with httpx.Client(timeout=20) as client:
      response = client.post(token_url, data=data)
    if response.status_code != 200:
      raise HTTPException(status_code=400, detail=f"Failed to refresh Zoho token: {response.text}")

    token_json = response.json()
    new_payload = self._build_token_payload(token_json, existing=payload.model_dump())
    zoho_token_store.save(user_id, new_payload.model_dump())
    return new_payload

  def get_connection_info(self, user_id: str) -> Optional[ZohoTokenPayload]:
    record = zoho_token_store.load(user_id)
    if not record:
      return None
    return ZohoTokenPayload.model_validate(record)


oauth_manager = ZohoOAuthManager()


class ZohoCRMClient:
  def __init__(self, oauth: ZohoOAuthManager):
    self.oauth = oauth

  def execute_plan(self, user_id: str, plan, message_id: str) -> CrmWriteResult:
    result = CrmWriteResult()
    contact_id = None
    account_id = None

    if plan.contact:
      contact_id, created = self._upsert_contact(user_id, plan.contact, plan.company)
      result.contact_id = contact_id
      result.contact_created = created

    if plan.company:
      account_id, account_created = self._upsert_account(user_id, plan.company)
      result.account_id = account_id
      result.account_created = account_created

    if plan.contact and account_id and contact_id:
      self._associate_contact_with_account(user_id, contact_id, account_id)

    parent_id = contact_id or account_id
    se_module = "Contacts" if contact_id else "Accounts"
    if parent_id:
      note_id, note_created = self._create_note_if_absent(user_id, parent_id, se_module, plan.note, message_id)
      result.note_id = note_id
      result.note_created = note_created

    return result

  def _upsert_contact(self, user_id: str, contact_plan, company_plan) -> tuple[str, bool]:
    existing = None
    if contact_plan.email:
      existing = self._search_contact_by_email(user_id, contact_plan.email)

    payload = self._build_contact_payload(contact_plan, company_plan, existing)
    if existing:
      contact_id = existing["id"]
      self._request(user_id, "PUT", f"/crm/v3/Contacts/{contact_id}", json={"data": [payload]})
      return contact_id, False

    response = self._request(user_id, "POST", "/crm/v3/Contacts", json={"data": [payload]})
    contact_id = response["data"][0]["details"]["id"]
    return contact_id, True

  def _build_contact_payload(self, contact_plan, company_plan, existing):
    payload = {}
    name = contact_plan.full_name.strip() if contact_plan.full_name else "Unknown"
    parts = name.split()
    if len(parts) == 1:
      payload["Last_Name"] = parts[0]
    else:
      payload["First_Name"] = " ".join(parts[:-1])
      payload["Last_Name"] = parts[-1]

    if contact_plan.email:
      payload["Email"] = contact_plan.email

    if company_plan and "Account_Name" not in payload and existing and existing.get("Account_Name"):
      payload["Account_Name"] = existing["Account_Name"]

    if company_plan and not existing:
      payload["Account_Name"] = {"name": company_plan.name}

    return payload

  def _upsert_account(self, user_id: str, company_plan) -> tuple[str, bool]:
    existing = self._search_account(user_id, company_plan)
    payload = {
      "Account_Name": company_plan.name,
    }
    if company_plan.domain:
      payload["Website"] = company_plan.domain

    if existing:
      account_id = existing["id"]
      self._request(user_id, "PUT", f"/crm/v3/Accounts/{account_id}", json={"data": [payload]})
      return account_id, False

    response = self._request(user_id, "POST", "/crm/v3/Accounts", json={"data": [payload]})
    account_id = response["data"][0]["details"]["id"]
    return account_id, True

  def _associate_contact_with_account(self, user_id: str, contact_id: str, account_id: str) -> None:
    payload = {"data": [{"Account_Name": {"id": account_id}}]}
    self._request(user_id, "PUT", f"/crm/v3/Contacts/{contact_id}", json=payload)

  def _create_note_if_absent(self, user_id: str, parent_id: str, se_module: str, note_plan, message_id: str) -> tuple[Optional[str], bool]:
    criteria = f"(Note_Content:contains:ExternalRef: {message_id})"
    params = {"criteria": criteria}
    search = self._request(user_id, "GET", "/crm/v3/Notes/search", params=params, allow_404=True)
    if search and search.get("data"):
      # Check if note is for same parent
      for note in search["data"]:
        parent = note.get("Parent_Id", {})
        if parent.get("id") == parent_id:
          return note.get("id"), False

    payload = {
      "data": [
        {
          "Note_Title": note_plan.title,
          "Note_Content": note_plan.body,
          "Parent_Id": parent_id,
          "se_module": se_module,
        }
      ]
    }
    response = self._request(user_id, "POST", "/crm/v3/Notes", json=payload)
    note_id = response["data"][0]["details"]["id"]
    return note_id, True

  def _search_contact_by_email(self, user_id: str, email: str) -> Optional[Dict[str, Any]]:
    response = self._request(user_id, "GET", "/crm/v3/Contacts/search", params={"email": email}, allow_404=True)
    data = (response or {}).get("data") if response else None
    if data:
      return data[0]
    return None

  def _search_account(self, user_id: str, company_plan) -> Optional[Dict[str, Any]]:
    if company_plan.domain:
      criteria = f"(Website:equals:{company_plan.domain})"
      response = self._request(user_id, "GET", "/crm/v3/Accounts/search", params={"criteria": criteria}, allow_404=True)
      data = (response or {}).get("data") if response else None
      if data:
        return data[0]

    criteria = f"(Account_Name:equals:{company_plan.name})"
    response = self._request(user_id, "GET", "/crm/v3/Accounts/search", params={"criteria": criteria}, allow_404=True)
    data = (response or {}).get("data") if response else None
    if data:
      return data[0]
    return None

  def _request(
    self,
    user_id: str,
    method: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    allow_404: bool = False,
  ) -> Optional[Dict[str, Any]]:
    tokens = oauth_manager.get_connection_info(user_id)
    if not tokens:
      raise HTTPException(status_code=400, detail="Zoho is not connected")

    api_base = tokens.api_domain.rstrip("/") if tokens.api_domain else str(settings.zoho_api_url).rstrip("/")
    url = f"{api_base}{path}"
    access_token = oauth_manager.get_valid_access_token(user_id)

    for attempt in range(2):
      try:
        with httpx.Client(timeout=20) as client:
          response = client.request(
            method,
            url,
            params=params,
            json=json,
            headers={"Authorization": f"Zoho-oauthtoken {access_token}"},
          )
      except httpx.HTTPError as exc:  # pragma: no cover - network
        logger.warning("Zoho request failed", extra={"path": path, "attempt": attempt + 1, "error": str(exc)})
        time.sleep(1)
        continue

      if response.status_code == 401 and attempt == 0:
        oauth_manager.refresh_token(user_id, tokens)
        tokens = oauth_manager.get_connection_info(user_id)
        access_token = oauth_manager.get_valid_access_token(user_id)
        continue

      if allow_404 and response.status_code == 404:
        return None

      if response.status_code >= 500 and attempt == 0:
        time.sleep(1)
        continue

      if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

      if response.content:
        return response.json()
      return None

    raise HTTPException(status_code=500, detail="Zoho request failed after retries")


crm_client = ZohoCRMClient(oauth_manager)
