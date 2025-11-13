from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from httpx import QueryParams
from pydantic import BaseModel

from ..config import settings
from ..services.hubspot_client import hubspot_client, oauth_manager

router = APIRouter(prefix="/api/hubspot", tags=["hubspot"])
logger = logging.getLogger(__name__)

CMS_BLOG_POST_SAMPLE: Dict[str, Any] = {
  "name": "Codex Sample Blog Post",
  "contentGroupId": "184993428780",
  "slug": "codex-sample-post",
  "blogAuthorId": "4183274253",
  "metaDescription": "Synthetic payload used to exercise the CMS blog POST endpoints.",
  "useFeaturedImage": False,
  "postBody": "<p>This is a sample payload triggered from the Safe Point control panel.</p>",
}


class CmsBlogPostTestRequest(BaseModel):
  user_id: str


@router.get("/connect")
def connect_hubspot(user_id: str):
  if not user_id:
    raise HTTPException(status_code=400, detail="Missing user_id")
  state = oauth_manager.sign_state(user_id)
  params = QueryParams(
    {
      "client_id": settings.hubspot_client_id,
      "redirect_uri": str(settings.hubspot_redirect_uri),
      "scope": settings.hubspot_scope,
      "response_type": "code",
      "prompt": "consent",
      "access_type": "offline",
      "state": state,
    }
  )
  optional_scope = settings.hubspot_optional_scope.strip()
  if optional_scope:
    params = params.merge({"optional_scope": optional_scope})
  url = f"{str(settings.hubspot_auth_base).rstrip('/')}/authorize?{params}"
  return RedirectResponse(url=url)


@router.get("/callback")
def hubspot_callback(code: str, state: str):
  user_id = oauth_manager.verify_state(state)
  oauth_manager.exchange_code(user_id, code)
  return RedirectResponse(url=f"{str(settings.frontend_url).rstrip('/')}/home?connected=hubspot")


@router.get("/status")
def hubspot_status(user_id: str):
  if not user_id:
    raise HTTPException(status_code=400, detail="Missing user_id")
  record = oauth_manager.get_connection(user_id)
  if not record:
    return {"connected": False}
  return {"connected": True, "email": record.get("user_email")}


@router.post("/cms/test-blog-post")
def cms_test_blog_post(body: CmsBlogPostTestRequest):
  logger.info("CMS blog post test requested by %s", body.user_id)
  hubspot_response = hubspot_client.create_blog_post(body.user_id, CMS_BLOG_POST_SAMPLE)
  return {
    "status": "success",
    "hubspot_response": hubspot_response,
    "payload": CMS_BLOG_POST_SAMPLE,
  }
