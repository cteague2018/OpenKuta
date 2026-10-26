import xml.etree.ElementTree as ET
from pathlib import Path

from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.core.compiler import TypstCompiler
from backend.app.generators import COURSE_CATALOG, GENERATOR_REGISTRY, get_generator


def _assert_svg_not_clipped(svg_str: str, tid: str, diff_val: str, field_name: str) -> None:
    """Ensure every SVG has responsive scaling and zero out-of-bounds circles, ellipses, or labels."""
    assert svg_str.startswith("<svg") and svg_str.endswith("</svg>")
    root = ET.fromstring(svg_str)
    vb = root.attrib.get("viewBox", "0 0 220 220").split()
    width = float(vb[2])
    height = float(vb[3])
    assert "max-width:100%;height:auto" in root.attrib.get("style", ""), f"{tid} {field_name} missing responsive SVG style"
    for elem in root.iter():
        tag = elem.tag.split("}")[-1]
        if tag == "circle":
            cx = float(elem.attrib["cx"])
            cy = float(elem.attrib["cy"])
            r = float(elem.attrib["r"])
            assert cx - r >= -0.5 and cx + r <= width + 0.5, f"{tid} ({diff_val}) {field_name} circle x clipped: {cx} in {width}"
            assert cy - r >= -0.5 and cy + r <= height + 0.5, f"{tid} ({diff_val}) {field_name} circle y clipped: {cy} in {height}"
        elif tag == "ellipse":
            cx = float(elem.attrib["cx"])
            cy = float(elem.attrib["cy"])
            rx = float(elem.attrib["rx"])
            ry = float(elem.attrib["ry"])
            assert cx - rx >= -0.5 and cx + rx <= width + 0.5, f"{tid} ({diff_val}) {field_name} ellipse x clipped"
            assert cy - ry >= -0.5 and cy + ry <= height + 0.5, f"{tid} ({diff_val}) {field_name} ellipse y clipped"
        elif tag == "text":
            tx = float(elem.attrib["x"])
            ty = float(elem.attrib["y"])
            txt = elem.text or ""
            anchor = elem.attrib.get("text-anchor", "start")
            est_w = len(txt) * 4.2
            x0 = tx if anchor == "start" else (tx - est_w if anchor == "end" else tx - est_w / 2)
            x1 = tx + est_w if anchor == "start" else (tx if anchor == "end" else tx + est_w / 2)
            assert x0 >= -4.0 and x1 <= width + 4.0, f"{tid} ({diff_val}) {field_name} text '{txt}' clipped horizontally"
            assert 4.0 <= ty <= height + 2.0, f"{tid} ({diff_val}) {field_name} text '{txt}' clipped vertically"


def test_catalog_uniqueness_and_frontend_sync():
    """Verify all 598 topics have globally unique IDs, 1-to-1 generator mappings,
    and are 100% synchronized between backend catalog_data.json and frontend catalogData.ts.
    """
    topic_ids = []
    gen_ids = []
    for _course_key, course in COURSE_CATALOG.items():
        for cat in course["categories"]:
            for topic in cat["topics"]:
                topic_ids.append(topic["id"])
                gen_ids.append(topic["generator_id"])
                assert topic["available"] is True
                assert topic["id"] == topic["generator_id"]
                assert topic["generator_id"] in GENERATOR_REGISTRY

    assert len(topic_ids) == 598
    assert len(set(topic_ids)) == 598, "Duplicate topic IDs detected!"
    assert len(set(gen_ids)) == 598, "Topics must not share generator_id!"

    # Verify frontend catalogData.ts contains all 598 topic IDs
    fe_text = Path("frontend/app/catalogData.ts").read_text(encoding="utf-8")
    assert "diagram_svg?: string | null;" in fe_text
    assert "answer_svg?: string | null;" in fe_text
    for tid in topic_ids:
        assert f'"id": "{tid}"' in fe_text, f"Missing topic id {tid} in frontend/app/catalogData.ts"
        assert f'"generator_id": "{tid}"' in fe_text, (
            f"Mismatched generator_id {tid} in frontend/app/catalogData.ts"
        )


