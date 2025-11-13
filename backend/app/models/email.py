from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class EmailAttachment(BaseModel):
  filename: str
  mime_type: str = Field(..., alias="mimeType")
  data: Optional[bytes] = None
  text_content: Optional[str] = None


class EmailMessage(BaseModel):
  id: str
  thread_id: Optional[str] = Field(None, alias="threadId")
  subject: Optional[str] = None
  sender: Optional[str] = None
  recipients: List[str] = Field(default_factory=list)
  sent_at: Optional[datetime] = None
  snippet: Optional[str] = None
  body_text: Optional[str] = None
  attachments: List[EmailAttachment] = Field(default_factory=list)


class AIExtraction(BaseModel):
  contact_name: str
  company: Optional[str] = None
  topic: str
  next_step: str
  value: Optional[str] = None


class HubSpotPayload(BaseModel):
  contact: dict
  company: Optional[dict] = None
  engagements: List[dict] = Field(default_factory=list)
