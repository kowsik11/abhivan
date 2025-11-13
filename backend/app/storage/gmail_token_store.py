from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

TOKENS_PATH = Path(__file__).resolve().parents[2] / "gmail_tokens.json"


class GmailTokenStore:
  def __init__(self, path: Path = TOKENS_PATH):
    self.path = path
    self.path.parent.mkdir(parents=True, exist_ok=True)

  def _read(self) -> Dict[str, Any]:
    if not self.path.exists():
      return {}
    with self.path.open("r", encoding="utf-8") as handle:
      return json.load(handle)

  def _write(self, payload: Dict[str, Any]) -> None:
    with self.path.open("w", encoding="utf-8") as handle:
      json.dump(payload, handle, indent=2)

  def save(self, user_id: str, record: Dict[str, Any]) -> None:
    data = self._read()
    data[user_id] = record
    self._write(data)

  def load(self, user_id: str) -> Optional[Dict[str, Any]]:
    return self._read().get(user_id)

  def all(self) -> Dict[str, Any]:
    return self._read()

  def delete(self, user_id: str) -> None:
    data = self._read()
    if user_id in data:
      data.pop(user_id)
      self._write(data)

  @staticmethod
  def compute_expiry(expires_in: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=expires_in - 60)).isoformat()


gmail_token_store = GmailTokenStore()
