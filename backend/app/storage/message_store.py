from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional

if TYPE_CHECKING:
  from ..services.gmail_ingest import GmailMessage

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "inbox_messages.json"
DEFAULT_BUCKET = {"last_checked_at": None, "messages": {}}
MAX_STORED_MESSAGES = 10


def _utcnow() -> str:
  return datetime.now(timezone.utc).isoformat()


class MessageStore:
  def __init__(self, path: Path = DEFAULT_PATH):
    self.path = path
    self.path.parent.mkdir(parents=True, exist_ok=True)

  def _read(self) -> Dict[str, Any]:
    if not self.path.exists():
      return {"users": {}}
    with self.path.open("r", encoding="utf-8") as handle:
      return json.load(handle)

  def _write(self, payload: Dict[str, Any]) -> None:
    with self.path.open("w", encoding="utf-8") as handle:
      json.dump(payload, handle, indent=2)

  def record_poll(self, user_id: str, messages: Iterable["GmailMessage"]) -> None:
    data = self._read()
    bucket = self._bucket_for_user(data, user_id, prune=True)
    existing: Dict[str, Any] = bucket.get("messages", {})
    for message in messages:
      if message.message_id in existing:
        continue
      existing[message.message_id] = self._serialize_message(message)
    bucket["messages"] = self._prune_messages(existing)
    bucket["last_checked_at"] = _utcnow()
    data["users"][user_id] = bucket
    self._write(data)

  def _serialize_message(self, message: "GmailMessage") -> Dict[str, Any]:
    has_attachments = any(message.attachments)
    has_images = any(att.mime_type.startswith("image/") for att in message.attachments)
    body_sample = (message.body_text or "").strip()
    has_links = "http://" in body_sample or "https://" in body_sample
    return {
      "id": message.message_id,
      "thread_id": message.thread_id,
      "subject": message.subject or "(no subject)",
      "sender": message.sender,
      "snippet": message.snippet,
      "preview": body_sample[:800],
      "received_at": message.sent_at.isoformat() if message.sent_at else None,
      "status": "new",
      "has_attachments": has_attachments,
      "has_images": has_images,
      "has_links": has_links,
      "gmail_url": self._gmail_url(message),
      "crm_record_url": None,
      "crm_note_id": None,
      "hubspot_note_id": None,
      "error": None,
      "created_at": _utcnow(),
      "updated_at": _utcnow(),
    }

  @staticmethod
  def _gmail_url(message: "GmailMessage") -> str:
    thread_or_id = message.thread_id or message.message_id
    return f"https://mail.google.com/mail/u/0/#inbox/{thread_or_id}"

  def update_status(
    self,
    user_id: str,
    message_id: str,
    *,
    status: str,
    crm_contact_id: Optional[str] = None,
    crm_note_id: Optional[str] = None,
    hubspot_portal_id: Optional[int] = None,
    error: Optional[str] = None,
  ) -> None:
    data = self._read()
    bucket = self._bucket_for_user(data, user_id, prune=True)
    entry = bucket.get("messages", {}).get(message_id)
    if not entry:
      return
    entry["status"] = status
    entry["updated_at"] = _utcnow()
    entry["error"] = error
    if crm_contact_id and hubspot_portal_id:
      entry["crm_record_url"] = f"https://app.hubspot.com/contacts/{hubspot_portal_id}/record/0-1/{crm_contact_id}"
    if crm_note_id:
      entry["hubspot_note_id"] = crm_note_id
    bucket["messages"][message_id] = entry
    data["users"][user_id] = bucket
    self._write(data)

  def list_messages(self, user_id: str, *, status: Optional[str] = None, query: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    data = self._read()
    bucket = self._bucket_for_user(data, user_id, prune=True)
    records = list(bucket.get("messages", {}).values())
    if status:
      records = [row for row in records if row.get("status") == status]
    if query:
      lowered = query.lower()
      records = [
        row
        for row in records
        if lowered in (row.get("subject") or "").lower()
        or lowered in (row.get("sender") or "").lower()
        or lowered in (row.get("preview") or "").lower()
      ]
    records.sort(key=lambda row: row.get("received_at") or row.get("created_at"), reverse=True)
    return records[:limit]

  def summary(self, user_id: str) -> Dict[str, Any]:
    data = self._read()
    bucket = self._bucket_for_user(data, user_id, prune=True)
    records = list(bucket.get("messages", {}).values())
    counts = {"new": 0, "processed": 0, "error": 0}
    for row in records:
      status = row.get("status", "new")
      if status in counts:
        counts[status] += 1
    return {
      "last_checked_at": bucket.get("last_checked_at"),
      "counts": counts,
      "total": len(records),
    }

  def mark_error(self, user_id: str, message_id: str, detail: str) -> None:
    self.update_status(user_id, message_id, status="error", error=detail)

  def get(self, user_id: str, message_id: str) -> Optional[Dict[str, Any]]:
    bucket = self._bucket_for_user(self._read(), user_id, prune=True)
    return bucket.get("messages", {}).get(message_id)

  def reset_user(self, user_id: str) -> None:
    data = self._read()
    users = data.setdefault("users", {})
    users[user_id] = dict(DEFAULT_BUCKET)
    self._write(data)

  def _bucket_for_user(self, data: Dict[str, Any], user_id: str, prune: bool = False) -> Dict[str, Any]:
    users = data.setdefault("users", {})
    if user_id not in users:
      users[user_id] = dict(DEFAULT_BUCKET)
    if prune:
      users[user_id]["messages"] = self._prune_messages(users[user_id].get("messages", {}))
    return users[user_id]

  def _prune_messages(self, messages: Dict[str, Any]) -> Dict[str, Any]:
    if not messages:
      return {}
    records = list(messages.values())
    records.sort(key=self._sort_key, reverse=True)
    trimmed = records[:MAX_STORED_MESSAGES]
    return {row["id"]: row for row in trimmed}

  @staticmethod
  def _sort_key(record: Dict[str, Any]) -> str:
    return record.get("received_at") or record.get("created_at") or ""


message_store = MessageStore()
