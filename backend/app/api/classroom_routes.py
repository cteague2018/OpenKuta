from __future__ import annotations

import csv
import io
import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, Response, UploadFile
from pydantic import BaseModel, Field

from backend.app.classroom.models import Classroom, Student, StudentSubmission
from backend.app.classroom.roster_parser import RosterParser
from backend.app.classroom.store import ClassroomStore
from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.core.compiler import TypstCompiler
from backend.app.generators import get_generator


router = APIRouter(prefix="/api/classroom")
store = ClassroomStore()
compiler = TypstCompiler()


class CreateClassRequest(BaseModel):
    name: str = Field(..., description="Algebra 1 - Period 3")
    subject: str = Field(default="Algebra 1")
    period: str = Field(default="3")
    teacher_name: str = Field(default="Teacher")


class BatchWorksheetRequest(BaseModel):
    class_id: str
    generator_id: str = Field(default="algebra_1.quadratics")
    title: str = Field(default="Unit 4 Practice")
    form_id: str = Field(default="A")
    problem_count: int = Field(default=6, ge=2, le=30)
    seed: int = Field(default=42)
    columns: int = Field(default=2, ge=1, le=3)
    difficulty_distribution: Optional[Dict[str, float]] = None


class RecordGradeRequest(BaseModel):
    class_id: str
    student_id: str
    worksheet_id: str
    form_id: str
    total_problems: int
    correct_count: int
    score_percentage: float
    error_types: List[str] = Field(default_factory=list)


@router.get("/classes")
def list_classes():
    """List all registered classrooms with student enrollment numbers."""
    classes = store.list_classes()
    return [
        {
            "id": c.id,
            "name": c.name,
            "subject": c.subject,
            "period": c.period,
            "teacher_name": c.teacher_name,
            "student_count": len(c.students),
            "created_at": c.created_at,
        }
        for c in classes
    ]


@router.post("/classes")
def create_class(req: CreateClassRequest):
    """Create a new classroom/period."""
    c = store.create_class(
        name=req.name,
        subject=req.subject,
        period=req.period,
        teacher_name=req.teacher_name,
    )
    return c


@router.get("/classes/{class_id}")
def get_class(class_id: str):
    """Get classroom details and full student roster."""
    c = store.get_class(class_id)
    if not c:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return c


@router.post("/import-roster")
async def import_roster(
    class_id: str = Form(...),
    file: UploadFile = File(...),
):
    """Upload CSV from Google Classroom, Canvas SIS, Clever, OneRoster, or generic CSV."""
    c = store.get_class(class_id)
    if not c:
        raise HTTPException(status_code=404, detail="Classroom not found")

    content = await file.read()
    students, detected_fmt = RosterParser.parse_csv(content, default_period=c.period)

    if not students:
        raise HTTPException(status_code=400, detail="No students could be parsed from CSV")

    updated_class = store.add_students_to_class(class_id, students)

    return {
        "status": "success",
        "detected_format": detected_fmt.value,
        "imported_count": len(students),
        "total_enrolled": len(updated_class.students),
        "students": [s.model_dump() for s in students],
    }


@router.post("/batch-worksheet")
def generate_class_batch_worksheet(req: BatchWorksheetRequest):
    """Generate a single bundled PDF for the entire class with pre-printed names and personalized QR codes."""
    c = store.get_class(req.class_id)
    if not c:
        raise HTTPException(status_code=404, detail="Classroom not found")
    if not c.students:
        raise HTTPException(status_code=400, detail="Classroom has no students in roster")

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
    )
    problems = gen.generate(cfg)
    worksheet_id = f"WS-{req.seed % 10000:04d}"

    students_data = [
        {
            "student_id": s.student_id,
            "name": s.full_name,
            "period": s.period or c.period,
        }
        for s in c.students
    ]

    pdf_bytes = compiler.compile_class_batch_pdf(
        title=req.title,
        form_id=req.form_id,
        worksheet_id=worksheet_id,
        seed=req.seed,
        problems=problems,
        students=students_data,
        class_id=req.class_id,
        columns=req.columns,
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{c.name.replace(" ", "_")}_Class_Set.pdf"'},
    )


@router.get("/gradebook/{class_id}")
def get_gradebook(class_id: str):
    """Return gradebook table showing students and their verified assessment submissions."""
    c = store.get_class(class_id)
    if not c:
        raise HTTPException(status_code=404, detail="Classroom not found")

    submissions = store.get_class_submissions(class_id)
    sub_by_student: Dict[str, StudentSubmission] = {}
    for s in submissions:
        sub_by_student[s.student_id] = s

    entries = []
    for stu in c.students:
        sub = sub_by_student.get(stu.student_id)
        entries.append({
            "student_id": stu.student_id,
            "name": stu.full_name,
            "email": stu.email,
            "status": "graded" if sub else "pending",
            "score_percentage": sub.score_percentage if sub else None,
            "correct_count": sub.correct_count if sub else None,
            "total_problems": sub.total_problems if sub else None,
            "error_types": sub.error_types if sub else [],
            "submitted_at": sub.submitted_at if sub else None,
            "worksheet_id": sub.worksheet_id if sub else None,
        })

    return {
        "class_id": class_id,
        "class_name": c.name,
        "total_enrolled": len(c.students),
        "total_graded": len(sub_by_student),
        "entries": entries,
    }


@router.post("/record-grade")
def record_grade(req: RecordGradeRequest):
    """Record or update verified student submission score."""
    student = store.find_student(req.class_id, req.student_id)
    student_name = student.full_name if student else f"Student {req.student_id}"

    sub = StudentSubmission(
        submission_id=f"sub_{uuid.uuid4().hex[:8]}",
        worksheet_id=req.worksheet_id,
        class_id=req.class_id,
        student_id=req.student_id,
        student_name=student_name,
        form_id=req.form_id,
        total_problems=req.total_problems,
        correct_count=req.correct_count,
        score_percentage=req.score_percentage,
        error_types=req.error_types,
        is_verified=True,
    )
    store.record_submission(sub)
    return {"status": "recorded", "submission": sub.model_dump()}


@router.get("/export-gradebook-csv/{class_id}")
def export_gradebook_csv(class_id: str, format: str = "canvas"):
    """Export gradebook to Canvas SIS or Google Classroom compatible CSV."""
    c = store.get_class(class_id)
    if not c:
        raise HTTPException(status_code=404, detail="Classroom not found")

    submissions = store.get_class_submissions(class_id)
    sub_map = {s.student_id: s for s in submissions}

    output = io.StringIO()
    writer = csv.writer(output)

    if format == "canvas":
        writer.writerow(["Student", "ID", "SIS User ID", "Section", "OpenKuta Assessment"])
        for stu in c.students:
            score = sub_map[stu.student_id].score_percentage if stu.student_id in sub_map else ""
            writer.writerow([f"{stu.last_name}, {stu.first_name}", stu.id, stu.student_id, stu.period or c.period, score])
    else:
        # Google Classroom / Standard
        writer.writerow(["Student ID", "First Name", "Last Name", "Email", "Score (%)", "Status"])
        for stu in c.students:
            sub = sub_map.get(stu.student_id)
            score = f"{sub.score_percentage:.1f}" if sub else ""
            status = "Graded" if sub else "Missing"
            writer.writerow([stu.student_id, stu.first_name, stu.last_name, stu.email or "", score, status])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{c.name.replace(" ", "_")}_Gradebook.csv"'},
    )
