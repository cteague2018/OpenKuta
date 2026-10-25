from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException, Request, Response

from backend.app.api.routes import GeneratePDFRequest, generate_pdf
from backend.app.core.rate_limiter import TokenBucketRateLimiter

router = APIRouter(prefix="/api/v1", tags=["Multi-Tenant & Security"])

# Known registered tenants and their worksheets
TENANT_STORE: Dict[str, Dict[str, Any]] = {
    "teacher_a": {
        "teacher_name": "Teacher Alice",
        "worksheets": [
            {"id": "ws_alg1_unit2", "title": "Algebra 1 Unit 2 Quadratics", "problems_count": 12},
            {"id": "ws_alg1_midterm", "title": "Algebra 1 Midterm Exam", "problems_count": 25},
        ],
        "roster": [
            {"student_id": "stu_001", "name": "Charlie Adams"},
            {"student_id": "stu_002", "name": "Dana Brooks"},
        ],
    },
    "teacher_b": {
        "teacher_name": "Teacher Bob",
        "worksheets": [
            {"id": "ws_geo_unit4", "title": "Geometry Triangles & Similarity", "problems_count": 10},
        ],
        "roster": [
            {"student_id": "stu_101", "name": "Elena Clark"},
        ],
    },
}

heavy_endpoint_limiter = TokenBucketRateLimiter(capacity=10, refill_rate_per_sec=2.0)


def verify_tenant_authorization(
    target_teacher_id: str,
    x_teacher_id: Optional[str] = Header(None, alias="X-Teacher-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> str:
    """BOLA / IDOR defense: Verify the requesting user is authorized for target_teacher_id."""
    caller_id = x_teacher_id
    if not caller_id and authorization:
        # e.g., "Bearer teacher_a"
        token = authorization.replace("Bearer ", "").strip()
        caller_id = token

    if target_teacher_id not in TENANT_STORE:
        raise HTTPException(status_code=404, detail="Teacher account not found")

    if not caller_id:
        raise HTTPException(status_code=403, detail="Authentication required")

    if caller_id != target_teacher_id:
        raise HTTPException(
            status_code=403,
            detail=f"Forbidden: Tenant '{caller_id}' is not authorized to access '{target_teacher_id}' resources.",
        )

    return caller_id


@router.get("/worksheets/{teacher_id}")
def get_tenant_worksheets(
    teacher_id: str,
    x_teacher_id: Optional[str] = Header(None, alias="X-Teacher-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> Dict[str, Any]:
    """Retrieve saved worksheets for a specific teacher with BOLA / IDOR protection."""
    caller = verify_tenant_authorization(teacher_id, x_teacher_id, authorization)
    data = TENANT_STORE[caller]
    return {
        "teacher_id": caller,
        "teacher_name": data["teacher_name"],
        "worksheets": data["worksheets"],
    }


@router.get("/rosters/{teacher_id}")
def get_tenant_rosters(
    teacher_id: str,
    x_teacher_id: Optional[str] = Header(None, alias="X-Teacher-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> Dict[str, Any]:
    """Retrieve student roster for a specific teacher with BOLA / IDOR protection."""
    caller = verify_tenant_authorization(teacher_id, x_teacher_id, authorization)
    data = TENANT_STORE[caller]
    return {
        "teacher_id": caller,
        "roster": data["roster"],
    }


# Aliases for CPU-heavy endpoints with DoS rate limiting
@router.post("/generate-pdf")
def api_v1_generate_pdf(req: GeneratePDFRequest, request: Request) -> Response:
    client_ip = request.client.host if request.client else "local"
    if not heavy_endpoint_limiter.check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    return generate_pdf(req)


@router.post("/compile-typst")
def api_v1_compile_typst(req: GeneratePDFRequest, request: Request) -> Response:
    client_ip = request.client.host if request.client else "local"
    if not heavy_endpoint_limiter.check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    return generate_pdf(req)
