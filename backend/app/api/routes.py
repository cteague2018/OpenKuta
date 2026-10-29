from __future__ import annotations

import base64
import io
import json
import pathlib
import uuid
import zipfile
from typing import Any, Dict, List, Optional

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field

from backend.app.core.base import BaseProblem, GeneratorConfig, ProblemDifficulty
from backend.app.core.compiler import TypstCompiler
from backend.app.core.rate_limiter import TokenBucketRateLimiter
from backend.app.export.qti_builder import QTIBuilder
from backend.app.generators import (
    COURSE_CATALOG,
    GENERATOR_REGISTRY,
    get_generator,
)
from backend.app.grading.aligner import WorksheetAligner
from backend.app.grading.extractor import ProblemWorkspaceExtractor
from backend.app.grading.verifier import CASStepVerifier

router = APIRouter(prefix="/api")
compiler = TypstCompiler()
aligner = WorksheetAligner()
extractor = ProblemWorkspaceExtractor()
cas_verifier = CASStepVerifier()
qti_builder = QTIBuilder()
pdf_limiter = TokenBucketRateLimiter(capacity=10, refill_rate_per_sec=2.0)
upload_limiter = TokenBucketRateLimiter(capacity=10, refill_rate_per_sec=2.0)


class GeneratePDFRequest(BaseModel):
    generator_id: str = Field(default="algebra_1.quadratics")
    title: str = Field(default="Quadratic Equations Worksheet")
    form_id: str = Field(default="A")
    problem_count: int = Field(default=8, ge=1, le=50)
    seed: Optional[int] = Field(default=None)
    difficulty_distribution: Optional[Dict[str, float]] = None
    allow_negatives: bool = Field(default=True)
    columns: int = Field(default=2, ge=1, le=3)
    show_answers: bool = Field(default=False)
    question_type: str = Field(default="free_response")
    topics: Optional[List[Dict[str, Any]]] = None
    student_name: Optional[str] = None
    student_id: Optional[str] = None
    student_period: Optional[str] = None


class MultiFormRequest(BaseModel):
    generator_id: str = Field(default="algebra_1.quadratics")
    title: str = Field(default="Quadratic Equations Multi-Form Exam")
    base_seed: int = Field(default=42)
    problem_count: int = Field(default=8, ge=1, le=50)
    forms: List[str] = Field(default_factory=lambda: ["A", "B", "C", "D"])
    topics: Optional[List[Dict[str, Any]]] = None


class QTIExportRequest(BaseModel):
    generator_id: str = Field(default="algebra_1.quadratics")
    title: str = Field(default="Canvas Quiz - Quadratics")
    problem_count: int = Field(default=10, ge=1, le=50)
    seed: Optional[int] = Field(default=123)
    topics: Optional[List[Dict[str, Any]]] = None


class StepVerifyRequest(BaseModel):
    problem_id: str
    steps: List[str]


def _generate_problems_for_request(
    generator_id: str,
    problem_count: int,
    seed: int,
    topics: Optional[List[Dict[str, Any]]] = None,
    difficulty_distribution: Optional[Dict[str, float]] = None,
    allow_negatives: bool = True,
    question_type: str = "free_response",
) -> List[BaseProblem]:
    """Shared helper to generate single-topic or multi-topic problem batches deterministically."""
    problems: List[BaseProblem] = []
    if topics:
        item_seed = seed
        for t in topics:
            t_gen_id = t.get("generator_id", generator_id)
            t_gen = get_generator(t_gen_id)
            t_count = t.get("count", 4)
            t_diff = t.get("difficulty", "medium")
            t_qtype = t.get("question_type", question_type)
            diff_dist = {
                ProblemDifficulty.MILD: 1.0 if t_diff == "mild" else 0.0,
                ProblemDifficulty.MEDIUM: 1.0 if t_diff == "medium" else 0.0,
                ProblemDifficulty.SPICY: 1.0 if t_diff == "spicy" else 0.0,
            }
            cfg = GeneratorConfig(
                problem_count=t_count,
                seed=item_seed,
                difficulty_distribution=diff_dist,
                allow_negatives=allow_negatives,
                question_type=t_qtype,
            )
            problems.extend(t_gen.generate(cfg))
            item_seed += 113
    else:
        gen = get_generator(generator_id)
        diff_dist = {
            ProblemDifficulty(k): v
            for k, v in (
                difficulty_distribution
                or {
                    "mild": 0.4,
                    "medium": 0.4,
                    "spicy": 0.2,
                }
            ).items()
        }
        cfg = GeneratorConfig(
            problem_count=problem_count,
            seed=seed,
            difficulty_distribution=diff_dist,
            allow_negatives=allow_negatives,
            question_type=question_type,
        )
        problems = gen.generate(cfg)
    return problems


