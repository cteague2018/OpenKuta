from __future__ import annotations

import io
import json
import pathlib
import uuid
import zipfile
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field

from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.core.compiler import TypstCompiler
from backend.app.export.qti_builder import QTIBuilder
from backend.app.generators import (
    GENERATOR_REGISTRY,
    KUTA_COURSE_CATALOG,
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


class GeneratePDFRequest(BaseModel):
    generator_id: str = Field(default="algebra_1.quadratics")
    title: str = Field(default="Quadratic Equations Worksheet")
    form_id: str = Field(default="A")
    problem_count: int = Field(default=8, ge=2, le=50)
    seed: Optional[int] = Field(default=None)
    difficulty_distribution: Optional[Dict[str, float]] = None
    allow_negatives: bool = Field(default=True)
    columns: int = Field(default=2, ge=1, le=3)
    show_answers: bool = Field(default=False)
    topics: Optional[List[Dict[str, Any]]] = None
    student_name: Optional[str] = None
    student_id: Optional[str] = None
    student_period: Optional[str] = None


class MultiFormRequest(BaseModel):
    generator_id: str = Field(default="algebra_1.quadratics")
    title: str = Field(default="Quadratic Equations Multi-Form Exam")
    base_seed: int = Field(default=42)
    problem_count: int = Field(default=8, ge=2, le=50)
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


@router.get("/catalog")
def get_catalog():
    """Return comprehensive 7-product Kuta course catalog with categories
    and topics.
    """
    return KUTA_COURSE_CATALOG


@router.get("/generators")
def list_generators():
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
def get_standards():
    """Return hierarchical CCSS-M and TEKS curriculum standards."""
    standards_path = (
        pathlib.Path(__file__).parent.parent / "export" / "standards.json"
    )
    if not standards_path.exists():
        raise HTTPException(status_code=404, detail="Standards file not found")
    return json.loads(standards_path.read_text(encoding="utf-8"))


@router.post("/worksheet/preview")
def preview_problems(req: GeneratePDFRequest):
    """Generate problem data for live frontend KaTeX preview."""
    gen = get_generator(req.generator_id)
    diff_dist = {
        ProblemDifficulty(k): v
        for k, v in (req.difficulty_distribution or {
            "mild": 0.4,
            "medium": 0.4,
            "spicy": 0.2,
        }).items()
    }
    cfg = GeneratorConfig(
        problem_count=req.problem_count,
        seed=req.seed,
        difficulty_distribution=diff_dist,
        allow_negatives=req.allow_negatives,
    )
    problems = gen.generate(cfg)
    return {
        "worksheet_id": f"WS-{uuid.uuid4().hex[:6].upper()}",
        "generator_id": req.generator_id,
        "seed": cfg.seed,
        "problems": [p.model_dump() for p in problems],
    }


@router.post("/worksheet/pdf")
def generate_pdf(req: GeneratePDFRequest):
    """Generate and stream a student printable PDF worksheet with corner
    ArUco markers and QR code.
    """
    active_seed = req.seed if req.seed is not None else 42
    problems = []

    if req.topics:
        item_seed = active_seed
        for t in req.topics:
            t_gen = get_generator(t.get("generator_id", req.generator_id))
            t_count = t.get("count", 4)
            t_diff = t.get("difficulty", "medium")
            diff_dist = {
                ProblemDifficulty.MILD: 1.0 if t_diff == "mild" else 0.0,
                ProblemDifficulty.MEDIUM: 1.0 if t_diff == "medium" else 0.0,
                ProblemDifficulty.SPICY: 1.0 if t_diff == "spicy" else 0.0,
            }
            cfg = GeneratorConfig(
                problem_count=t_count,
                seed=item_seed,
                difficulty_distribution=diff_dist,
                allow_negatives=req.allow_negatives,
            )
            probs = t_gen.generate(cfg)
            problems.extend(probs)
            item_seed += 113
    else:
        gen = get_generator(req.generator_id)
        diff_dist = {
            ProblemDifficulty(k): v
            for k, v in (req.difficulty_distribution or {
                "mild": 0.4,
                "medium": 0.4,
                "spicy": 0.2,
            }).items()
        }
        cfg = GeneratorConfig(
            problem_count=req.problem_count,
            seed=active_seed,
            difficulty_distribution=diff_dist,
            allow_negatives=req.allow_negatives,
        )
        problems = gen.generate(cfg)

    worksheet_id = f"WS-{active_seed % 10000:04d}"

    pdf_bytes = compiler.compile_worksheet_pdf(
        title=req.title,
        form_id=req.form_id,
        worksheet_id=worksheet_id,
        seed=active_seed,
        problems=problems,
        columns=req.columns,
        student_name=req.student_name,
        student_id=req.student_id,
        student_period=req.student_period,
    )

    disposition = f'inline; filename="{worksheet_id}_Form_{req.form_id}.pdf"'
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": disposition},
    )


