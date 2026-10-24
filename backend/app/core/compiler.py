from __future__ import annotations

import json
import pathlib
import shutil
import tempfile
from typing import Any, Dict, List, Optional
import cv2
import jinja2
import qrcode
import qrcode.constants as qr_constants
import typst

from backend.app.core.base import BaseProblem


TEMPLATE_DIR = pathlib.Path(__file__).parent.parent / "templates"
STATIC_ASSETS_DIR = pathlib.Path(__file__).parent.parent / "static" / "markers"


def ensure_aruco_markers() -> Dict[int, pathlib.Path]:
    """Generate and cache canonical 4x4 ArUco markers for the 4 corners."""
    STATIC_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    marker_paths: Dict[int, pathlib.Path] = {}

    for marker_id in [0, 1, 2, 3]:
        file_path = STATIC_ASSETS_DIR / f"aruco_{marker_id}.png"
        if not file_path.exists():
            img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, 200)
            cv2.imwrite(str(file_path), img)
        marker_paths[marker_id] = file_path

    return marker_paths


def generate_qr_code(
    payload: Dict[str, Any], output_path: pathlib.Path
) -> pathlib.Path:
    """Generate a high-contrast QR code image encoding worksheet metadata."""
    qr_data = json.dumps(payload, separators=(",", ":"))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qr_constants.ERROR_CORRECT_M,
        box_size=8,
        border=1,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    with open(output_path, "wb") as f:
        img.save(f)
    return output_path


