import io
import json
import pathlib
import zipfile

from backend.app.core.base import GeneratorConfig
from backend.app.export.qti_builder import QTIBuilder
from backend.app.generators.algebra_1.quadratics import QuadraticEquationsGenerator


def test_qti_canvas_zip_generation():
    gen = QuadraticEquationsGenerator()
    problems = gen.generate(GeneratorConfig(problem_count=3, seed=888))

    builder = QTIBuilder()
    zip_bytes = builder.create_canvas_zip(
        quiz_title="Unit 4 Quadratics Quiz",
        problems=problems,
        quiz_id="quiz_quad_test",
    )

    assert isinstance(zip_bytes, bytes)
    assert len(zip_bytes) > 500

    # Inspect zip contents
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        namelist = zf.namelist()
        assert "imsmanifest.xml" in namelist
        assert "assessment_meta.xml" in namelist
        assert "assessment_qti.xml" in namelist

        manifest_content = zf.read("imsmanifest.xml").decode("utf-8")
        assert "imsqti_test_xmlv2p1" in manifest_content

        qti_content = zf.read("assessment_qti.xml").decode("utf-8")
        assert "choiceInteraction" in qti_content
        assert "modalFeedback" in qti_content


def test_standards_json_integrity():
    standards_path = pathlib.Path(__file__).parent.parent / "app" / "export" / "standards.json"
    assert standards_path.exists()

    data = json.loads(standards_path.read_text(encoding="utf-8"))
    assert "curricula" in data
    assert "CCSS-M" in data["curricula"]
    assert "TEKS" in data["curricula"]