@router.post("/worksheet/multi-form")
def generate_multi_form(req: MultiFormRequest):
    """Generate Forms A-D worksheets + companion Master Grading Matrix
    ZIP bundle.
    """
    worksheet_id = f"MF-{req.base_seed % 10000:04d}"

    forms_problems: Dict[str, List] = {}
    forms_pdfs: Dict[str, bytes] = {}

    for idx, form_id in enumerate(req.forms):
        form_seed = req.base_seed + (idx * 1337)
        probs = []

        if req.topics:
            item_seed = form_seed
            for t in req.topics:
                t_gen = get_generator(t.get("generator_id", req.generator_id))
                t_count = t.get("count", 4)
                t_diff = t.get("difficulty", "medium")
                diff_dist = {
                    ProblemDifficulty.MILD: 1.0 if t_diff == "mild" else 0.0,
                    ProblemDifficulty.MEDIUM: (
                        1.0 if t_diff == "medium" else 0.0
                    ),
                    ProblemDifficulty.SPICY: (
                        1.0 if t_diff == "spicy" else 0.0
                    ),
                }
                cfg = GeneratorConfig(
                    problem_count=t_count,
                    seed=item_seed,
                    difficulty_distribution=diff_dist,
                )
                probs.extend(t_gen.generate(cfg))
                item_seed += 113
        else:
            gen = get_generator(req.generator_id)
            cfg = GeneratorConfig(
                problem_count=req.problem_count,
                seed=form_seed,
            )
            probs = gen.generate(cfg)

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


@router.post("/grade/upload")
async def grade_upload(file: UploadFile = File(...)):
    """Receive student scan image, apply ArUco perspective deskewing,
    crop workspaces, decode student QR, and run verification.
    """
    image_bytes = await file.read()
    try:
        align_result = aligner.process(image_bytes)
    except Exception as e:
        msg = f"Image processing failed: {str(e)}"
        raise HTTPException(status_code=400, detail=msg)

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
            }
            for c in crops
        ],
    }


@router.post("/grade/verify-steps")
def verify_steps(req: StepVerifyRequest):
    """CAS verification of student step transitions with error diagnostic."""
    report = cas_verifier.verify_solution_steps(req.problem_id, req.steps)
    return report


@router.post("/export/qti")
def export_qti(req: QTIExportRequest):
    """Generate and download Canvas / Schoology QTI 2.1 quiz ZIP package."""
    problems = []
    if req.topics:
        item_seed = req.seed or 123
        for t in req.topics:
            t_gen = get_generator(t.get("generator_id", req.generator_id))
            t_count = t.get("count", 4)
            t_diff = t.get("difficulty", "medium")
            diff_dist = {
                ProblemDifficulty.MILD: 1.0 if t_diff == "mild" else 0.0,
                ProblemDifficulty.MEDIUM: 1.0 if t_diff == "medium" else 0.0,
                ProblemDifficulty.SPICY: 1.0 if t_diff == "spicy" else 0.0,
            }
            cfg = GeneratorConfig(
                problem_count=t_count,
                seed=item_seed,
                difficulty_distribution=diff_dist,
            )
            problems.extend(t_gen.generate(cfg))
            item_seed += 113
    else:
        gen = get_generator(req.generator_id)
        cfg = GeneratorConfig(problem_count=req.problem_count, seed=req.seed)
        problems = gen.generate(cfg)

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