@router.get("/health")
def api_health() -> dict[str, str]:
    """Health check endpoint for API route."""
    return {"status": "ok"}


@router.get("/catalog")
def get_catalog() -> Any:
    """Return comprehensive 7-tier curriculum course catalog with categories
    and topics.
    """
    return COURSE_CATALOG


@router.get("/generators")
def list_generators() -> List[Dict[str, Any]]:
    """List available procedural CAS math problem generators."""
    return [
        {
            "id": gen_cls.generator_id,
            "name": gen_cls.name,
            "category": gen_cls.category,
            "standards": gen_cls.standards,
        }
        for gen_cls in GENERATOR_REGISTRY.values()
    ]


@router.get("/standards")
def get_standards() -> Any:
    """Return hierarchical CCSS-M and TEKS curriculum standards."""
    standards_path = (
        pathlib.Path(__file__).parent.parent / "export" / "standards.json"
    )
    if not standards_path.exists():
        raise HTTPException(status_code=404, detail="Standards file not found")
    return json.loads(standards_path.read_text(encoding="utf-8"))


@router.post("/worksheet/preview")
def preview_problems(req: GeneratePDFRequest) -> Dict[str, Any]:
    """Generate problem data for live frontend KaTeX preview."""
    active_seed = req.seed if req.seed is not None else 42
    problems = _generate_problems_for_request(
        generator_id=req.generator_id,
        problem_count=req.problem_count,
        seed=active_seed,
        topics=req.topics,
        difficulty_distribution=req.difficulty_distribution,
        allow_negatives=req.allow_negatives,
        question_type=req.question_type,
    )
    return {
        "worksheet_id": f"WS-{uuid.uuid4().hex[:6].upper()}",
        "generator_id": req.generator_id,
        "seed": active_seed,
        "problems": [p.model_dump() for p in problems],
    }


def generate_pdf(req: GeneratePDFRequest) -> Response:
    """Generate and stream a student printable PDF worksheet with corner
    ArUco markers and QR code.
    """
    try:
        active_seed = req.seed if req.seed is not None else 42
        problems = _generate_problems_for_request(
            generator_id=req.generator_id,
            problem_count=req.problem_count,
            seed=active_seed,
            topics=req.topics,
            difficulty_distribution=req.difficulty_distribution,
            allow_negatives=req.allow_negatives,
            question_type=req.question_type,
        )

        worksheet_id = f"WS-{active_seed % 10000:04d}"

        pdf_bytes = compiler.compile_worksheet_pdf(
            title=req.title,
            form_id=req.form_id,
            worksheet_id=worksheet_id,
            seed=active_seed,
            problems=problems,
            columns=req.columns,
            show_answers=req.show_answers,
            student_name=req.student_name,
            student_id=req.student_id,
            student_period=req.student_period,
        )

        suffix = "_Answer_Key" if req.show_answers else ""
        disposition = f'inline; filename="{worksheet_id}_Form_{req.form_id}{suffix}.pdf"'
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": disposition},
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF compilation failed: {e}") from e


@router.post("/worksheet/pdf")
@router.post("/generate-pdf")
@router.post("/compile-typst")
def generate_pdf_endpoint(req: GeneratePDFRequest, request: Request) -> Response:
    forwarded = request.headers.get("x-forwarded-for", "")
    client_ip = (
        forwarded.split(",")[0].strip()
        if forwarded
        else (request.client.host if request.client else "local")
    )
    if not pdf_limiter.check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    return generate_pdf(req)


