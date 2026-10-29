from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class BBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def intersects(self, other: BBox, padding: float = 2.0) -> bool:
        return not (
            self.x_max + padding < other.x_min
            or self.x_min - padding > other.x_max
            or self.y_max + padding < other.y_min
            or self.y_min - padding > other.y_max
        )


@dataclass(frozen=True)
class LineSegment:
    x1: float
    y1: float
    x2: float
    y2: float

    def distance_to_point(self, px: float, py: float) -> float:
        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        if dx == 0 and dy == 0:
            return math.hypot(px - self.x1, py - self.y1)
        t = max(0.0, min(1.0, ((px - self.x1) * dx + (py - self.y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(px - (self.x1 + t * dx), py - (self.y1 + t * dy))


def segment_intersects_bbox(seg: LineSegment, box: BBox) -> bool:
    """Return True when any part of ``seg`` lies inside ``box`` (Liang-Barsky clip)."""
    dx, dy = seg.x2 - seg.x1, seg.y2 - seg.y1
    t0, t1 = 0.0, 1.0
    for p, q in (
        (-dx, seg.x1 - box.x_min),
        (dx, box.x_max - seg.x1),
        (-dy, seg.y1 - box.y_min),
        (dy, box.y_max - seg.y1),
    ):
        if p == 0:
            # Segment is parallel to this boundary: reject only if it starts outside.
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


class SVGCollisionSolver:
    def __init__(
        self,
        width: float = 320.0,
        height: float = 240.0,
        margin: float = 12.0,
        clearance: float = 3.0,
    ) -> None:
        self.width = width
        self.height = height
        self.margin = margin
        self.clearance = clearance
        self.placed_boxes: List[BBox] = []
        # Drawn geometry (lines, curves, circles) that a text label must not cover.
        self.obstacles: List[LineSegment] = []
        # Reference geometry (the axes) that a label may sit on when a point lies on
        # the axis itself - avoided when possible, but never at the cost of covering a
        # plotted line or curve.
        self.soft_obstacles: List[LineSegment] = []

    def add_segment(self, x1: float, y1: float, x2: float, y2: float, soft: bool = False) -> None:
        """Register a drawn segment (line, curve, asymptote, axis) as an obstacle."""
        if all(math.isfinite(v) for v in (x1, y1, x2, y2)):
            seg = LineSegment(float(x1), float(y1), float(x2), float(y2))
            (self.soft_obstacles if soft else self.obstacles).append(seg)

    def add_polyline(self, points: List[Tuple[float, float]], soft: bool = False) -> None:
        """Register every segment of a sampled curve as an obstacle."""
        for (x1, y1), (x2, y2) in zip(points, points[1:], strict=False):
            self.add_segment(x1, y1, x2, y2, soft=soft)

    def add_ellipse(
        self, cx: float, cy: float, rx: float, ry: float, steps: int = 24, soft: bool = False
    ) -> None:
        """Approximate a circle/ellipse outline with short segments."""
        pts = [
            (cx + rx * math.cos(2 * math.pi * i / steps), cy + ry * math.sin(2 * math.pi * i / steps))
            for i in range(steps + 1)
        ]
        self.add_polyline(pts, soft=soft)

    def add_marker(self, cx: float, cy: float, radius: float = 4.0) -> None:
        """Reserve the footprint of a plotted point so labels never sit on top of it."""
        self.placed_boxes.append(BBox(cx - radius, cy - radius, cx + radius, cy + radius))

    def _obstacle_hits(self, box: BBox, reach: float, anchor: Tuple[float, float]) -> Tuple[int, int]:
        """Count (hard, soft) obstacle intersections for ``box``.

        Only obstacles within ``reach`` of the label anchor are considered, which keeps
        placement cheap on densely sampled curves.
        """
        pad = self.clearance
        grown = BBox(box.x_min - pad, box.y_min - pad, box.x_max + pad, box.y_max + pad)
        hard = sum(
            1
            for seg in self.obstacles
            if seg.distance_to_point(*anchor) <= reach and segment_intersects_bbox(seg, grown)
        )
        soft = sum(
            1
            for seg in self.soft_obstacles
            if seg.distance_to_point(*anchor) <= reach and segment_intersects_bbox(seg, grown)
        )
        return hard, soft

    @staticmethod
    def estimate_text_bbox(
        cx: float, cy: float, text: str, font_size: float = 13.0, anchor: str = "middle"
    ) -> BBox:
        w = max(1, len(text.replace("$", ""))) * (font_size * 0.58) + 4.0
        h = font_size * 1.15 + 3.0
        if anchor == "start":
            center_x = cx + w / 2.0
        elif anchor == "end":
            center_x = cx - w / 2.0
        else:
            center_x = cx
        return BBox(center_x - w / 2.0, cy - h / 2.0, center_x + w / 2.0, cy + h / 2.0)

    def place_label(
        self,
        anchor_x: float,
        anchor_y: float,
        text: str,
        preferred_angle_deg: float = 45.0,
        font_size: float = 13.0,
    ) -> Tuple[float, float]:
        radii = (22.0, 30.0, 38.0, 46.0, 54.0, 64.0)
        step = 15.0
        offsets = [0.0]
        k = 1
        while k * step <= 180.0:
            offsets.extend([k * step, -k * step])
            k += 1
        reach = radii[-1] + 80.0

        # Rank candidates: covering a plotted line/curve costs far more than grazing an
        # axis, and covering another label costs most of all.
        best: Optional[Tuple[int, int, float, float, BBox]] = None

        for r_index, r in enumerate(radii):
            for offset in offsets:
                theta = math.radians(preferred_angle_deg + offset)
                cx = anchor_x + r * math.cos(theta)
                cy = anchor_y - r * math.sin(theta)
                box = self.estimate_text_bbox(cx, cy, text, font_size)

                # Check boundary margins
                if (
                    box.x_min < self.margin
                    or box.x_max > self.width - self.margin
                    or box.y_min < self.margin
                    or box.y_max > self.height - self.margin
                ):
                    continue

                text_hits = sum(1 for b in self.placed_boxes if box.intersects(b))
                hard, soft = self._obstacle_hits(box, reach, (anchor_x, anchor_y))
                if text_hits == 0 and hard == 0 and soft == 0:
                    self.placed_boxes.append(box)
                    return (round(cx, 2), round(cy, 2))

                score = 100 * hard + 10 * text_hits + soft
                rank = (score, r_index)
                if best is None or (best[0], best[1]) > rank:
                    best = (score, r_index, cx, cy, box)

        # Never leave a label on top of a plotted line/curve: only a candidate that
        # merely grazes an axis (score < 100) is accepted as a compromise.
        if best is not None and best[0] < 100:
            _, _, cx, cy, box = best
            self.placed_boxes.append(box)
            return (round(cx, 2), round(cy, 2))

        # Fallback to direct placement if constrained
        fb_box = self.estimate_text_bbox(anchor_x, anchor_y, text, font_size)
        self.placed_boxes.append(fb_box)
        return (anchor_x, anchor_y)
