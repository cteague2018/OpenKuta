from __future__ import annotations

import csv
import io
import uuid
from typing import List, Tuple

from backend.app.classroom.models import RosterFormat, Student


class RosterParser:
    """Auto-detects and parses classroom roster CSV files from Google Classroom, Canvas, Clever, OneRoster, or generic CSV."""

    @staticmethod
    def detect_format(headers: List[str]) -> RosterFormat:
        h_lower = [h.strip().lower() for h in headers]
        h_str = " ".join(h_lower)

        if "sis user id" in h_str or "sis login id" in h_str or ("student" in h_lower and "id" in h_lower and "section" in h_lower):
            return RosterFormat.CANVAS_SIS
        elif "student name" in h_str and "email address" in h_str:
            return RosterFormat.GOOGLE_CLASSROOM
        elif "givenname" in h_lower and "familyname" in h_lower:
            if "role" in h_lower:
                return RosterFormat.ONEROSTER
            return RosterFormat.CLEVER
        else:
            return RosterFormat.GENERIC_CSV

    @classmethod
    def parse_csv(cls, csv_content: str | bytes, default_period: str = "1") -> Tuple[List[Student], RosterFormat]:
        if isinstance(csv_content, bytes):
            # Try utf-8 or utf-8-sig (handles Excel BOM)
            try:
                text = csv_content.decode("utf-8-sig")
            except Exception:
                text = csv_content.decode("latin-1")
        else:
            text = csv_content

        f = io.StringIO(text.strip())
        reader = csv.reader(f)

        rows = [r for r in reader if r and any(cell.strip() for cell in r)]
        if not rows:
            return [], RosterFormat.GENERIC_CSV

        header_row = rows[0]
        fmt = cls.detect_format(header_row)
        header_map = {col.strip().lower(): idx for idx, col in enumerate(header_row)}

        students: List[Student] = []

        for row_idx, row in enumerate(rows[1:], start=1):
            if not row or len(row) == 0:
                continue

            def get_val(key_candidates: List[str], current_row: List[str] = row) -> str:
                for k in key_candidates:
                    if k in header_map and header_map[k] < len(current_row):
                        v = current_row[header_map[k]].strip()
                        if v:
                            return v
                return ""

            first_name = ""
            last_name = ""
            student_id = ""
            email = ""
            period = default_period

            if fmt == RosterFormat.CANVAS_SIS:
                # Canvas format usually has "Student" as "LastName, FirstName"
                full_name = get_val(["student", "name"])
                if "," in full_name:
                    parts = full_name.split(",", 1)
                    last_name = parts[0].strip()
                    first_name = parts[1].strip()
                else:
                    parts = full_name.split()
                    first_name = parts[0] if parts else f"Student_{row_idx}"
                    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

                student_id = get_val(["sis user id", "id", "sis login id"]) or f"CANV_{row_idx:04d}"
                email = get_val(["sis login id", "email", "login id"])
                period = get_val(["section", "period"]) or default_period

            elif fmt == RosterFormat.GOOGLE_CLASSROOM:
                full_name = get_val(["student name", "name"])
                parts = full_name.split()
                first_name = parts[0] if parts else f"Student_{row_idx}"
                last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

                student_id = get_val(["student id", "id", "identifier"]) or f"GC_{row_idx:04d}"
                email = get_val(["email address", "email"])
                period = get_val(["period", "section"]) or default_period

            elif fmt in (RosterFormat.CLEVER, RosterFormat.ONEROSTER):
                first_name = get_val(["givenname", "first_name", "first name"])
                last_name = get_val(["familyname", "last_name", "last name"])
                student_id = get_val(["student_number", "identifier", "sourcedid", "id"]) or f"SIS_{row_idx:04d}"
                email = get_val(["email", "username"])
                period = get_val(["period", "sectionid", "section"]) or default_period

            else:
                # Generic CSV
                first_name = get_val(["first_name", "firstname", "first", "fname"])
                last_name = get_val(["last_name", "lastname", "last", "lname"])
                if not first_name and not last_name:
                    full_name = get_val(["name", "student_name", "student"])
                    if "," in full_name:
                        parts = full_name.split(",", 1)
                        last_name = parts[0].strip()
                        first_name = parts[1].strip()
                    else:
                        parts = full_name.split()
                        first_name = parts[0] if parts else f"Student_{row_idx}"
                        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

                student_id = get_val(["student_id", "id", "studentid", "student number", "identifier"]) or f"STU_{row_idx:04d}"
                email = get_val(["email", "email_address", "mail"])
                period = get_val(["period", "section", "class_period", "hour"]) or default_period

            if not first_name:
                first_name = f"Student_{row_idx}"

            students.append(
                Student(
                    id=f"stu_{uuid.uuid4().hex[:8]}",
                    student_id=student_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email if "@" in email else None,
                    period=period,
                )
            )

        return students, fmt
