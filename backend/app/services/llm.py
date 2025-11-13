from __future__ import annotations

import logging
import time
from typing import Optional

import httpx

from ..config import settings
from .gmail_ingest import GmailMessage

logger = logging.getLogger(__name__)


class GeminiClient:
  def __init__(self):
    self.api_keys = settings.gemini_api_keys
    if not self.api_keys:
      raise RuntimeError("GEMINI_API_KEYS is not configured.")
    self.endpoint = str(settings.gemini_endpoint).rstrip("/")
    self.model = settings.gemini_model

  def _compose_url(self) -> str:
    if self.endpoint.endswith(self.model):
      return self.endpoint
    return f"{self.endpoint}/{self.model}:generateContent"

  def analyze_email(self, email: GmailMessage) -> str:
    prompt = self._build_prompt(email)
    return self._invoke(prompt, email.message_id, "analysis")

  def repair(self, email: GmailMessage, error_message: str) -> str:
    prompt = (
      "Your previous JSON response was invalid.\n"
      f"Reason: {error_message}\n"
      "Return only corrected JSON matching the required schema.\n"
      f"Email context:\n{email.consolidated_text}"
    )
    return self._invoke(prompt, email.message_id, "repair")

  def _invoke(self, prompt: str, message_id: str, purpose: str) -> str:
    url = self._compose_url()
    payload = {
      "contents": [{"role": "user", "parts": [{"text": prompt}]}],
      "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
    }

    for idx, api_key in enumerate(self.api_keys, start=1):
      start = time.perf_counter()
      try:
        with httpx.Client(timeout=30) as client:
          response = client.post(url, params={"key": api_key}, json=payload)
      except httpx.HTTPError as exc:
        logger.warning(
          "Gemini request failed",
          extra={"message_id": message_id, "purpose": purpose, "attempt": idx, "error": str(exc)},
        )
        continue

      latency = round((time.perf_counter() - start) * 1000, 2)
      if response.status_code == 200:
        data = response.json()
        try:
          return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
          logger.warning(
            "Gemini returned unexpected payload",
            extra={"message_id": message_id, "purpose": purpose, "error": str(exc)},
          )
          continue

      if response.status_code in {401, 403, 429, 500, 502, 503, 504}:
        logger.warning(
          "Gemini call failed, rotating key",
          extra={"message_id": message_id, "purpose": purpose, "status": response.status_code, "attempt": idx},
        )
        continue

      raise RuntimeError(f"Gemini error ({response.status_code}): {response.text}")

    raise RuntimeError("All Gemini API keys exhausted.")

  def _build_prompt(self, email: GmailMessage) -> str:
    metadata = [
      f"Subject: {email.subject or 'N/A'}",
      f"From: {email.sender or 'N/A'}",
      f"To: {', '.join(email.recipients) or 'N/A'}",
      f"Sent at: {email.sent_at.isoformat() if email.sent_at else 'N/A'}",
    ]
    instructions = """
Extract structured CRM data from the email body and attachments.
Return JSON with keys:
- people: array of { "name": string, "email": string }
- company: { "name": string, "domain": string }
- intent: string
- amount: string
- dates: array of strings
- next_steps: array of strings
- summary: string
- evidence: string (quote or reference)
If a field is unknown, use an empty string or empty array.
"""
    return "\n".join(filter(None, [*metadata, "", instructions, "", email.consolidated_text]))


gemini_client = GeminiClient()
