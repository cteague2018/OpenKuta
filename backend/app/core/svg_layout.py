from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple


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


class SVGCollisionSolver:
    def __init__(self, width: float = 320.0, height: float = 240.0, margin: float = 12.0) -> None:
        self.width = width
        self.height = height
        self.margin = margin
        self.placed_boxes: List[BBox] = []

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
    ) -> Tuple[float, float]:
        radii = (22.0, 30.0, 38.0, 48.0)
        angle_offsets = (0.0, 30.0, -30.0, 45.0, -45.0, 60.0, -60.0, 90.0, -90.0, 135.0, -135.0, 180.0)

        for r in radii:
            for offset in angle_offsets:
                candidate_angle = preferred_angle_deg + offset
                theta = math.radians(candidate_angle)
                cx = anchor_x + r * math.cos(theta)
                cy = anchor_y - r * math.sin(theta)
                box = self.estimate_text_bbox(cx, cy, text)

                # Check boundary margins
                if (
                    box.x_min < self.margin
                    or box.x_max > self.width - self.margin
                    or box.y_min < self.margin
                    or box.y_max > self.height - self.margin
                ):
                    continue

                if not any(box.intersects(b) for b in self.placed_boxes):
                    self.placed_boxes.append(box)
                    return (round(cx, 2), round(cy, 2))

        # Fallback to direct placement if constrained
        fb_box = self.estimate_text_bbox(anchor_x, anchor_y, text)
        self.placed_boxes.append(fb_box)
        return (anchor_x, anchor_y)

