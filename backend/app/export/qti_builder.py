from __future__ import annotations

import io
import random
import uuid
import xml.etree.ElementTree as ET
import zipfile
from typing import List, Optional
from xml.dom import minidom

from backend.app.core.base import BaseProblem, ProblemDifficulty


class QTIBuilder:
    """Builds QTI 2.1 compliant XML assessments and Canvas-compatible
    ZIP archives.
    """

    def __init__(self) -> None:
        pass

    def build_qti_item_xml(
        self,
        problem: BaseProblem,
        item_index: int,
        points: float = 1.0,
        rng: Optional[random.Random] = None,
    ) -> ET.Element:
        """Create a single QTI 2.1 assessmentItem XML node for a
        multiple-choice math problem.
        """
        item_id = f"omf_{problem.id}_{item_index}"
        local_rng = rng or random.Random()

        # Combine correct answer and distractors into shuffled options
        options = [(problem.answer_typst, True, "correct_choice")]
        for idx, d in enumerate(problem.distractors):
            options.append((d, False, f"distractor_{idx}"))
        local_rng.shuffle(options)

        # Root assessmentItem
        item = ET.Element(
            "assessmentItem",
            {
                "xmlns": "http://www.imsglobal.org/xsd/imsqti_v2p1",
                "xmlns:xsi": (
                    "http://www.w3.org/2001/XMLSchema-instance"
                ),
                "xsi:schemaLocation": (
                    "http://www.imsglobal.org/xsd/imsqti_v2p1 "
                    "http://www.imsglobal.org/xsd/imsqti_v2p1.xsd"
                ),
                "identifier": item_id,
                "title": f"Question {item_index}: {problem.prompt_text}",
                "adaptive": "false",
                "timeDependent": "false",
            },
        )

        # Response declaration
        resp_decl = ET.SubElement(
            item,
            "responseDeclaration",
            {
                "identifier": "RESPONSE",
                "cardinality": "single",
                "baseType": "identifier",
            },
        )
        correct_resp = ET.SubElement(resp_decl, "correctResponse")
        correct_id = ""
        for _opt_text, is_correct, opt_id in options:
            if is_correct:
                correct_id = opt_id
                ET.SubElement(correct_resp, "value").text = opt_id

        # Mapping for points
        mapping = ET.SubElement(resp_decl, "mapping", {"defaultValue": "0"})
        ET.SubElement(
            mapping,
            "mapEntry",
            {"mapKey": correct_id, "mappedValue": str(points)},
        )

        # Outcome declaration (SCORE)
        out_decl = ET.SubElement(
            item,
            "outcomeDeclaration",
            {
                "identifier": "SCORE",
                "cardinality": "single",
                "baseType": "float",
            },
        )
        ET.SubElement(out_decl, "defaultValue").text = "0"

        # Item Body
        body = ET.SubElement(item, "itemBody")

        # Prompt & Equation
        prompt_p = ET.SubElement(body, "p")
        prompt_p.text = f"{problem.prompt_text}"

        math_p = ET.SubElement(
            body,
            "p",
            {"style": "font-size: 1.2em; font-weight: bold;"},
        )
        math_p.text = problem.equation_typst

        # Multiple choice interaction
        choice_int = ET.SubElement(
            body,
            "choiceInteraction",
            {
                "responseIdentifier": "RESPONSE",
                "shuffle": "false",
                "maxChoices": "1",
            },
        )

        for opt_text, _is_corr, opt_id in options:
            choice = ET.SubElement(
                choice_int,
                "simpleChoice",
                {"identifier": opt_id},
            )
            choice.text = opt_text

        # Response processing (standard match template)
        ET.SubElement(
            item,
            "responseProcessing",
            {
                "template": (
                    "http://www.imsglobal.org/question/qti_v2p1/"
                    "rptemplates/match_correct"
                )
            },
        )

        # Modal Feedback (Solution Steps)
        if problem.steps_typst:
            feedback = ET.SubElement(
                item,
                "modalFeedback",
                {
                    "outcomeIdentifier": "FEEDBACK",
                    "identifier": "SOLUTION",
                    "showHide": "show",
                },
            )
            fb_h = ET.SubElement(feedback, "h4")
            fb_h.text = "Step-by-Step Solution:"
            fb_ol = ET.SubElement(feedback, "ol")
            for step in problem.steps_typst:
                li = ET.SubElement(fb_ol, "li")
                li.text = step

        return item

    def build_manifest_xml(self, quiz_id: str, quiz_title: str) -> str:
        """Create IMS Manifest XML for Canvas / LMS package."""
        manifest = ET.Element(
            "manifest",
            {
                "identifier": f"manifest_{quiz_id}",
                "xmlns": "http://www.imsproject.org/xsd/imscp_rootv1p1p2",
                "xmlns:imsmd": "http://www.imsglobal.org/xsd/imsmd_v1p2",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            },
        )
        metadata = ET.SubElement(manifest, "metadata")
        schema = ET.SubElement(metadata, "schema")
        schema.text = "IMS Content"
        schema_ver = ET.SubElement(metadata, "schemaversion")
        schema_ver.text = "1.1.3"

        resources = ET.SubElement(manifest, "resources")
        res = ET.SubElement(
            resources,
            "resource",
            {
                "identifier": f"resource_{quiz_id}",
                "type": "imsqti_test_xmlv2p1",
                "href": "assessment_qti.xml",
            },
        )
        ET.SubElement(res, "file", {"href": "assessment_qti.xml"})
        ET.SubElement(res, "file", {"href": "assessment_meta.xml"})

        return self._prettify_xml(manifest)

    def build_assessment_meta_xml(
        self, quiz_id: str, quiz_title: str, problem_count: int
    ) -> str:
        """Create Canvas assessment_meta.xml configuration."""
        root = ET.Element(
            "quiz",
            {
                "identifier": quiz_id,
                "xmlns": "http://canvas.instructure.com/xsd/cccv1p0",
            },
        )
        ET.SubElement(root, "title").text = quiz_title
        desc = (
            "<p>Procedurally generated assessment produced by "
            f"OpenMathForge. Total questions: {problem_count}.</p>"
        )
        ET.SubElement(root, "description").text = desc
        ET.SubElement(root, "quiz_type").text = "assignment"
        ET.SubElement(root, "points_possible").text = str(float(problem_count))
        ET.SubElement(root, "shuffle_answers").text = "true"
        ET.SubElement(root, "scoring_policy").text = "keep_highest"
        ET.SubElement(root, "allowed_attempts").text = "1"
        return self._prettify_xml(root)

    def build_assessment_qti_xml(
        self,
        quiz_id: str,
        quiz_title: str,
        problems: List[BaseProblem],
    ) -> str:
        """Create QTI assessment document containing all items."""
        root = ET.Element(
            "assessmentTest",
            {
                "xmlns": "http://www.imsglobal.org/xsd/imsqti_v2p1",
                "identifier": quiz_id,
                "title": quiz_title,
            },
        )
        part = ET.SubElement(
            root,
            "testPart",
            {
                "identifier": "part_1",
                "navigationMode": "linear",
                "submissionMode": "individual",
            },
        )
        section = ET.SubElement(
            part,
            "assessmentSection",
            {
                "identifier": "section_1",
                "title": "Main Questions",
                "visible": "true",
            },
        )

        # Point allocation by difficulty
        diff_weights = {
            ProblemDifficulty.MILD: 1.0,
            ProblemDifficulty.MEDIUM: 2.0,
            ProblemDifficulty.SPICY: 3.0,
        }

        for idx, prob in enumerate(problems, start=1):
            pts = diff_weights.get(prob.difficulty, 1.0)
            item_node = self.build_qti_item_xml(prob, idx, points=pts)
            section.append(item_node)

        return self._prettify_xml(root)

    def create_canvas_zip(
        self,
        quiz_title: str,
        problems: List[BaseProblem],
        quiz_id: Optional[str] = None,
    ) -> bytes:
        """Package QTI 2.1 quiz XML, manifest, and meta XML into a
        Canvas-ready ZIP archive.
        """
        qid = quiz_id or f"omf_{uuid.uuid4().hex[:8]}"

        manifest_xml = self.build_manifest_xml(qid, quiz_title)
        meta_xml = self.build_assessment_meta_xml(
            qid, quiz_title, len(problems)
        )
        qti_xml = self.build_assessment_qti_xml(qid, quiz_title, problems)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("imsmanifest.xml", manifest_xml)
            zf.writestr("assessment_meta.xml", meta_xml)
            zf.writestr("assessment_qti.xml", qti_xml)

        return zip_buffer.getvalue()

    def _prettify_xml(self, elem: ET.Element) -> str:
        """Return pretty-printed XML string."""
        raw_str = ET.tostring(elem, encoding="utf-8")
        parsed = minidom.parseString(raw_str)
        return (
            parsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
        )
