import json
import numpy as np
import cv2
import pytest

from backend.app.grading.aligner import WorksheetAligner, CANONICAL_WIDTH, CANONICAL_HEIGHT
from backend.app.grading.extractor import ProblemWorkspaceExtractor
from backend.app.grading.verifier import CASStepVerifier, ErrorType


def test_cas_verifier_perfect_solution():
    verifier = CASStepVerifier()
    steps = [
        "2*x + 6 = 14",
        "2*x = 8",
        "x = 4"
    ]
    report = verifier.verify_solution_steps("prob_1", steps)
    assert report.final_answer_correct is True
    assert report.partial_credit_score == 1.0
    assert report.first_failure_step is None
    assert report.error_classification == ErrorType.NONE


def test_cas_verifier_arithmetic_error():
    verifier = CASStepVerifier()
    steps = [
        "2*x + 6 = 14",
        "2*x = 7",  # Error: 14 - 6 != 7
        "x = 7/2"
    ]
    report = verifier.verify_solution_steps("prob_2", steps)
    assert report.final_answer_correct is False
    assert report.first_failure_step == 2
    assert report.error_classification == ErrorType.ARITHMETIC_ERROR
    assert report.partial_credit_score < 1.0


def test_cas_verifier_distribution_error():
    verifier = CASStepVerifier()
    steps = [
        "3*(x + 4) = 21",
        "3*x + 4 = 21",  # Error: forgot to multiply 4 by 3
        "3*x = 17"
    ]
    report = verifier.verify_solution_steps("prob_3", steps)
    assert report.final_answer_correct is False
    assert report.first_failure_step == 2
    assert report.error_classification == ErrorType.DISTRIBUTION_ERROR


def test_workspace_extractor_coordinates():
    extractor = ProblemWorkspaceExtractor()
    coords = extractor.compute_box_coordinates(problem_count=6, columns=2)
    assert len(coords) == 6
    for x, y, w, h in coords:
        assert x >= 150
        assert y >= 400
        assert w > 0
        assert h > 0
        assert x + w <= CANONICAL_WIDTH
        assert y + h <= CANONICAL_HEIGHT


def test_aligner_aruco_and_qr():
    # Construct a synthetic canvas with 4 markers and a QR code
    aligner = WorksheetAligner()
    canvas = np.ones((1000, 800, 3), dtype=np.uint8) * 255

    # Insert 4 markers
    dict_aruco = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    m0 = cv2.aruco.generateImageMarker(dict_aruco, 0, 80)
    m1 = cv2.aruco.generateImageMarker(dict_aruco, 1, 80)
    m2 = cv2.aruco.generateImageMarker(dict_aruco, 2, 80)
    m3 = cv2.aruco.generateImageMarker(dict_aruco, 3, 80)

    # Paste markers near corners
    canvas[20:100, 20:100] = cv2.cvtColor(m0, cv2.COLOR_GRAY2BGR)
    canvas[20:100, 700:780] = cv2.cvtColor(m1, cv2.COLOR_GRAY2BGR)
    canvas[900:980, 700:780] = cv2.cvtColor(m2, cv2.COLOR_GRAY2BGR)
    canvas[900:980, 20:100] = cv2.cvtColor(m3, cv2.COLOR_GRAY2BGR)

    # Detect markers
    markers = aligner.detect_markers(canvas)
    assert 0 in markers
    assert 1 in markers
    assert 2 in markers
    assert 3 in markers

    # Deskew
    warped, is_aligned = aligner.align_and_deskew(canvas)
    assert is_aligned is True
    assert warped.shape == (CANONICAL_HEIGHT, CANONICAL_WIDTH, 3)

