from __future__ import annotations

import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RosterFormat(str, Enum):
    GOOGLE_CLASSROOM = "google_classroom"
    CANVAS_SIS = "canvas_sis"
    CLEVER = "clever"
    ONEROSTER = "oneroster"
    GENERIC_CSV = "generic_csv"


class Student(BaseModel):
    id: str = Field(..., description="Unique internal student ID")
    student_id: str = Field(..., description="School/SIS Student ID (e.g., S10482)")
    first_name: str
    last_name: str
    email: Optional[str] = None
    period: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


class Classroom(BaseModel):
    id: str = Field(..., description="Unique class ID (e.g., class_alg1_p2)")
    name: str = Field(..., description="Class name (e.g., Algebra 1 - Period 2)")
    subject: str = Field(default="Algebra 1")
    period: str = Field(default="1")
    teacher_name: str = Field(default="Teacher")
    students: List[Student] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


class StudentSubmission(BaseModel):
    submission_id: str
    worksheet_id: str
    class_id: str
    student_id: str
    student_name: str
    form_id: str
    submitted_at: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    total_problems: int
    correct_count: int
    score_percentage: float
    error_types: List[str] = Field(default_factory=list)
    is_verified: bool = True
    raw_qr_data: Dict[str, Any] = Field(default_factory=dict)