def test_all_598_topics_across_all_difficulties_and_visuals():
    """Forensic audit across all 598 topics x 3 difficulties (1,794 topic-difficulty pairs)."""
    diffs = [ProblemDifficulty.MILD, ProblemDifficulty.MEDIUM, ProblemDifficulty.SPICY]

    visual_keywords = [
        "graph",
        "plot",
        "histogram",
        "number line",
        "tape diagram",
        "hanger diagram",
        "area diagram",
        "slope field",
        "riemann sum table",
        "rules, using tables",
        "polar coordinates",
        "right triangle",
        "pythagorean",
        "inscribed angle",
        "parallel lines and transversal",
    ]

    total_checked = 0
    svg_count = 0

    for _course_key, course in COURSE_CATALOG.items():
        for cat in course["categories"]:
            cat["name"]
            for topic in cat["topics"]:
                tid = topic["id"]
                tname = topic["name"]
                gen = get_generator(topic["generator_id"])

                by_diff = {}
                for diff in diffs:
                    cfg = GeneratorConfig(
                        problem_count=3,
                        seed=42,
                        difficulty_distribution={
                            ProblemDifficulty.MILD: 1.0 if diff == ProblemDifficulty.MILD else 0.0,
                            ProblemDifficulty.MEDIUM: 1.0 if diff == ProblemDifficulty.MEDIUM else 0.0,
                            ProblemDifficulty.SPICY: 1.0 if diff == ProblemDifficulty.SPICY else 0.0,
                        },
                    )
                    probs = gen.generate(cfg)
                    assert len(probs) == 3, f"{tid} ({diff}) did not return 3 problems"
                    by_diff[diff] = probs

                    for p in probs:
                        assert p.prompt_text and len(p.prompt_text) > 5, f"{tid} empty prompt"
                        assert p.equation_typst, f"{tid} empty equation"
                        assert p.answer_typst and p.answer_typst not in (
                            "Graph",
                            "Shaded intersection region",
                        ), f"{tid} placeholder answer: {p.answer_typst}"
                        assert len(p.steps_typst) >= 3, f"{tid} ({diff}) < 3 steps"
                        assert len(p.distractors) >= 2, f"{tid} ({diff}) < 2 distractors"

                        if p.diagram_svg or p.answer_svg:
                            svg_count += 1
                            if p.diagram_svg:
                                _assert_svg_not_clipped(p.diagram_svg, tid, diff.value, "diagram_svg")
                            if p.answer_svg:
                                _assert_svg_not_clipped(p.answer_svg, tid, diff.value, "answer_svg")

                        # Check mandatory SVG presence for explicit visual/table topics
                        t_low = tname.lower()
                        if any(vk in t_low for vk in visual_keywords):
                            assert (
                                p.diagram_svg is not None or p.answer_svg is not None
                            ), f"Visual topic '{tid}' ({tname}) missing diagram_svg / answer_svg!"

                total_checked += 1

    assert total_checked == 598
    assert svg_count > 1500, f"Expected rich SVG coverage across visual topics, got {svg_count}"


def test_typst_pdf_compilation_with_embedded_svgs():
    """Verify TypstCompiler compiles both Student Worksheet and Answer Key PDFs
    with embedded coordinate planes, number lines, statistical plots, and tables.
    """
    compiler = TypstCompiler()
    sample_topic_ids = [
        "algebra_1.systems_of_equa.solving_by_graphing",
        "algebra_1.systems_of_equa.graphing_systems_of_inequ",
        "algebra_1.inequalities.compound_inequalities",
        "grade_6.data_sets_and_d.interpreting_box_plots",
        "grade_6.equations.hanger_diagrams",
        "calculus.differentiation.rules_using_tables",
        "calculus.differential_eq.slope_fields",
        "precalculus.polar_coordinat.graphs_of_polar_equations",
    ]
    problems = []
    for tid in sample_topic_ids:
        gen = get_generator(tid)
        probs = gen.generate(GeneratorConfig(problem_count=1, seed=101))
        assert probs[0].diagram_svg is not None or probs[0].answer_svg is not None
        problems.extend(probs)

    pdf_student = compiler.compile_worksheet_pdf(
        title="Forensic Visual Audit - Student",
        form_id="A",
        worksheet_id="WS-AUDIT",
        seed=101,
        problems=problems,
        show_answers=False,
    )
    assert pdf_student.startswith(b"%PDF-") and len(pdf_student) > 2000

    pdf_key = compiler.compile_worksheet_pdf(
        title="Forensic Visual Audit - Answer Key",
        form_id="A",
        worksheet_id="WS-AUDIT",
        seed=101,
        problems=problems,
        show_answers=True,
    )
    assert pdf_key.startswith(b"%PDF-") and len(pdf_key) > 2000


def test_single_problem_regeneration_and_student_view_graph_separation():
    """Verify single-problem preview (problem_count=1) succeeds and that Student View
    graphs never leak Answer Key graphs.
    """
    from backend.app.api.routes import GeneratePDFRequest, preview_problems

    # 1. Verify problem_count=1 succeeds in GeneratePDFRequest / preview_problems
    res1 = preview_problems(
        GeneratePDFRequest(
            generator_id="algebra_1.linear_equation.slope",
            problem_count=1,
            seed=42,
            question_type="multiple_choice",
        )
    )
    assert len(res1["problems"]) == 1
    p1 = res1["problems"][0]
    assert p1["generator_id"] == "algebra_1.linear_equation.slope"
    assert p1["diagram_svg"] is None, "Slope from two points must not show plotted line in Student View"
    assert p1["answer_svg"] is not None and p1["answer_svg"].startswith("<svg")

    # 2. Verify regenerating with a different seed produces a new distinct problem
    res2 = preview_problems(
        GeneratePDFRequest(
            generator_id="algebra_1.linear_equation.slope",
            problem_count=4,
            seed=777,
            question_type="multiple_choice",
        )
    )
    assert any(p["equation_typst"] != p1["equation_typst"] for p in res2["problems"])
