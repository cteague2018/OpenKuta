"""Coordinate labels must never be obscured by the plotted lines, curves or axes.

Data labels like ``(-3, -4)`` used to be placed at a fixed offset from their point, so a
plotted line could run straight through the text. Labels are now placed by
``SVGCollisionSolver``, which knows about every drawn segment; this test parses the
rendered SVG and asserts the invariant directly, so a future change to either the solver
or the plane renderer cannot silently regress it.
"""

from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET
from typing import Iterator, List, Tuple

import pytest

from backend.app.core.base import GeneratorConfig
from backend.app.core.svg_utils import GRAPH_PLANE_ATTR
from backend.app.generators import GENERATOR_REGISTRY, get_generator

GRID_STROKES = {"#cbd5e1", "#e2e8f0", "#d1d5db", "#f1f5f9"}
AXIS_LABELS = {"x", "y", "0°", "90°", "180°", "270°"}


def _num(value: object, default: float = 0.0) -> float:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def _segments(root: ET.Element) -> List[Tuple[float, float, float, float, str]]:
    """Collect drawn segments as ``(x1, y1, x2, y2, kind)`` with kind grid/axis/drawn."""
    segments: List[Tuple[float, float, float, float, str]] = []

    def add(x1: float, y1: float, x2: float, y2: float, kind: str) -> None:
        segments.append((x1, y1, x2, y2, kind))

    for el in root.iter():
        tag = el.tag.split("}")[-1]
        stroke = str(el.get("stroke") or "").lower()
        if tag == "line":
            if stroke in GRID_STROKES:
                kind = "grid"
            elif stroke == "#0f172a":
                kind = "axis"
            else:
                kind = "drawn"
            add(_num(el.get("x1")), _num(el.get("y1")), _num(el.get("x2")), _num(el.get("y2")), kind)
        elif tag in ("polyline", "polygon"):
            values = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", el.get("points", ""))]
            points = list(zip(values[0::2], values[1::2], strict=False))
            pairs = list(zip(points, points[1:], strict=False))
            if tag == "polygon" and len(points) > 2:
                pairs.append((points[-1], points[0]))
            for (x1, y1), (x2, y2) in pairs:
                add(x1, y1, x2, y2, "drawn")
        elif tag == "ellipse":
            cx, cy = _num(el.get("cx")), _num(el.get("cy"))
            rx, ry = _num(el.get("rx")), _num(el.get("ry"))
            steps = 24
            ring = [
                (cx + rx * math.cos(2 * math.pi * i / steps), cy + ry * math.sin(2 * math.pi * i / steps))
                for i in range(steps + 1)
            ]
            for (x1, y1), (x2, y2) in zip(ring, ring[1:], strict=False):
                add(x1, y1, x2, y2, "drawn")
    return segments


def _intersects(segment: Tuple[float, float, float, float, str], box: Tuple[float, float, float, float]) -> bool:
    """Liang-Barsky clip test between a segment and an axis-aligned box."""
    x1, y1, x2, y2 = segment[0], segment[1], segment[2], segment[3]
    x_min, y_min, x_max, y_max = box
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - x_min), (dx, x_max - x1), (-dy, y1 - y_min), (dy, y_max - y1)):
        if p == 0:
            if q < 0:
                return False
            continue
        t = q / p
        if p < 0:
            if t > t1:
                return False
            t0 = max(t0, t)
        else:
            if t < t0:
                return False
            t1 = min(t1, t)
    return t0 <= t1


def _label_boxes(root: ET.Element) -> Iterator[Tuple[str, Tuple[float, float, float, float]]]:
    for el in root.iter():
        if el.tag.split("}")[-1] != "text":
            continue
        label = (el.text or "").strip()
        if not label or label in AXIS_LABELS:
            continue
        size = _num(el.get("font-size"), 9.0)
        cx, cy = _num(el.get("x")), _num(el.get("y"))
        width = max(1, len(label)) * (size * 0.58) + 4.0
        height = size * 1.15 + 3.0
        anchor = el.get("text-anchor", "start")
        if anchor == "middle":
            center_x = cx
        elif anchor == "end":
            center_x = cx - width / 2
        else:
            center_x = cx + width / 2
        yield label, (center_x - width / 2, cy - height / 2, center_x + width / 2, cy + height / 2)


@pytest.mark.parametrize("gen_id", sorted(GENERATOR_REGISTRY))
def test_data_labels_are_never_covered_by_plotted_geometry(gen_id: str) -> None:
    """Every ``text`` label on a coordinate plane must clear the drawn lines and curves."""
    try:
        problems = get_generator(gen_id).generate(GeneratorConfig(problem_count=2, seed=5))
    except Exception:  # pragma: no cover - generators that need richer configs
        pytest.skip(f"{gen_id} cannot be generated with a plain config")

    violations = []
    for problem in problems:
        for field in ("diagram_svg", "answer_svg"):
            svg = getattr(problem, field, None)
            if not svg or GRAPH_PLANE_ATTR not in str(svg):
                continue
            root = ET.fromstring(str(svg))
            drawn = [seg for seg in _segments(root) if seg[4] != "grid"]
            for label, box in _label_boxes(root):
                if any(_intersects(seg, box) for seg in drawn):
                    violations.append(f"{problem.id}/{field}: label {label!r} overlaps drawn geometry")

    assert not violations, f"{gen_id} placed data labels on top of plotted geometry:\n" + "\n".join(
        violations[:10]
    )
