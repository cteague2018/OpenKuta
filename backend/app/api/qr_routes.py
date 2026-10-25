from __future__ import annotations

import io
import json
from typing import Any, Dict, Optional

import cv2
import numpy as np
import qrcode
import qrcode.constants as qr_constants
import qrcode.image.svg
from fastapi import APIRouter, File, HTTPException, Response, UploadFile

router = APIRouter(prefix="/api/qr", tags=["QR Code System"])


def multi_pass_decode_qr(image: np.ndarray) -> Dict[str, Any]:
    """Robust multi-pass QR decoder using contrast enhancement,
    multi-scale, and 4-way rotation search.
    """
    detector = cv2.QRCodeDetector()

    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Pass 1: Direct grayscale decode
    decoded_info, _, _ = detector.detectAndDecode(gray)
    if decoded_info:
        return _parse_payload(decoded_info)

    # Pass 2: Contrast Limited Adaptive Histogram Equalization (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    decoded_info, _, _ = detector.detectAndDecode(enhanced)
    if decoded_info:
        return _parse_payload(decoded_info)

    # Pass 3: Adaptive Otsu thresholding
    _, thresh = cv2.threshold(
        enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    decoded_info, _, _ = detector.detectAndDecode(thresh)
    if decoded_info:
        return _parse_payload(decoded_info)

    # Pass 4: 90, 180, 270 degree rotation search
    rotations = (
        cv2.ROTATE_90_CLOCKWISE,
        cv2.ROTATE_180,
        cv2.ROTATE_90_COUNTERCLOCKWISE,
    )
    for rot in rotations:
        rot_img = cv2.rotate(gray, rot)
        decoded_info, _, _ = detector.detectAndDecode(rot_img)
        if decoded_info:
            return _parse_payload(decoded_info)

    # Pass 5: Multi-scale search (downscale 0.5x, upscale 1.5x)
    for scale in (0.5, 1.5):
        scaled = cv2.resize(
            gray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR
        )
        decoded_info, _, _ = detector.detectAndDecode(scaled)
        if decoded_info:
            return _parse_payload(decoded_info)

    return {}


def _parse_payload(raw_text: str) -> Dict[str, Any]:
    """Parse JSON or raw QR payload into standardized dictionary."""
    try:
        raw_dict = json.loads(raw_text)
        return {
            "worksheet_id": (
                raw_dict.get("w") or raw_dict.get("worksheet_id", "unknown")
            ),
            "form_id": raw_dict.get("f") or raw_dict.get("form_id", "A"),
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
            "student_id": raw_dict.get("sid") or raw_dict.get("student_id"),
            "class_id": raw_dict.get("cid") or raw_dict.get("class_id"),
            "_raw": raw_dict,
            "_raw_text": raw_text,
        }
    except Exception:
        return {"raw": raw_text, "_raw_text": raw_text}


@router.get("/render")
def render_qr_code(
    data: Optional[str] = None,
    w: Optional[str] = None,
    f: Optional[str] = "A",
    s: Optional[int] = 42,
    c: Optional[int] = 6,
    sid: Optional[str] = None,
    cid: Optional[str] = None,
    fmt: str = "png",
    box_size: int = 8,
) -> Response:
    """Generate and return a high-contrast QR code image (PNG or SVG)."""
    if data:
        payload_str = data
    else:
        payload: Dict[str, Any] = {
            "w": w or "WS-PREVIEW",
            "f": f or "A",
            "s": s if s is not None else 42,
            "c": c if c is not None else 6,
        }
        if sid:
            payload["sid"] = sid
        if cid:
            payload["cid"] = cid
        payload_str = json.dumps(payload, separators=(",", ":"))

    if fmt.lower() == "svg":
        factory = qrcode.image.svg.SvgPathImage
        qr = qrcode.QRCode(
            version=1,
            error_correction=qr_constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=1,
            image_factory=factory,
        )
        qr.add_data(payload_str)
        qr.make(fit=True)
        img = qr.make_image()
        buf = io.BytesIO()
        img.save(buf)
        svg_bytes = buf.getvalue()
        return Response(content=svg_bytes, media_type="image/svg+xml")
    else:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qr_constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=1,
        )
        qr.add_data(payload_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, "PNG")
        png_bytes = buf.getvalue()
        return Response(content=png_bytes, media_type="image/png")


@router.post("/decode")
def decode_qr_image(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload an image to scan and decode its QR code using multi-pass
    computer vision.
    """
    image_bytes = file.file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(
            status_code=400, detail="Failed to decode image file"
        )

    metadata = multi_pass_decode_qr(img)
    if not metadata:
        return {
            "success": False,
            "error": "No QR code could be detected in image",
            "metadata": {},
        }

    return {
        "success": True,
        "metadata": metadata,
    }
