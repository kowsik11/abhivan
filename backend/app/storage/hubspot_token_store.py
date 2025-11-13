from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

TOKENS_PATH = Path(__file__).resolve().parents[2] / "hubspot_tokens.json"


class HubSpotTokenStore:
  def __init__(self, path: Path = TOKENS_PATH):
    self.path = path
    self.path.parent.mkdir(parents=True, exist_ok=True)

  def _read(self) -> Dict[str, Any]:
    if not self.path.exists():
      return {}
    with self.path.open("r", encoding="utf-8") as handle:
      return json.load(handle)

  def _write(self, data: Dict[str, Any]) -> None:
    with self.path.open("w", encoding="utf-8") as handle:
      json.dump(data, handle, indent=2)

  def load(self, user_id: str) -> Optional[Dict[str, Any]]:
    return self._read().get(user_id)

  def save(self, user_id: str, payload: Dict[str, Any]) -> None:
    data = self._read()
    data[user_id] = payload
    self._write(data)


hubspot_token_store = HubSpotTokenStore()
