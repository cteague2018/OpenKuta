from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
from backend.app.api.classroom_routes import router as classroom_router


app = FastAPI(
    title="OpenKuta Math Assessment Engine",
    description="Deterministic math worksheet generator, Typst typesetting engine, and OpenCV/SymPy grading pipeline",
    version="0.1.0",
)

# Configure CORS for Next.js development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(classroom_router)


@app.get("/")
def root():
    return {
        "engine": "OpenKuta",
        "version": "0.1.0",
        "status": "online",
        "docs_url": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}

