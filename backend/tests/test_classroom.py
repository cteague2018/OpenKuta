from backend.app.classroom.models import RosterFormat
from backend.app.classroom.roster_parser import RosterParser
from backend.app.classroom.store import ClassroomStore
from backend.app.core.base import GeneratorConfig
from backend.app.core.compiler import TypstCompiler
from backend.app.generators.algebra_1.two_step_equations import TwoStepEquationsGenerator


def test_roster_parser_google_classroom():
    csv_text = """Student Name,Email Address,Student ID
Alice Walker,alice.w@school.edu,S1001
Bob Builder,bob.b@school.edu,S1002
Charlie Brown,charlie.b@school.edu,S1003"""

    students, fmt = RosterParser.parse_csv(csv_text, default_period="1")
    assert fmt == RosterFormat.GOOGLE_CLASSROOM
    assert len(students) == 3
    assert students[0].first_name == "Alice"
    assert students[0].last_name == "Walker"
    assert students[0].student_id == "S1001"
    assert students[0].email == "alice.w@school.edu"


def test_roster_parser_canvas_sis():
    csv_text = """Student,ID,SIS User ID,SIS Login ID,Section
"Johnson, Sarah",4821,SIS9921,sjohnson@district.org,Period 3
"Smith, Marcus",4822,SIS9922,msmith@district.org,Period 3"""

    students, fmt = RosterParser.parse_csv(csv_text, default_period="3")
    assert fmt == RosterFormat.CANVAS_SIS
    assert len(students) == 2
    assert students[0].first_name == "Sarah"
    assert students[0].last_name == "Johnson"
    assert students[0].student_id == "SIS9921"
    assert students[0].period == "Period 3"


def test_roster_parser_clever():
    csv_text = """sourcedId,givenName,familyName,email,student_number
clv_01,David,Copperfield,david@clever.com,D101
clv_02,Emma,Watson,emma@clever.com,E102"""

    students, fmt = RosterParser.parse_csv(csv_text)
    assert fmt == RosterFormat.CLEVER
    assert len(students) == 2
    assert students[0].first_name == "David"
    assert students[1].last_name == "Watson"


def test_classroom_store_and_batch_pdf():
    store = ClassroomStore()
    cls_obj = store.create_class(name="Geometry Period 4", subject="Geometry", period="4")
    assert cls_obj.name == "Geometry Period 4"

    students, _ = RosterParser.parse_csv("first_name,last_name,student_id\nLeo,Tolstoy,STU_1\nMark,Twain,STU_2")
    store.add_students_to_class(cls_obj.id, students)

    updated = store.get_class(cls_obj.id)
    assert updated is not None
    assert len(updated.students) == 2

    # Test batch class PDF compilation with personalized student QR codes
    gen = TwoStepEquationsGenerator()
    probs = gen.generate(GeneratorConfig(problem_count=4, seed=42))

    compiler = TypstCompiler()
    students_data = [
        {"student_id": s.student_id, "name": s.full_name, "period": s.period}
        for s in updated.students
    ]

    pdf_bytes = compiler.compile_class_batch_pdf(
        title="Pop Quiz 1",
        form_id="A",
        worksheet_id="WS-8888",
        seed=42,
        problems=probs,
        students=students_data,
        class_id=cls_obj.id,
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF-")
