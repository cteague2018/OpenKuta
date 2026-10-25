from backend.app.core.base import GeneratorConfig
from backend.app.core.compiler import TypstCompiler
from backend.app.generators.algebra_1.quadratics import QuadraticEquationsGenerator
from backend.app.generators.algebra_1.two_step_equations import TwoStepEquationsGenerator


def test_worksheet_typst_compilation():
    gen = QuadraticEquationsGenerator()
    config = GeneratorConfig(problem_count=4, seed=123)
    problems = gen.generate(config)

    compiler = TypstCompiler()
    pdf_bytes = compiler.compile_worksheet_pdf(
        title="Quadratic Equations Test",
        form_id="A",
        worksheet_id="WS-TEST-001",
        seed=123,
        problems=problems,
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    # PDF magic bytes %PDF-
    assert pdf_bytes.startswith(b"%PDF-")


def test_matrix_key_typst_compilation():
    gen = TwoStepEquationsGenerator()
    forms_data = {
        "A": gen.generate(GeneratorConfig(problem_count=4, seed=1)),
        "B": gen.generate(GeneratorConfig(problem_count=4, seed=2)),
        "C": gen.generate(GeneratorConfig(problem_count=4, seed=3)),
        "D": gen.generate(GeneratorConfig(problem_count=4, seed=4)),
    }

    compiler = TypstCompiler()
    pdf_bytes = compiler.compile_matrix_key_pdf(
        title="Linear Equations Master Key",
        worksheet_id="WS-TEST-002",
        forms_data=forms_data,
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF-")

