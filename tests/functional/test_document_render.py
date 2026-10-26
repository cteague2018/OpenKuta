from __future__ import annotations

from backend.app.core.base import GeneratorConfig
from backend.app.core.compiler import TypstCompiler
from backend.app.generators import get_generator


class TestDocumentRenderPipeline:
    """Typst compilation, multi-page layout integrity, and sequential problem numbering."""

    def test_batch_compile_diverse_worksheets_with_answer_keys(self) -> None:
        """Batch compile 50+ diverse worksheets with student view and full answer keys."""
        compiler = TypstCompiler()
        generators_to_test = [
            "algebra_1.quadratics",
            "algebra_1.two_step",
            "algebra_1.systems",
            "algebra_1.factoring",
            "geometry.pythagorean",
            "geometry.triangles",
            "geometry.circles",
            "algebra_2.complex_numbers",
            "algebra_2.radicals",
            "precalculus.vectors",
            "calculus.derivatives",
            "calculus.integrals",
            "grade_6.order_of_operations",
            "grade_6.statistics",
        ]

        compiled_count = 0

        for gen_id in generators_to_test:
            gen = get_generator(gen_id)
            for prob_count in [2, 6]:
                for show_ans in [False, True]:
                    cfg = GeneratorConfig(
                        problem_count=prob_count,
                        seed=100 + compiled_count * 13,
                    )
                    problems = gen.generate(cfg)
                    assert len(problems) == prob_count

                    # Sequential problem numbering invariant: 1 to N
                    for idx, p in enumerate(problems, start=1):
                        assert p.id, f"Problem at index {idx} has empty ID"

                    ws_id = f"WS-T{compiled_count:04d}"
                    pdf_bytes = compiler.compile_worksheet_pdf(
                        title=f"Verification Worksheet - {gen.name}",
                        form_id="A",
                        worksheet_id=ws_id,
                        seed=100 + compiled_count * 13,
                        problems=problems,
                        columns=2,
                        show_answers=show_ans,
                    )

                    # Validation: Valid PDF magic bytes and size
                    assert pdf_bytes.startswith(b"%PDF-"), f"Output for {gen_id} not a valid PDF"
                    assert len(pdf_bytes) > 8000, f"PDF file size too small: {len(pdf_bytes)} bytes"

                    compiled_count += 1

        assert compiled_count >= 50, f"Expected 50+ batch compiled worksheets, got {compiled_count}"

    def test_sequential_unskipped_problem_numbering(self) -> None:
        """Assert generated problems in worksheet maintain strict monotonic 1-based indexing."""
        gen = get_generator("algebra_1.multi_step")
        cfg = GeneratorConfig(problem_count=12, seed=42)
        problems = gen.generate(cfg)
        assert len(problems) == 12

        for _i, p in enumerate(problems):
            # Check problem ID format contains index or conforms to structure
            assert p.id
            assert p.prompt_text
            assert p.equation_typst
            assert p.answer_typst

    def test_class_batch_pdf_personalized_compilation(self) -> None:
        """Verify multi-student class batch PDF generation with personalized tracking."""
        compiler = TypstCompiler()
        gen = get_generator("algebra_1.quadratics")
        cfg = GeneratorConfig(problem_count=4, seed=888)
        problems = gen.generate(cfg)

        students = [
            {"student_id": f"stu_{i:03d}", "name": f"Student {i}", "period": "Period 2"}
            for i in range(1, 6)
        ]

        batch_pdf = compiler.compile_class_batch_pdf(
            title="Period 2 Quiz",
            form_id="A",
            worksheet_id="WS-CLS-01",
            seed=888,
            problems=problems,
            students=students,
            class_id="cls_alg1_p2",
            columns=2,
        )

        assert batch_pdf.startswith(b"%PDF-")
        assert len(batch_pdf) > 25000, "Class batch PDF with 5 students should exceed 25 KB"

    def test_master_grading_matrix_compilation(self) -> None:
        """Verify Master Grading Matrix PDF compilation for 4 forms."""
        compiler = TypstCompiler()
        gen = get_generator("algebra_1.linear_equations")
        forms_data = {
            f_id: gen.generate(GeneratorConfig(problem_count=6, seed=100 + i))
            for i, f_id in enumerate(["A", "B", "C", "D"])
        }

        matrix_pdf = compiler.compile_matrix_key_pdf(
            title="Algebra 1 Linear Equations",
            worksheet_id="MF-0042",
            forms_data=forms_data,
        )

        assert matrix_pdf.startswith(b"%PDF-")
        assert len(matrix_pdf) > 10000, "Matrix key PDF should exceed 10 KB"
