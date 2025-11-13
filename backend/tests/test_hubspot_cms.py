from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.routers import hubspot as hubspot_router

client = TestClient(app)


def test_cms_test_blog_post_invokes_hubspot(monkeypatch):
  captured = {}

  def fake_create_blog_post(user_id, payload):
    captured["user_id"] = user_id
    captured["payload"] = payload
    return {"id": "123", "name": payload["name"]}

  monkeypatch.setattr(hubspot_router.hubspot_client, "create_blog_post", fake_create_blog_post)

  response = client.post("/api/hubspot/cms/test-blog-post", json={"user_id": "user_123"})
  assert response.status_code == 200
  body = response.json()
  assert body["status"] == "success"
  assert body["hubspot_response"]["id"] == "123"
  assert captured["user_id"] == "user_123"
  assert captured["payload"] == hubspot_router.CMS_BLOG_POST_SAMPLE


def test_cms_test_blog_post_propagates_errors(monkeypatch):
  def fake_create_blog_post(user_id, payload):
    raise HTTPException(status_code=401, detail="Not connected")

  monkeypatch.setattr(hubspot_router.hubspot_client, "create_blog_post", fake_create_blog_post)

  response = client.post("/api/hubspot/cms/test-blog-post", json={"user_id": "user_456"})
  assert response.status_code == 401
  assert response.json()["detail"] == "Not connected"
