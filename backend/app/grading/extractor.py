from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np


@dataclass
class WorkspaceCrop:
    problem_index: int
    raw_crop: np.ndarray
    binarized_crop: np.ndarray
    bounding_box: Tuple[int, int, int, int]  # (x, y, w, h)


class ProblemWorkspaceExtractor:
    """Slices problem bounding boxes from canonical 2550x3300 canvas and cleans handwriting marks."""

    def __init__(
        self,
        canvas_width: int = 2550,
        canvas_height: int = 3300,
        header_height: int = 400,
        margin_x: int = 150,
        margin_bottom: int = 150,
        gutter_x: int = 50,
        gutter_y: int = 40,
    ) -> None:
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.header_height = header_height
        self.margin_x = margin_x
        self.margin_bottom = margin_bottom
        self.gutter_x = gutter_x
        self.gutter_y = gutter_y

    def compute_box_coordinates(
        self, problem_count: int, columns: int = 2
    ) -> List[Tuple[int, int, int, int]]:
        """Compute pixel (x, y, w, h) bounding boxes matching the Typst template layout."""
        rows = max(1, (problem_count + columns - 1) // columns)
        usable_width = self.canvas_width - (2 * self.margin_x) - ((columns - 1) * self.gutter_x)
        col_width = int(usable_width / columns)

        usable_height = self.canvas_height - self.header_height - self.margin_bottom - ((rows - 1) * self.gutter_y)
        row_height = int(usable_height / rows)

        boxes: List[Tuple[int, int, int, int]] = []
        for idx in range(problem_count):
            r = idx // columns
            c = idx % columns

            x = self.margin_x + c * (col_width + self.gutter_x)
            y = self.header_height + r * (row_height + self.gutter_y)
            boxes.append((x, y, col_width, row_height))

        return boxes

    def binarize_pencil_strokes(self, crop_image: np.ndarray) -> np.ndarray:
        """Apply adaptive thresholding and bilateral filtering to enhance faint pencil strokes and remove shadows."""
        gray = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY) if len(crop_image.shape) == 3 else crop_image

        # Denoise while preserving sharp pencil strokes
        denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

        # Adaptive thresholding to handle uneven lighting and shadows
        binary = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            blockSize=25,
            C=12,
        )

        # Remove isolated single-pixel salt-and-pepper noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        return cleaned

    def extract_workspaces(
        self, aligned_canvas: np.ndarray, problem_count: int, columns: int = 2
    ) -> List[WorkspaceCrop]:
        """Slice and clean all problem workspace boxes from the aligned worksheet."""
        boxes = self.compute_box_coordinates(problem_count, columns=columns)
        h_max, w_max = aligned_canvas.shape[:2]

        results: List[WorkspaceCrop] = []
        for idx, (x, y, w, h) in enumerate(boxes, start=1):
            # Clamp bounds
            x0 = max(0, min(x, w_max - 1))
            y0 = max(0, min(y, h_max - 1))
            x1 = max(0, min(x + w, w_max))
            y1 = max(0, min(y + h, h_max))

            raw = aligned_canvas[y0:y1, x0:x1]
            binarized = self.binarize_pencil_strokes(raw) if raw.size > 0 else np.zeros((10, 10), dtype=np.uint8)

            results.append(
                WorkspaceCrop(
                    problem_index=idx,
                    raw_crop=raw,
                    binarized_crop=binarized,
                    bounding_box=(x0, y0, x1 - x0, y1 - y0),
                )
            )

        return results

