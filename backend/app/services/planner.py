from __future__ import annotations

from pydantic import BaseModel

from .gmail_ingest import GmailMessage
from .validator import ValidatedExtraction


class ContactPlan(BaseModel):
  full_name: str
  email: str | None = None


class CompanyPlan(BaseModel):
  name: str
  domain: str | None = None


class NotePlan(BaseModel):
  title: str
  body: str
  external_ref: str


class CrmUpsertPlan(BaseModel):
  contact: ContactPlan | None = None
  company: CompanyPlan | None = None
  note: NotePlan


def build_crm_plan(email: GmailMessage, extraction: ValidatedExtraction) -> CrmUpsertPlan:
  contact_plan = None
  if extraction.people:
    primary = extraction.people[0]
    contact_plan = ContactPlan(full_name=primary.name, email=primary.email)

  company_plan = None
  if extraction.company:
    company_plan = CompanyPlan(name=extraction.company.name, domain=extraction.company.domain)

  note_lines = [
    f"Summary: {extraction.summary}",
    f"Intent: {extraction.intent or 'N/A'}",
    f"Amount: {extraction.amount or 'N/A'}",
    f"Dates: {', '.join(extraction.dates) if extraction.dates else 'N/A'}",
    f"Next Steps: {', '.join(extraction.next_steps) if extraction.next_steps else 'N/A'}",
    f"Evidence: {extraction.evidence or 'N/A'}",
    "",
    f"ExternalRef: {extraction.message_id}",
  ]

  note_plan = NotePlan(
    title=email.subject or "Email Note",
    body="\n".join(note_lines),
    external_ref=extraction.message_id,
  )

  return CrmUpsertPlan(contact=contact_plan, company=company_plan, note=note_plan)
