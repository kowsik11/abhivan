from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

STATE_FILE = Path(__file__).resolve().parents[2] / "state.json"
DEFAULT_STATE = {
  "last_uid": None,
  "processed_ids": [],
  "baseline_at": None,
  "baseline_ready": False,
}


class StateStore:
  def __init__(self, path: Path = STATE_FILE):
    self.path = path
    self.path.parent.mkdir(parents=True, exist_ok=True)

  def _read(self) -> Dict[str, Any]:
    if not self.path.exists():
      return {"users": {}}
    with self.path.open("r", encoding="utf-8") as handle:
      return json.load(handle)

  def _write(self, data: Dict[str, Any]) -> None:
    with self.path.open("w", encoding="utf-8") as handle:
      json.dump(data, handle, indent=2)

  def _bucket_for_user(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    users = data.setdefault("users", {})
    bucket = dict(DEFAULT_STATE)
    bucket.update(users.get(user_id, {}))
    users[user_id] = bucket
    return bucket

  def get_state(self, user_id: str) -> Dict[str, Any]:
    data = self._read()
    return dict(self._bucket_for_user(data, user_id))

  def update_state(self, user_id: str, *, last_uid: str | None, processed_ids: list[str]) -> None:
    data = self._read()
    bucket = self._bucket_for_user(data, user_id)
    bucket["last_uid"] = last_uid
    bucket["processed_ids"] = processed_ids
    self._write(data)

  def set_baseline(self, user_id: str, baseline_at: str) -> None:
    data = self._read()
    bucket = self._bucket_for_user(data, user_id)
    bucket["baseline_at"] = baseline_at
    bucket["baseline_ready"] = False
    bucket["last_uid"] = None
    bucket["processed_ids"] = []
    self._write(data)

  def mark_baseline_ready(self, user_id: str) -> None:
    data = self._read()
    bucket = self._bucket_for_user(data, user_id)
    bucket["baseline_ready"] = True
    self._write(data)

  def reset_user(self, user_id: str) -> None:
    data = self._read()
    users = data.setdefault("users", {})
    users[user_id] = dict(DEFAULT_STATE)
    self._write(data)


state_store = StateStore()
