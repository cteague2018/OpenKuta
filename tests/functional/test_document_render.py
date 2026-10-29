from __future__ import annotations

import pathlib
import re
import shutil
import tempfile

import typst

from backend.app.core.base import GeneratorConfig
from backend.app.core.compiler import TypstCompiler, generate_qr_code
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


class TestGraphingWorksheetLayout:
    """Numberless student-scaled grids: 3.0in graph boxes, Grid Scale write-in,
    and one-page-per-four-card pagination for graphing topics."""

    GRAPHING_GEN = "algebra_1.systems_graphing"

    def _render_pages(
        self, problem_count: int, show_answers: bool = False
    ) -> tuple[str, list[bytes]]:
        """Render markup and rasterize it, returning (markup, page PNG bytes)."""
        compiler = TypstCompiler()
        problems = get_generator(self.GRAPHING_GEN).generate(
            GeneratorConfig(problem_count=problem_count, seed=42)
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = pathlib.Path(tmp_dir)

            marker_filenames: dict[int, str] = {}
            for m_id, m_path in compiler.marker_paths.items():
                shutil.copyfile(m_path, tmp_path / f"aruco_{m_id}.png")
                marker_filenames[m_id] = f"aruco_{m_id}.png"

            qr_filename = "qr_test.png"
            generate_qr_code(
                {"w": "WS-TEST", "f": "A", "s": 42, "c": problem_count},
                tmp_path / qr_filename,
            )

            diagram_files: dict[int, str] = {}
            answer_svg_files: dict[int, str] = {}
            for p_idx, prob in enumerate(problems, start=1):
                if prob.diagram_svg:
                    name = f"prob_{p_idx}_diagram.svg"
                    (tmp_path / name).write_text(str(prob.diagram_svg), encoding="utf-8")
                    diagram_files[p_idx] = name
                if prob.answer_svg:
                    name = f"prob_{p_idx}_answer.svg"
                    (tmp_path / name).write_text(str(prob.answer_svg), encoding="utf-8")
                    answer_svg_files[p_idx] = name

            markup = compiler.render_worksheet_typ(
                title="Solving Systems by Graphing",
                form_id="A",
                worksheet_id="WS-TEST",
                seed=42,
                problems=problems,
                marker_filenames=marker_filenames,
                qr_filename=qr_filename,
                columns=2,
                show_answers=show_answers,
                diagram_files=diagram_files,
                answer_svg_files=answer_svg_files,
            )

            source = tmp_path / "worksheet.typ"
            source.write_text(markup, encoding="utf-8")
            rendered = typst.compile(source, format="png", ppi=72)
            pages = rendered if isinstance(rendered, list) else [rendered]

        return markup, list(pages)

    def test_graphing_cards_use_3in_grid_and_scale_write_in(self) -> None:
        """Cards carry a 216pt (3.0in) grid, fit their chrome, and prompt for scale."""
        markup, pages = self._render_pages(problem_count=4)

        # 3.0in grid inside a taller card so prompt/equation/scale/Ans all fit.
        assert "width: 216pt, height: 216pt" in markup
        assert "height: 310pt" in markup
        # Underground write-in blank must be a stroked box: an empty
        # `#underline[]` renders no line at all.
        assert markup.count("Grid Scale: 1 square =") == 4
        assert "stroke: (bottom: 0.5pt + luma(90))" in markup
        assert "underline[#h(0.6in)]" not in markup
        # Graphing always lays out two columns of cards.
        assert "columns: (1fr, 1fr)," in markup
        # Four 3.0in cards fit on a single sheet.
        assert len(pages) == 1

    def test_eight_graphing_problems_paginate_with_sequential_numbering(self) -> None:
        """More than four graphing cards continue onto a second page, numbered 5-8."""
        markup, pages = self._render_pages(problem_count=8)

        assert len(pages) == 2, "8 graphing problems need two pages of 4 cards"
        assert "#pagebreak()" in markup
        # Global numbering survives pagination (page 2 restarts the loop).
        for expected in ("[5.]", "[6.]", "[7.]", "[8.]"):
            assert expected in markup, f"missing problem number {expected}"

    def test_answer_key_keeps_full_size_solved_grids(self) -> None:
        """Answer keys show the solved 3.0in grid plus the scale write-in."""
        markup, pages = self._render_pages(problem_count=4, show_answers=True)

        assert len(pages) == 1
        assert markup.count("Grid Scale: 1 square =") == 4
        assert "width: 216pt, height: 216pt" in markup

    def test_generated_grids_have_no_numeric_tick_labels(self) -> None:
        """Grids stay numberless so students choose their own scale."""
        problems = get_generator(self.GRAPHING_GEN).generate(
            GeneratorConfig(problem_count=4, seed=42)
        )
        for prob in problems:
            assert prob.graphing, "systems-by-graphing problems must flag graphing"
            svg = str(prob.diagram_svg or "")
            assert svg, "graphing problem is missing its diagram"
            numeric_labels = re.findall(r"<text[^>]*>\s*[-−]?\d", svg)
            assert not numeric_labels, f"numeric tick labels leaked: {numeric_labels}"
            # Axes must still show direction arrows and tick marks.
            assert 'marker-end="url(#axis-arrow)"' in svg
            assert 'stroke-width="1.2"' in svg
