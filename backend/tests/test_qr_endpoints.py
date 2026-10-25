from __future__ import annotations

import io

import cv2
import numpy as np
from starlette.datastructures import UploadFile

from backend.app.api.qr_routes import (
    decode_qr_image,
    multi_pass_decode_qr,
    render_qr_code,
)


def test_qr_render_png():
    """Test generating a PNG QR code with metadata."""
    res = render_qr_code(w="WS-TEST-123", f="A", s=42, c=6, fmt="png")
    assert res.status_code == 200
    assert res.media_type == "image/png"
    assert len(res.body) > 100


def test_qr_render_svg():
    """Test generating an SVG vector QR code."""
    res = render_qr_code(w="WS-TEST-123", f="B", s=99, fmt="svg")
    assert res.status_code == 200
    assert res.media_type == "image/svg+xml"
    assert b"<svg" in res.body


def test_qr_render_and_decode_roundtrip():
    """Test generating a QR code image and uploading it to decode_qr_image."""
    # 1. Render PNG with specific payload
    payload = {
        "w": "WS-ROUNDTRIP",
        "f": "D",
        "s": 777,
        "c": 8,
        "sid": "STU-888",
        "cid": "cls_bio",
    }
    res = render_qr_code(
        w=payload["w"],
        f=payload["f"],
        s=payload["s"],
        c=payload["c"],
        sid=payload["sid"],
        cid=payload["cid"],
        fmt="png"
    )
    png_bytes = res.body

    # 2. Decode via decode_qr_image
    upload_file = UploadFile(
        filename="test_qr.png", file=io.BytesIO(png_bytes)
    )
    decode_res = decode_qr_image(file=upload_file)

    assert decode_res["success"] is True
    meta = decode_res["metadata"]
    assert meta["worksheet_id"] == "WS-ROUNDTRIP"
    assert meta["form_id"] == "D"
    assert meta["seed"] == 777
    assert meta["problem_count"] == 8
    assert meta["student_id"] == "STU-888"
    assert meta["class_id"] == "cls_bio"


def test_multi_pass_decode_rotations():
    """Test multi_pass_decode_qr successfully recovers rotated QR codes."""
    res = render_qr_code(w="WS-ROTATED", f="B", s=123, fmt="png")
    nparr = np.frombuffer(res.body, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Rotate 90 degrees clockwise
    rot_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    decoded_90 = multi_pass_decode_qr(rot_90)
    assert decoded_90.get("worksheet_id") == "WS-ROTATED"

    # Rotate 180 degrees
    rot_180 = cv2.rotate(img, cv2.ROTATE_180)
    decoded_180 = multi_pass_decode_qr(rot_180)
    assert decoded_180.get("worksheet_id") == "WS-ROTATED"
