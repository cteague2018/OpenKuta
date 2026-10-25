from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.classroom_routes import router as classroom_router
from backend.app.api.multitenant_routes import router as multitenant_router
from backend.app.api.qr_routes import router as qr_router
from backend.app.api.routes import router

app = FastAPI(
    title="OpenMathForge Math Assessment Engine",
    description=(
        "Deterministic math worksheet generator, Typst typesetting engine, "
        "and OpenCV/SymPy grading pipeline"
    ),
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
app.include_router(qr_router)
app.include_router(multitenant_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "engine": "OpenMathForge",
        "version": "0.1.0",
        "status": "online",
        "docs_url": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
