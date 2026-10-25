from __future__ import annotations

import io
import pathlib
import tempfile
import pytest
from starlette.datastructures import UploadFile
from fastapi import HTTPException

from backend.app.api.multitenant_routes import (
    get_tenant_worksheets,
    get_tenant_rosters,
    verify_tenant_authorization,
    heavy_endpoint_limiter,
)
from backend.app.api.routes import grade_upload
from backend.app.core.privacy import (
    hash_student_identifier,
    anonymize_student_record,
    purge_ephemeral_storage,
)
from backend.app.grading.verifier import CASStepVerifier
from backend.app.core.rate_limiter import TokenBucketRateLimiter


class TestSecurityAndGovernance:
    """Multi-tenant isolation, FERPA/COPPA student data lifecycle, adversarial hardening, and rate limiting."""

    def test_multi_tenant_isolation_and_idor_defense(self) -> None:
        """Teacher A cannot access Teacher B's worksheets or rosters (BOLA/IDOR Defense)."""
        # 1. Teacher A accessing own worksheets -> 200 OK
        data_a = get_tenant_worksheets("teacher_a", x_teacher_id="teacher_a")
        assert data_a["teacher_id"] == "teacher_a"
        assert len(data_a["worksheets"]) >= 1

        # 2. Teacher A attempting to access Teacher B's worksheets -> 403 Forbidden
        with pytest.raises(HTTPException) as exc_info:
            get_tenant_worksheets("teacher_b", x_teacher_id="teacher_a")
        assert exc_info.value.status_code == 403
        assert "Forbidden" in exc_info.value.detail

        # 3. Teacher A attempting to access Teacher B's roster -> 403 Forbidden
        with pytest.raises(HTTPException) as exc_info:
            get_tenant_rosters("teacher_b", x_teacher_id="teacher_a")
        assert exc_info.value.status_code == 403

        # 4. Bearer token auth mismatch -> 403 Forbidden
        with pytest.raises(HTTPException) as exc_info:
            get_tenant_worksheets("teacher_b", authorization="Bearer teacher_a")
        assert exc_info.value.status_code == 403

        # 5. Non-existent tenant -> 404 Not Found
        with pytest.raises(HTTPException) as exc_info:
            get_tenant_worksheets("teacher_nonexistent", x_teacher_id="teacher_nonexistent")
        assert exc_info.value.status_code == 404

        # 6. Unauthenticated request -> 403 Forbidden
        with pytest.raises(HTTPException) as exc_info:
            get_tenant_worksheets("teacher_a", x_teacher_id=None, authorization=None)
        assert exc_info.value.status_code == 403

    def test_ferpa_coppa_privacy_and_ephemeral_lifecycle(self) -> None:
        """Verify student PII hashing and ephemeral temporary storage purge routine."""
        raw_id = "stu_10928_secure"
        raw_name = "Jane Elizabeth Doe"

        # 1. Cryptographic hashing
        hashed_id = hash_student_identifier(raw_id)
        assert hashed_id != raw_id
        assert len(hashed_id) == 16
        # Deterministic HMAC
        assert hash_student_identifier(raw_id) == hashed_id

        # 2. Student record anonymization
        anon = anonymize_student_record(raw_id, raw_name)
        assert anon["hashed_student_id"] == hashed_id
        assert "Jane" not in anon["masked_name"]
        assert "J. Doe" in anon["masked_name"]

        # 3. Ephemeral TTL storage purge
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = pathlib.Path(tmp_dir)
            f1 = tmp_path / "grading_scan_01.png"
            f2 = tmp_path / "crop_prob_02.png"
            f1.write_bytes(b"temp_scan_data")
            f2.write_bytes(b"temp_crop_data")

            # With TTL=0, all files should be purged
            purged = purge_ephemeral_storage(tmp_path, max_age_seconds=0)
            assert purged == 2
            assert not f1.exists()
            assert not f2.exists()

    def test_adversarial_file_uploads(self) -> None:
        """Reject path traversal filenames, pixel bombs, and non-image polyglot payloads."""
        # 1. Directory traversal filename
        fake_image = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc\xf8\xff\x9f\x01\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82"
        f_traversal = UploadFile(filename="../../etc/passwd.png", file=io.BytesIO(fake_image))
        with pytest.raises(HTTPException) as exc_info:
            grade_upload(f_traversal)
        assert exc_info.value.status_code == 400
        assert "Directory traversal" in exc_info.value.detail

        # 2. Non-image polyglot / executable bytes
        f_poly = UploadFile(filename="sample.png", file=io.BytesIO(b"MZ\x90\x00\x03fake_executable"))
        with pytest.raises(HTTPException) as exc_info:
            grade_upload(f_poly)
        assert exc_info.value.status_code == 400

        # 3. Truncated byte stream
        f_trunc = UploadFile(filename="tiny.png", file=io.BytesIO(b"\x89PNG"))
        with pytest.raises(HTTPException) as exc_info:
            grade_upload(f_trunc)
        assert exc_info.value.status_code == 400

    def test_sympy_code_injection_hardening(self) -> None:
        """Arbitrary Python code injection in formula fields must be completely rejected."""
        verifier = CASStepVerifier()

        payloads = [
            "__import__('os').system('id')",
            "eval('2 + 2')",
            "exec('import sys; sys.exit(1)')",
            "open('/etc/passwd', 'r').read()",
            "subprocess.Popen(['whoami'])",
            "globals()['__builtins__']",
            "os.system('rm -rf /')",
        ]

        for p in payloads:
            with pytest.raises(ValueError) as excinfo:
                verifier.parse_latex_to_sympy(p)
            assert "Prohibited code pattern detected" in str(excinfo.value)

    def test_dos_and_token_bucket_rate_limiting(self) -> None:
        """Rapid bursts on CPU-heavy routes trigger HTTP 429 Too Many Requests."""
        limiter = TokenBucketRateLimiter(capacity=3, refill_rate_per_sec=1.0)
        client_key = "192.168.1.100"

        # First 3 allowed
        assert limiter.check_rate_limit(client_key) is True
        assert limiter.check_rate_limit(client_key) is True
        assert limiter.check_rate_limit(client_key) is True

        # 4th in same second is rate-limited
        assert limiter.check_rate_limit(client_key) is False

        # End-to-end token bucket rate limiter
        heavy_endpoint_limiter.reset()
        for _ in range(10):
            assert heavy_endpoint_limiter.check_rate_limit("client_test") is True

        # 11th request exceeds token bucket capacity
        assert heavy_endpoint_limiter.check_rate_limit("client_test") is False
