from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import google_oauth, gmail, pipeline, hubspot, inbox

app = FastAPI(title="NextEdge Backend", version="1.0.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=[str(settings.frontend_url)],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(google_oauth.router)
app.include_router(gmail.router)
app.include_router(hubspot.router)
app.include_router(pipeline.router)
app.include_router(inbox.router)


@app.get("/healthz")
def healthcheck():
  return {"status": "ok"}
