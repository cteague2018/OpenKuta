import io
import json
import zipfile
import pytest

from backend.app.api.routes import (
    GeneratePDFRequest,
    MultiFormRequest,
    QTIExportRequest,
    StepVerifyRequest,
    export_qti,
    generate_multi_form,
    generate_pdf,
    get_standards,
    list_generators,
    preview_problems,
    verify_steps,
)
from backend.app.main import root, health


def test_health_and_root():
    assert health() == {"status": "ok"}
    r = root()
    assert r["engine"] == "OpenKuta"
    assert r["status"] == "online"


def test_list_generators():
    data = list_generators()
    assert len(data) >= 2
    ids = [g["id"] for g in data]
    assert "algebra_1.quadratics" in ids
    assert "algebra_1.two_step" in ids


def test_get_standards():
    data = get_standards()
    assert "curricula" in data
    assert "CCSS-M" in data["curricula"]


def test_worksheet_preview():
    req = GeneratePDFRequest(
        generator_id="algebra_1.quadratics",
        problem_count=4,
        seed=42,
    )
    res = preview_problems(req)
    assert len(res["problems"]) == 4
    assert res["seed"] == 42
    assert "worksheet_id" in res


def test_generate_pdf_endpoint():
    req = GeneratePDFRequest(
        generator_id="algebra_1.quadratics",
        problem_count=4,
        seed=42,
        form_id="A",
    )
    res = generate_pdf(req)
    assert res.status_code == 200
    assert res.media_type == "application/pdf"
    assert len(res.body) > 1000
    assert res.body.startswith(b"%PDF-")


def test_generate_multi_form_endpoint():
    req = MultiFormRequest(
        generator_id="algebra_1.two_step",
        problem_count=4,
        base_seed=100,
        forms=["A", "B", "C", "D"],
    )
    res = generate_multi_form(req)
    assert res.status_code == 200
    assert res.media_type == "application/zip"

    with zipfile.ZipFile(io.BytesIO(res.body)) as zf:
        names = zf.namelist()
        assert any("Master_Grading_Matrix" in n for n in names)
        assert any("Form_A" in n for n in names)
        assert any("Form_B" in n for n in names)


def test_step_verification_endpoint():
    req = StepVerifyRequest(
        problem_id="prob_test",
        steps=["2*x + 4 = 10", "2*x = 6", "x = 3"],
    )
    res = verify_steps(req)
    assert res.final_answer_correct is True
    assert res.partial_credit_score == 1.0
    assert res.first_failure_step is None


def test_export_qti_endpoint():
    req = QTIExportRequest(
        generator_id="algebra_1.quadratics",
        problem_count=3,
        seed=55,
    )
    res = export_qti(req)
    assert res.status_code == 200
    assert res.media_type == "application/zip"
    assert len(res.body) > 500


def test_classroom_api_endpoints():
    from backend.app.api.classroom_routes import (
        CreateClassRequest,
        BatchWorksheetRequest,
        RecordGradeRequest,
        create_class,
        list_classes,
        get_class,
        generate_class_batch_worksheet,
        get_gradebook,
        record_grade,
        export_gradebook_csv,
    )

    # List classes (seeded default)
    classes = list_classes()
    assert len(classes) >= 1
    default_id = classes[0]["id"]

    # Get class
    cls_data = get_class(default_id)
    assert cls_data.id == default_id

    # Create new class
    c_req = CreateClassRequest(name="Precalc Period 1", subject="Precalculus", period="1")
    new_c = create_class(c_req)
    assert new_c.name == "Precalc Period 1"

    # Batch class PDF
    batch_req = BatchWorksheetRequest(
        class_id=default_id,
        generator_id="algebra_1.two_step",
        title="Classroom Two Step Quiz",
        problem_count=4,
        seed=12,
    )
    pdf_res = generate_class_batch_worksheet(batch_req)
    assert pdf_res.status_code == 200
    assert len(pdf_res.body) > 1000

    # Record grade
    g_req = RecordGradeRequest(
        class_id=default_id,
        student_id="S10481",
        worksheet_id="WS-12",
        form_id="A",
        total_problems=4,
        correct_count=3,
        score_percentage=75.0,
        error_types=["sign_error"],
    )
    rec_res = record_grade(g_req)
    assert rec_res["status"] == "recorded"

    # Gradebook retrieval
    gb = get_gradebook(default_id)
    assert gb["total_graded"] >= 1
    stu_entry = next(e for e in gb["entries"] if e["student_id"] == "S10481")
    assert stu_entry["status"] == "graded"
    assert stu_entry["score_percentage"] == 75.0

    # Gradebook CSV export
    csv_res = export_gradebook_csv(default_id, format="canvas")
    assert csv_res.status_code == 200
    assert "SIS User ID" in csv_res.body.decode("utf-8")

