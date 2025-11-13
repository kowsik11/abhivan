from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

TOKENS_PATH = Path(__file__).resolve().parents[2] / "tokens.json"


class TokenStore:
  def __init__(self, path: Path = TOKENS_PATH):
    self.path = path
    self.path.parent.mkdir(parents=True, exist_ok=True)

  def save(self, payload: Dict[str, Any]) -> None:
    with self.path.open("w", encoding="utf-8") as handle:
      json.dump(payload, handle, indent=2)

  def load(self) -> Optional[Dict[str, Any]]:
    if not self.path.exists():
      return None
    with self.path.open("r", encoding="utf-8") as handle:
      return json.load(handle)


token_store = TokenStore()
