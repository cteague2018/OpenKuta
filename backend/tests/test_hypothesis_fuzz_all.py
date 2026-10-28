from __future__ import annotations

import re
import xml.etree.ElementTree as ET

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

try:
    from backend.app.generators.registry import get_all_registered_generators
    from backend.app.generators.svg_layout_engine import BBox, SVGCollisionSolver
    from backend.app.generators.validator import validate_problem_sanity
except ImportError:
    from app.generators.registry import get_all_registered_generators
    from app.generators.svg_layout_engine import BBox, SVGCollisionSolver
    from app.generators.validator import validate_problem_sanity

NAN_INF_REGEX = re.compile(r"\b(nan|inf|-inf|None)\b", re.IGNORECASE)


def assert_svg_zero_defects(svg_str: str) -> None:
    assert not NAN_INF_REGEX.search(svg_str), f"NaN/Inf detected in SVG: {svg_str[:200]}"
    root = ET.fromstring(svg_str)
    view_box = root.attrib.get("viewBox", "")
    parts = [float(x) for x in view_box.replace(",", " ").split() if x]
    assert len(parts) == 4 and parts[2] > 0 and parts[3] > 0, f"Invalid viewBox: {view_box}"

    text_boxes: list[BBox] = []
    for elem in root.iter():
        if elem.tag.endswith("text"):
            x = float(elem.attrib.get("x", "0"))
            y = float(elem.attrib.get("y", "0"))
            font_size = float(elem.attrib.get("font-size", "13").replace("px", ""))
            anchor = elem.attrib.get("text-anchor", "start")
            content = "".join(elem.itertext()).strip()
            if not content:
                continue
            box = SVGCollisionSolver.estimate_text_bbox(x, y, content, font_size, anchor=anchor)
            for existing in text_boxes:
                assert not box.intersects(existing, padding=-1.5), (
                    f"SVG text label collision detected for '{content}' at ({x}, {y})"
                )
            text_boxes.append(box)


@pytest.mark.parametrize("gen_id,gen_fn", list(get_all_registered_generators().items()))
@pytest.mark.parametrize("difficulty", ["mild", "medium", "spicy"])
@settings(max_examples=10, deadline=None)
@given(seed=st.integers(min_value=1, max_value=100_000))
def test_fuzz_generator_mathematical_and_visual_truth(
    gen_id: str, gen_fn, difficulty: str, seed: int
) -> None:
    problem = gen_fn(seed=seed, difficulty=difficulty)
    validate_problem_sanity(problem)
    assert problem.prompt_text.strip()
    assert problem.equation_typst.strip()
    assert problem.answer_typst.strip()
    if problem.distractors:
        normalized = [d.strip() for d in problem.distractors]
        assert len(set(normalized)) == len(normalized)
        assert problem.answer_typst.strip() not in normalized
    if problem.diagram_svg:
        assert_svg_zero_defects(problem.diagram_svg)
    if problem.answer_svg:
        assert_svg_zero_defects(problem.answer_svg)
