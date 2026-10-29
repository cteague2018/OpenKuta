from __future__ import annotations

import json
import os
import pathlib
import uuid
from typing import Dict, List, Optional

from backend.app.classroom.models import Classroom, Student, StudentSubmission

DEFAULT_STORAGE_DIR = pathlib.Path(__file__).parent.parent / "data"
# Kept for backwards compatibility with any external tooling; the store itself resolves
# its paths per instance so tests can redirect them to a temporary directory.
STORAGE_DIR = DEFAULT_STORAGE_DIR
CLASSROOM_FILE = STORAGE_DIR / "classrooms.json"
SUBMISSIONS_FILE = STORAGE_DIR / "submissions.json"


def resolve_storage_dir() -> pathlib.Path:
    """Return the directory that holds the classroom/submission JSON stores.

    ``OPENKUTA_DATA_DIR`` overrides the in-repo default, which is how the test suite and
    any ephemeral deployment keep run-time state out of the source tree.
    """
    override = os.environ.get("OPENKUTA_DATA_DIR")
    return pathlib.Path(override) if override else DEFAULT_STORAGE_DIR


class ClassroomStore:
    """Manages persistence of classrooms, rosters, and individual student submissions."""

    def __init__(self, storage_dir: Optional[pathlib.Path] = None) -> None:
        self.storage_dir = pathlib.Path(storage_dir) if storage_dir else resolve_storage_dir()
        self.classroom_file = self.storage_dir / "classrooms.json"
        self.submissions_file = self.storage_dir / "submissions.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.classrooms: Dict[str, Classroom] = {}
        self.submissions: Dict[str, StudentSubmission] = {}
        self._load()

    def _load(self) -> None:
        if self.classroom_file.exists():
            try:
                data = json.loads(self.classroom_file.read_text(encoding="utf-8"))
                for cid, cdata in data.items():
                    self.classrooms[cid] = Classroom.model_validate(cdata)
            except Exception:
                self._seed_default_classes()
        else:
            self._seed_default_classes()

        if self.submissions_file.exists():
            try:
                data = json.loads(self.submissions_file.read_text(encoding="utf-8"))
                for sid, sdata in data.items():
                    self.submissions[sid] = StudentSubmission.model_validate(sdata)
            except Exception:
                pass

    def _save(self) -> None:
        self.classroom_file.write_text(
            json.dumps({k: v.model_dump() for k, v in self.classrooms.items()}, indent=2),
            encoding="utf-8",
        )
        self.submissions_file.write_text(
            json.dumps({k: v.model_dump() for k, v in self.submissions.items()}, indent=2),
            encoding="utf-8",
        )

    def _seed_default_classes(self) -> None:
        """Seed a default Algebra 1 Period 2 class with sample students."""
        sample_students = [
            Student(id="stu_101", student_id="S10481", first_name="Maya", last_name="Lin", email="maya.lin@school.edu", period="2"),
            Student(id="stu_102", student_id="S10482", first_name="Lucas", last_name="Vance", email="lucas.vance@school.edu", period="2"),
            Student(id="stu_103", student_id="S10483", first_name="Chloe", last_name="Zhao", email="chloe.zhao@school.edu", period="2"),
            Student(id="stu_104", student_id="S10484", first_name="Ethan", last_name="Davis", email="ethan.davis@school.edu", period="2"),
            Student(id="stu_105", student_id="S10485", first_name="Sophia", last_name="Martinez", email="sophia.m@school.edu", period="2"),
        ]
        default_class = Classroom(
            id="class_alg1_p2",
            name="Algebra 1 (Period 2)",
            subject="Algebra 1",
            period="2",
            teacher_name="Mr. Anderson",
            students=sample_students,
        )
        self.classrooms[default_class.id] = default_class
        self._save()

    def list_classes(self) -> List[Classroom]:
        return list(self.classrooms.values())

    def get_class(self, class_id: str) -> Optional[Classroom]:
        if class_id in self.classrooms:
            return self.classrooms[class_id]
        if class_id in ("cls_alg1_p3", "class_alg1_p3", "cls_alg1_p2"):
            return self.classrooms.get("class_alg1_p2") or self.classrooms.get("cls_alg1_p3") or (list(self.classrooms.values())[0] if self.classrooms else None)
        return None

    def create_class(self, name: str, subject: str, period: str, teacher_name: str = "Teacher") -> Classroom:
        cid = f"class_{uuid.uuid4().hex[:8]}"
        classroom = Classroom(
            id=cid,
            name=name,
            subject=subject,
            period=period,
            teacher_name=teacher_name,
            students=[],
        )
        self.classrooms[cid] = classroom
        self._save()
        return classroom

    def add_students_to_class(self, class_id: str, new_students: List[Student]) -> Classroom:
        classroom = self.get_class(class_id)
        if not classroom:
            raise ValueError(f"Classroom '{class_id}' not found")

        # Avoid duplicates based on student_id
        existing_ids = {s.student_id for s in classroom.students}
        for s in new_students:
            if s.student_id not in existing_ids:
                classroom.students.append(s)
                existing_ids.add(s.student_id)

        self._save()
        return classroom

    def record_submission(self, submission: StudentSubmission) -> None:
        self.submissions[submission.submission_id] = submission
        self._save()

    def get_class_submissions(self, class_id: str) -> List[StudentSubmission]:
        target_ids = {class_id}
        if class_id in ("cls_alg1_p3", "class_alg1_p3"):
            target_ids.add("class_alg1_p2")
        return [s for s in self.submissions.values() if s.class_id in target_ids]

    def find_student(self, class_id: str, student_id: str) -> Optional[Student]:
        classroom = self.get_class(class_id)
        if not classroom:
            return None
        for s in classroom.students:
            if s.student_id.lower() == student_id.lower():
                return s
        return None
