from pathlib import Path

from backend.app.core.base import GeneratorConfig, ProblemDifficulty
from backend.app.core.compiler import TypstCompiler
from backend.app.generators import COURSE_CATALOG, GENERATOR_REGISTRY, get_generator


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
        assert f'"{tid}"' in fe_text, f"Missing topic {tid} in frontend/app/catalogData.ts"


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
                                assert p.diagram_svg.startswith("<svg") and p.diagram_svg.endswith("</svg>")
                            if p.answer_svg:
                                assert p.answer_svg.startswith("<svg") and p.answer_svg.endswith("</svg>")

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
