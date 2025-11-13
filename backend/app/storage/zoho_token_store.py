from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime, timezone

TOKENS_FILE = Path(__file__).resolve().parents[2] / "zoho_tokens.json"


class ZohoTokenStore:
  def __init__(self, path: Path = TOKENS_FILE):
    self.path = path
    self.path.parent.mkdir(parents=True, exist_ok=True)

  def load(self, user_id: str) -> Optional[Dict[str, Any]]:
    data = self._read()
    return data.get(user_id)

  def save(self, user_id: str, payload: Dict[str, Any]) -> None:
    data = self._read()
    data[user_id] = payload
    self._write(data)

  def _read(self) -> Dict[str, Any]:
    if not self.path.exists():
      return {}
    with self.path.open("r", encoding="utf-8") as handle:
      return json.load(handle)

  def _write(self, data: Dict[str, Any]) -> None:
    with self.path.open("w", encoding="utf-8") as handle:
      json.dump(data, handle, indent=2)


zoho_token_store = ZohoTokenStore()
