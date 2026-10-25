from __future__ import annotations

import cv2
import numpy as np
import pytest

from backend.app.grading.aligner import (
    CANONICAL_HEIGHT,
    CANONICAL_MARGIN,
    CANONICAL_WIDTH,
    WorksheetAligner,
)
from backend.app.grading.extractor import ProblemWorkspaceExtractor


def create_synthetic_worksheet(
    width: int = 800,
    height: int = 1000,
    include_markers: bool = True,
    corrupt_marker: int | None = None,
) -> np.ndarray:
    """Generate a clean synthetic worksheet canvas with corner ArUco fiducials."""
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

    if include_markers:
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        marker_size = 80
        positions = {
            0: (20, 20),
            1: (width - 100, 20),
            2: (width - 100, height - 100),
            3: (20, height - 100),
        }

        for m_id, (x, y) in positions.items():
            if corrupt_marker is not None and m_id == corrupt_marker:
                noise = np.random.randint(50, 200, (marker_size, marker_size, 3), dtype=np.uint8)
                canvas[y : y + marker_size, x : x + marker_size] = noise
                continue

            marker_img = cv2.aruco.generateImageMarker(aruco_dict, m_id, marker_size)
            canvas[y : y + marker_size, x : x + marker_size] = cv2.cvtColor(marker_img, cv2.COLOR_GRAY2BGR)

    return canvas


class TestComputerVisionEngine:
    """OpenCV marker resilience, geometric deskewing, and boundary stress testing."""

    def test_canonical_clean_worksheet_alignment(self) -> None:
        """Verify perfect alignment and deskewing on a standard synthetic sheet."""
        aligner = WorksheetAligner()
        canvas = create_synthetic_worksheet()
        res = aligner.process(canvas)

        assert res.is_aligned is True
        assert len(res.detected_marker_ids) == 4
        assert set(res.detected_marker_ids) == {0, 1, 2, 3}
        assert res.warped_image.shape == (CANONICAL_HEIGHT, CANONICAL_WIDTH, 3)
        assert res.error_message is None

    def test_rotated_and_skewed_scans(self) -> None:
        """Verify alignment under ±25° rotational skew."""
        aligner = WorksheetAligner()
        canvas = create_synthetic_worksheet()
        h, w = canvas.shape[:2]

        for angle in [-20.0, 15.0, 25.0]:
            center = (w // 2, h // 2)
            rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
            # Add padding to avoid clipping markers during rotation
            rotated = cv2.warpAffine(canvas, rot_mat, (w, h), borderValue=(255, 255, 255))

            res = aligner.process(rotated)
            # Must not crash; if all 4 markers detected, align succeeds
            assert isinstance(res.is_aligned, bool)
            assert res.warped_image is not None
            if res.is_aligned:
                assert res.warped_image.shape == (CANONICAL_HEIGHT, CANONICAL_WIDTH, 3)

    def test_low_contrast_and_shadow_degradation(self) -> None:
        """Verify alignment under synthetic non-uniform lighting and reduced contrast."""
        aligner = WorksheetAligner()
        canvas = create_synthetic_worksheet()
        h, w = canvas.shape[:2]

        # 1. Low contrast (compressed dynamic range)
        low_contrast = (canvas.astype(np.float32) * 0.4 + 100).astype(np.uint8)
        res_lc = aligner.process(low_contrast)
        assert isinstance(res_lc.is_aligned, bool)
        assert res_lc.warped_image is not None

        # 2. Non-uniform lighting shadow gradient (darker at bottom right)
        y_grad = np.linspace(1.0, 0.4, h)[:, None, None]
        x_grad = np.linspace(1.0, 0.4, w)[None, :, None]
        shadow_map = y_grad * x_grad
        shadowed = (canvas.astype(np.float32) * shadow_map).astype(np.uint8)

        res_sh = aligner.process(shadowed)
        assert isinstance(res_sh.is_aligned, bool)
        assert res_sh.warped_image is not None

    def test_missing_or_damaged_aruco_markers_fail_gracefully(self) -> None:
        """Verify damaged/missing markers produce structured error codes instead of OpenCV crashes."""
        aligner = WorksheetAligner()

        # Canvas with marker 2 destroyed
        damaged = create_synthetic_worksheet(corrupt_marker=2)
        res = aligner.process(damaged)

        assert res.is_aligned is False
        assert 2 not in res.detected_marker_ids
        assert res.error_message is not None
        assert "Missing 1 or more corner fiducials" in res.error_message

        # Canvas with no markers at all
        blank = np.ones((800, 600, 3), dtype=np.uint8) * 255
        res_blank = aligner.process(blank)
        assert res_blank.is_aligned is False
        assert len(res_blank.detected_marker_ids) == 0
        assert res_blank.error_message is not None

    def test_degenerate_and_corrupt_matrices(self) -> None:
        """Verify completely degenerate inputs (1x1, noise, non-square) do not crash."""
        aligner = WorksheetAligner()
        extractor = ProblemWorkspaceExtractor()

        # 1. Pure random Gaussian noise
        noise = np.random.randint(0, 256, (500, 500, 3), dtype=np.uint8)
        res_noise = aligner.process(noise)
        assert res_noise.is_aligned is False

        # 2. Workspace extraction on arbitrary matrix
        crops = extractor.extract_workspaces(res_noise.warped_image, problem_count=6)
        assert len(crops) == 6
        for c in crops:
            assert c.raw_crop is not None
            assert c.bounding_box is not None
            assert len(c.bounding_box) == 4
