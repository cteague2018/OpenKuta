import pytest

from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.core.compiler import TypstCompiler
from backend.app.generators import GENERATOR_REGISTRY, get_generator
from backend.app.generators.calculus.lhopital import LhopitalGenerator
from backend.app.generators.geometry.coordinate_geometry import CoordinateGeometryGenerator
from backend.app.generators.precalculus.triangle_trig import TriangleTrigGenerator


def test_registry_registration():
    """Verify all 3 generators are registered in GENERATOR_REGISTRY and can be instantiated."""
    assert "geometry.coordinate_geometry" in GENERATOR_REGISTRY
    assert "precalculus.triangle_trig" in GENERATOR_REGISTRY
    assert "calculus.lhopital" in GENERATOR_REGISTRY

    g1 = get_generator("geometry.coordinate_geometry")
    assert isinstance(g1, CoordinateGeometryGenerator)
    assert g1.name == "Coordinate Geometry (Distance, Midpoint & Slope)"
    assert "CCSS.MATH.CONTENT.HSG.GPE.B.7" in g1.standards

    g2 = get_generator("precalculus.triangle_trig")
    assert isinstance(g2, TriangleTrigGenerator)
    assert g2.name == "Law of Sines and Law of Cosines"
    assert "CCSS.MATH.CONTENT.HSG.SRT.D.10" in g2.standards

    g3 = get_generator("calculus.lhopital")
    assert isinstance(g3, LhopitalGenerator)
    assert "L'Hôpital" in g3.name
    assert "AP.CALC.LIM.3" in g3.standards


@pytest.mark.parametrize("seed", [1, 42, 100, 2024, 9999])
@pytest.mark.parametrize("difficulty", [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY])
def test_coordinate_geometry_generation(seed: int, difficulty: ProblemDifficulty) -> None:
    gen = CoordinateGeometryGenerator()
    config = GeneratorConfig(
        problem_count=5,
        difficulty_distribution={difficulty: 1.0},
        seed=seed,
    )
    problems = gen.generate(config)
    assert len(problems) == 5

    for p in problems:
        assert p.prompt_text
        assert p.equation_typst.startswith("$") and p.equation_typst.endswith("$")
        assert p.answer_typst.startswith("$") and p.answer_typst.endswith("$")
        assert len(p.steps_typst) >= 3
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(set(p.distractors)) == len(p.distractors)

        if difficulty == ProblemDifficulty.MILD:
            # Midpoint or slope
            assert "midpoint" in p.prompt_text.lower() or "slope" in p.prompt_text.lower()
        elif difficulty == ProblemDifficulty.MEDIUM:
            # Exact distance formula with radical
            assert "distance" in p.prompt_text.lower()
            assert "d =" in p.answer_typst
        else:
            # Missing endpoint or large distance
            assert "endpoint" in p.prompt_text.lower() or "distance" in p.prompt_text.lower()


@pytest.mark.parametrize("seed", [2, 55, 303, 1729, 8888])
@pytest.mark.parametrize("difficulty", [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY])
def test_triangle_trig_generation(seed: int, difficulty: ProblemDifficulty) -> None:
    gen = TriangleTrigGenerator()
    config = GeneratorConfig(
        problem_count=5,
        difficulty_distribution={difficulty: 1.0},
        seed=seed,
    )
    problems = gen.generate(config)
    assert len(problems) == 5

    for p in problems:
        assert p.prompt_text
        assert p.equation_typst.startswith("$") and p.equation_typst.endswith("$")
        assert p.answer_typst.startswith("$") and p.answer_typst.endswith("$")
        assert len(p.steps_typst) >= 3
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(set(p.distractors)) == len(p.distractors)

        if difficulty == ProblemDifficulty.MILD:
            # Law of Sines AAS / ASA
            assert "law of sines" in p.prompt_text.lower()
            assert "b =" in p.answer_typst
        elif difficulty == ProblemDifficulty.MEDIUM:
            # Law of Cosines SAS
            assert "law of cosines" in p.prompt_text.lower()
            assert "c =" in p.answer_typst
        else:
            # SSS angle or SSA ambiguous case
            assert "law of cosines" in p.prompt_text.lower() or "triangles" in p.prompt_text.lower()


@pytest.mark.parametrize("seed", [3, 77, 404, 5555, 9876])
@pytest.mark.parametrize("difficulty", [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY])
def test_lhopital_generation(seed: int, difficulty: ProblemDifficulty) -> None:
    gen = LhopitalGenerator()
    config = GeneratorConfig(
        problem_count=5,
        difficulty_distribution={difficulty: 1.0},
        seed=seed,
    )
    problems = gen.generate(config)
    assert len(problems) == 5

    for p in problems:
        assert p.prompt_text
        assert p.equation_typst.startswith("$") and p.equation_typst.endswith("$")
        assert p.answer_typst.startswith("$") and p.answer_typst.endswith("$")
        assert len(p.steps_typst) >= 3
        assert len(p.distractors) >= 3
        assert p.answer_typst not in p.distractors
        assert len(set(p.distractors)) == len(p.distractors)

        # Check that steps explain indeterminate forms
        step_text = " ".join(p.steps_typst)
        assert "0/0" in step_text or "infinity" in step_text or "indeterminate" in step_text.lower()
        assert "l'hôpital" in step_text.lower() or "l'hopital" in step_text.lower()


def test_typst_pdf_compilation():
    """Verify that generated problems compile cleanly into PDFs via TypstCompiler."""
    compiler = TypstCompiler()

    for gen in [CoordinateGeometryGenerator(), TriangleTrigGenerator(), LhopitalGenerator()]:
        for diff in [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY]:
            problems = gen.generate(GeneratorConfig(problem_count=4, difficulty_distribution={diff: 1.0}, seed=42))
            pdf_bytes = compiler.compile_worksheet_pdf(
                title=f"{gen.name} - Test",
                form_id="A",
                worksheet_id="WS-TEST-PDF",
                seed=42,
                problems=problems,
            )
            assert isinstance(pdf_bytes, bytes)
            assert pdf_bytes.startswith(b"%PDF-")