class TypstCompiler:
    """High performance Typst template compiler with anti-cheating ArUco
    fiducials and QR tracking.
    """

    def __init__(self, template_dir: Optional[pathlib.Path] = None) -> None:
        self.template_dir = template_dir or TEMPLATE_DIR
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.marker_paths = ensure_aruco_markers()

    def render_worksheet_typ(
        self,
        title: str,
        form_id: str,
        worksheet_id: str,
        seed: int,
        problems: List[BaseProblem],
        marker_filenames: Dict[int, str],
        qr_filename: str,
        columns: int = 2,
        student_name: Optional[str] = None,
        student_id: Optional[str] = None,
        student_period: Optional[str] = None,
    ) -> str:
        """Render the Typst markup for a student worksheet."""
        template = self.jinja_env.get_template("worksheet.typ.j2")

        mild_problems = [p for p in problems if p.difficulty == "mild"]
        medium_problems = [p for p in problems if p.difficulty == "medium"]
        spicy_problems = [p for p in problems if p.difficulty == "spicy"]

        # Dynamic workspace height with extra clearance for multi-step
        has_multistep = any(
            "multi" in (p.prompt_text or "").lower() or len(p.steps_typst) >= 4
            for p in problems
        )
        total_rows = max(1, (len(problems) + columns - 1) // columns)
        if has_multistep or total_rows <= 3:
            effective_rows = min(total_rows, 3)
            box_height_pt = max(
                150, min(270, int(580 / max(1, effective_rows)))
            )
        else:
            box_height_pt = max(110, min(240, int(580 / max(1, total_rows))))

        context = {
            "title": title,
            "form_id": form_id,
            "worksheet_id": worksheet_id,
            "seed": seed,
            "problems": problems,
            "mild_problems": mild_problems,
            "medium_problems": medium_problems,
            "spicy_problems": spicy_problems,
            "marker_top_left": marker_filenames[0],
            "marker_top_right": marker_filenames[1],
            "marker_bottom_right": marker_filenames[2],
            "marker_bottom_left": marker_filenames[3],
            "qr_path": qr_filename,
            "box_height_pt": box_height_pt,
            "columns": columns,
            "student_name": student_name,
            "student_id": student_id,
            "student_period": student_period,
        }
        return template.render(context)

    def render_matrix_key_typ(
        self,
        title: str,
        worksheet_id: str,
        forms_data: Dict[str, List[BaseProblem]],
    ) -> str:
        """Render the 4-column Master Grading Matrix aligning Forms A-D."""
        template = self.jinja_env.get_template("matrix_key.typ.j2")

        first_form = next(iter(forms_data.values()))
        problem_indices = list(range(1, len(first_form) + 1))

        rows: List[Dict[str, Any]] = []
        for idx in problem_indices:
            row: Dict[str, Any] = {"index": idx}
            for form_id in ["A", "B", "C", "D"]:
                if (
                    form_id in forms_data
                    and idx - 1 < len(forms_data[form_id])
                ):
                    prob = forms_data[form_id][idx - 1]
                    diff_val = (
                        prob.difficulty.value
                        if hasattr(prob.difficulty, "value")
                        else prob.difficulty
                    )
                    row[form_id] = {
                        "equation": prob.equation_typst,
                        "answer": prob.answer_typst,
                        "difficulty": diff_val,
                    }
                else:
                    row[form_id] = {
                        "equation": "-",
                        "answer": "-",
                        "difficulty": "-",
                    }
            rows.append(row)

        context = {
            "title": title,
            "worksheet_id": worksheet_id,
            "rows": rows,
            "form_ids": ["A", "B", "C", "D"],
        }
        return template.render(context)

    def compile_worksheet_pdf(
        self,
        title: str,
        form_id: str,
        worksheet_id: str,
        seed: int,
        problems: List[BaseProblem],
        columns: int = 2,
        show_answers: bool = False,
        student_name: Optional[str] = None,
        student_id: Optional[str] = None,
        student_period: Optional[str] = None,
        class_id: Optional[str] = None,
    ) -> bytes:
        """End-to-end worksheet generation with QR + ArUco markers."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = pathlib.Path(tmp_dir)

            # Copy markers to temp dir
            marker_filenames: Dict[int, str] = {}
            for m_id, m_path in self.marker_paths.items():
                dest = tmp_path / f"aruco_{m_id}.png"
                shutil.copyfile(m_path, dest)
                marker_filenames[m_id] = f"aruco_{m_id}.png"

            # Generate QR code with student and class tracking
            anon_sid = student_id or "anon"
            qr_filename = f"qr_{worksheet_id}_{form_id}_{anon_sid}.png"
            payload: Dict[str, Any] = {
                "w": worksheet_id,
                "f": form_id,
                "s": seed,
                "c": len(problems),
            }
            if student_id:
                payload["sid"] = student_id
            if class_id:
                payload["cid"] = class_id

            generate_qr_code(payload, tmp_path / qr_filename)

            typ_markup = self.render_worksheet_typ(
                title=title,
                form_id=form_id,
                worksheet_id=worksheet_id,
                seed=seed,
                problems=problems,
                marker_filenames=marker_filenames,
                qr_filename=qr_filename,
                columns=columns,
                student_name=student_name,
                student_id=student_id,
                student_period=student_period,
            )

            source_file = tmp_path / "worksheet.typ"
            source_file.write_text(typ_markup, encoding="utf-8")

            return typst.compile(source_file)

    def compile_class_batch_pdf(
        self,
        title: str,
        form_id: str,
        worksheet_id: str,
        seed: int,
        problems: List[BaseProblem],
        students: List[Dict[str, Any]],
        class_id: str,
        columns: int = 2,
    ) -> bytes:
        """Generate bundled PDF with a personalized page per student."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = pathlib.Path(tmp_dir)

            marker_filenames: Dict[int, str] = {}
            for m_id, m_path in self.marker_paths.items():
                dest = tmp_path / f"aruco_{m_id}.png"
                shutil.copyfile(m_path, dest)
                marker_filenames[m_id] = f"aruco_{m_id}.png"

            page_markups: List[str] = []

            for s_idx, stu in enumerate(students):
                s_id = stu.get("student_id", f"S{s_idx:04d}")
                fn = stu.get("first_name", "")
                ln = stu.get("last_name", "")
                raw_name = f"{fn} {ln}".strip()
                s_name = stu.get("name") or raw_name
                s_period = stu.get("period", "1")

                qr_filename = f"qr_batch_{worksheet_id}_{s_id}.png"
                payload = {
                    "w": worksheet_id,
                    "f": form_id,
                    "s": seed,
                    "c": len(problems),
                    "sid": s_id,
                    "cid": class_id,
                }
                generate_qr_code(payload, tmp_path / qr_filename)

                markup = self.render_worksheet_typ(
                    title=title,
                    form_id=form_id,
                    worksheet_id=worksheet_id,
                    seed=seed,
                    problems=problems,
                    marker_filenames=marker_filenames,
                    qr_filename=qr_filename,
                    columns=columns,
                    student_name=s_name,
                    student_id=s_id,
                    student_period=s_period,
                )
                page_markups.append(markup)

            combined_markup = "\n#pagebreak()\n".join(page_markups)

            source_file = tmp_path / "class_batch.typ"
            source_file.write_text(combined_markup, encoding="utf-8")

            return typst.compile(source_file)

    def compile_matrix_key_pdf(
        self,
        title: str,
        worksheet_id: str,
        forms_data: Dict[str, List[BaseProblem]],
    ) -> bytes:
        """Compile Master Grading Matrix PDF."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = pathlib.Path(tmp_dir)
            typ_markup = self.render_matrix_key_typ(
                title=title,
                worksheet_id=worksheet_id,
                forms_data=forms_data,
            )
            source_file = tmp_path / "matrix.typ"
            source_file.write_text(typ_markup, encoding="utf-8")
            return typst.compile(source_file)