@router.post("/worksheet/multi-form")
def generate_multi_form(req: MultiFormRequest) -> Response:
    """Generate Forms A-D worksheets + companion Master Grading Matrix
    ZIP bundle.
    """
    worksheet_id = f"MF-{req.base_seed % 10000:04d}"

    forms_problems: Dict[str, List[BaseProblem]] = {}
    forms_pdfs: Dict[str, bytes] = {}

    for idx, form_id in enumerate(req.forms):
        form_seed = req.base_seed + (idx * 1337)
        probs = _generate_problems_for_request(
            generator_id=req.generator_id,
            problem_count=req.problem_count,
            seed=form_seed,
            topics=req.topics,
        )
        forms_problems[form_id] = probs

        pdf_bytes = compiler.compile_worksheet_pdf(
            title=f"{req.title} - Form {form_id}",
            form_id=form_id,
            worksheet_id=worksheet_id,
            seed=form_seed,
            problems=probs,
        )
        forms_pdfs[form_id] = pdf_bytes

    # Compile 4-column Master Grading Matrix
    matrix_pdf = compiler.compile_matrix_key_pdf(
        title=req.title,
        worksheet_id=worksheet_id,
        forms_data=forms_problems,
    )

    # Package everything into a downloadable ZIP archive
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{worksheet_id}_Master_Grading_Matrix.pdf", matrix_pdf)
        for form_id, pdf_data in forms_pdfs.items():
            fname = f"{worksheet_id}_Worksheet_Form_{form_id}.pdf"
            zf.writestr(fname, pdf_data)

    bundle_filename = f"{worksheet_id}_MultiForm_Bundle.zip"
    disposition = f'attachment; filename="{bundle_filename}"'
    return Response(
        content=zip_buf.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": disposition},
    )


def grade_upload(file: UploadFile) -> Dict[str, Any]:
    """Receive student scan image, apply ArUco perspective deskewing,
    crop workspaces, decode student QR, and run verification.
    """
    filename = file.filename or ""
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Directory traversal prohibited in filename")

    image_bytes = file.file.read()
    if len(image_bytes) < 16:
        raise HTTPException(status_code=400, detail="File too small or truncated byte stream")
    if len(image_bytes) > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds maximum threshold")

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Non-image file or invalid image format")

    h, w = img.shape[:2]
    if h > 5000 or w > 5000 or (h * w) > 25_000_000:
        raise HTTPException(status_code=400, detail="Image dimensions exceed safe limits (decompression bomb protection)")

    try:
        align_result = aligner.process(img)
    except Exception as e:
        msg = f"Image processing failed: {str(e)}"
        raise HTTPException(status_code=400, detail=msg) from e

    problem_count = align_result.metadata.get("problem_count", 6)
    crops = extractor.extract_workspaces(
        align_result.warped_image, problem_count=problem_count
    )

    # Check for student identification in QR metadata
    from backend.app.classroom.store import ClassroomStore
    class_store = ClassroomStore()
    student_info = None
    sid = align_result.metadata.get("student_id")
    cid = align_result.metadata.get("class_id")
    if cid and sid:
        stu = class_store.find_student(cid, sid)
        if stu:
            student_info = {
                "student_id": stu.student_id,
                "name": stu.full_name,
                "period": stu.period,
                "class_id": cid,
            }

    return {
        "is_aligned": align_result.is_aligned,
        "metadata": align_result.metadata,
        "student_info": student_info,
        "detected_markers": align_result.detected_marker_ids,
        "error_message": align_result.error_message,
        "problem_count": len(crops),
        "crops": [
            {
                "problem_index": c.problem_index,
                "bounding_box": c.bounding_box,
                "image_data": f"data:image/jpeg;base64,{base64.b64encode(cv2.imencode('.jpg', c.raw_crop, [cv2.IMWRITE_JPEG_QUALITY, 80])[1].tobytes()).decode('ascii')}" if c.raw_crop.size > 0 else None,
            }
            for c in crops
        ],
    }


@router.post("/grade/upload")
def grade_upload_route(request: Request, file: UploadFile = File(...)) -> Dict[str, Any]:
    client_ip = request.client.host if request.client else "local"
    if not upload_limiter.check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    return grade_upload(file)


@router.post("/grade/verify-steps")
def verify_steps(req: StepVerifyRequest) -> Any:
    """CAS verification of student step transitions with error diagnostic."""
    report = cas_verifier.verify_solution_steps(req.problem_id, req.steps)
    return report


@router.post("/export/qti")
def export_qti(req: QTIExportRequest) -> Response:
    """Generate and download Canvas / Schoology QTI 2.1 quiz ZIP package."""
    problems = _generate_problems_for_request(
        generator_id=req.generator_id,
        problem_count=req.problem_count,
        seed=req.seed or 123,
        topics=req.topics,
    )

    zip_bytes = qti_builder.create_canvas_zip(
        quiz_title=req.title,
        problems=problems,
    )

    disposition = 'attachment; filename="canvas_quiz_qti21.zip"'
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": disposition},
    )
