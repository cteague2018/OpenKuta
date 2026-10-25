from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import cv2
import numpy as np

CANONICAL_WIDTH = 2550   # 8.5in * 300 DPI
CANONICAL_HEIGHT = 3300  # 11.0in * 300 DPI
CANONICAL_MARGIN = 150   # 0.5in * 300 DPI


@dataclass
class AlignmentResult:
    warped_image: np.ndarray
    metadata: Dict[str, Any]
    detected_marker_ids: list[int]
    is_aligned: bool
    error_message: Optional[str] = None


class WorksheetAligner:
    """Detects 4 ArUco markers, deskews/perspective-corrects to 2550x3300,
    and decodes QR payload.
    """

    def __init__(self) -> None:
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.aruco_detector = cv2.aruco.ArucoDetector(
            self.aruco_dict, self.aruco_params
        )
        self.qr_detector = cv2.QRCodeDetector()

    def load_image(self, image_data: bytes | np.ndarray) -> np.ndarray:
        """Decode image bytes or validate numpy array."""
        if isinstance(image_data, bytes):
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Failed to decode uploaded image")
            return img
        return image_data

    def detect_markers(self, image: np.ndarray) -> Dict[int, np.ndarray]:
        """Detect ArUco markers and return map of marker_id -> center
        coordinate (x, y).
        """
        gray = (
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if len(image.shape) == 3
            else image
        )
        corners, ids, _ = self.aruco_detector.detectMarkers(gray)

        marker_centers: Dict[int, np.ndarray] = {}
        if ids is not None:
            ids = ids.flatten()
            for marker_id, corner in zip(ids, corners, strict=False):
                # corner shape: (1, 4, 2)
                pts = corner[0]
                center = np.mean(pts, axis=0)
                marker_centers[int(marker_id)] = center

        return marker_centers

    def align_and_deskew(self, image: np.ndarray) -> Tuple[np.ndarray, bool]:
        """Apply 4-point perspective warp based on markers 0 (TL), 1 (TR),
        2 (BR), 3 (BL).
        """
        marker_centers = self.detect_markers(image)

        required_markers = [0, 1, 2, 3]
        if not all(m in marker_centers for m in required_markers):
            # If some markers are missing, return original with warning
            return image, False

        # Source coordinates in scanned image
        # Marker 0: Top-Left, Marker 1: Top-Right,
        # Marker 2: Bottom-Right, Marker 3: Bottom-Left
        src_pts = np.array([
            marker_centers[0],
            marker_centers[1],
            marker_centers[2],
            marker_centers[3],
        ], dtype=np.float32)

        # Destination coordinates in canonical 2550 x 3300 canvas
        # Center of markers are at CANONICAL_MARGIN / 2 from edge,
        # or ~CANONICAL_MARGIN. Marker center offset: ~100px from border
        offset = CANONICAL_MARGIN
        dst_pts = np.array([
            [offset, offset],  # Top-Left
            [CANONICAL_WIDTH - offset, offset],  # Top-Right
            [
                CANONICAL_WIDTH - offset,
                CANONICAL_HEIGHT - offset,
            ],  # Bottom-Right
            [offset, CANONICAL_HEIGHT - offset],  # Bottom-Left
        ], dtype=np.float32)

        try:
            transform_matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(
                image,
                transform_matrix,
                (CANONICAL_WIDTH, CANONICAL_HEIGHT),
                flags=cv2.INTER_LANCZOS4,
            )
            return warped, True
        except Exception:
            return image, False

    def decode_qr(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect and decode worksheet QR code from header area with
        multi-pass fallback.
        """
        gray = (
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if len(image.shape) == 3
            else image
        )

        # 1. Fast path: header ROI (top-right quadrant)
        h, w = gray.shape[:2]
        header_roi = gray[0:int(h * 0.30), int(w * 0.45):w]

        decoded_info, _, _ = self.qr_detector.detectAndDecode(header_roi)
        if not decoded_info:
            # 2. Contrast-enhanced header ROI
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced_roi = clahe.apply(header_roi)
            decoded_info, _, _ = self.qr_detector.detectAndDecode(enhanced_roi)

        if not decoded_info:
            # 3. Full image direct
            decoded_info, _, _ = self.qr_detector.detectAndDecode(gray)

        if not decoded_info:
            # 4. Full image CLAHE
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced_full = clahe.apply(gray)
            decoded_info, _, _ = self.qr_detector.detectAndDecode(
                enhanced_full
            )

        if not decoded_info:
            # 5. Rotation search (in case photo is rotated 90, 180, 270 deg)
            rotations = (
                cv2.ROTATE_90_CLOCKWISE,
                cv2.ROTATE_180,
                cv2.ROTATE_90_COUNTERCLOCKWISE,
            )
            for rot in rotations:
                rot_img = cv2.rotate(gray, rot)
                decoded_info, _, _ = self.qr_detector.detectAndDecode(rot_img)
                if decoded_info:
                    break

        if decoded_info:
            try:
                raw_dict = json.loads(decoded_info)
                # Normalize abbreviated QR keys
                normalized = {
                    "worksheet_id": (
                        raw_dict.get("w")
                        or raw_dict.get("worksheet_id", "unknown")
                    ),
                    "form_id": (
                        raw_dict.get("f") or raw_dict.get("form_id", "A")
                    ),
                    "seed": (
                        raw_dict.get("s")
                        if "s" in raw_dict
                        else raw_dict.get("seed", 42)
                    ),
                    "problem_count": (
                        raw_dict.get("c")
                        if "c" in raw_dict
                        else raw_dict.get("problem_count", 6)
                    ),
                    "student_id": (
                        raw_dict.get("sid") or raw_dict.get("student_id")
                    ),
                    "class_id": (
                        raw_dict.get("cid") or raw_dict.get("class_id")
                    ),
                    "_raw": raw_dict,
                }
                return normalized
            except Exception:
                return {"raw": decoded_info}
        return {}

    def process(self, image_input: bytes | np.ndarray) -> AlignmentResult:
        """Run full alignment and metadata retrieval pipeline."""
        img = self.load_image(image_input)
        marker_centers = self.detect_markers(img)
        detected_ids = list(marker_centers.keys())

        warped, is_aligned = self.align_and_deskew(img)
        metadata = self.decode_qr(warped)

        error_msg = (
            None
            if is_aligned
            else "Missing 1 or more corner fiducials "
            "(requires markers 0, 1, 2, 3)"
        )
        return AlignmentResult(
            warped_image=warped,
            metadata=metadata,
            detected_marker_ids=detected_ids,
            is_aligned=is_aligned,
            error_message=error_msg,
        )
