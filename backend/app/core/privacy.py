from __future__ import annotations

import hashlib
import hmac
import pathlib
import time
from typing import Dict


def hash_student_identifier(student_id: str, salt: str = "openmathforge-ferpa-salt") -> str:
    """Cryptographically hash student identifier using HMAC-SHA256 for FERPA/COPPA compliance."""
    return hmac.new(salt.encode("utf-8"), student_id.encode("utf-8"), hashlib.sha256).hexdigest()[:16]


def anonymize_student_record(student_id: str, name: str) -> Dict[str, str]:
    """Return anonymized representation with hashed identifier and masked name."""
    hashed_id = hash_student_identifier(student_id)
    parts = name.strip().split()
    masked_name = f"{parts[0][0]}. {parts[-1]}" if len(parts) >= 2 else (parts[0][:2] + "***" if parts else "Anon")
    return {
        "hashed_student_id": hashed_id,
        "masked_name": masked_name,
    }


def purge_ephemeral_storage(storage_dir: pathlib.Path, max_age_seconds: float = 86400) -> int:
    """Hard-delete temporary grading scans, intermediate matrices, and rendered files older than TTL."""
    if not storage_dir.exists():
        return 0
    deleted_count = 0
    for path in storage_dir.glob("**/*"):
        if path.is_file():
            try:
                mtime = path.stat().st_mtime
                if (time.time() - mtime) >= (max_age_seconds - 0.05):
                    path.unlink()
                    deleted_count += 1
            except Exception:
                pass
    return deleted_count
