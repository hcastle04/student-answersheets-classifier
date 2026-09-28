from pathlib import Path

from answer_classifier.student_repository import (
    load_students,
    parse_student_folder_name,
)

def test_parse_student_folder_name_without_school():
    name, school = parse_student_folder_name("김주훈")

    assert name == "김주훈"
    assert school is None


def test_parse_student_folder_name_with_school():
    name, school = parse_student_folder_name(
        "민윤기(달천고)"
    )

    assert name == "민윤기"
    assert school == "달천고"


def test_parse_student_folder_name_strips_whitespace():
    name, school = parse_student_folder_name(
        "  민윤기(달천고)  "
    )

    assert name == "민윤기"
    assert school == "달천고"


def test_load_students_from_directories(tmp_path: Path):
    (tmp_path / "김민수").mkdir()
    (tmp_path / "이영희").mkdir()

    students = load_students(tmp_path)

    assert len(students) == 2

    student_map = {
        student.folder_name: student
        for student in students
    }

    assert student_map["김민수"].name == "김민수"
    assert student_map["김민수"].school is None
    assert student_map["김민수"].folder_name == "김민수"

    assert student_map["이영희"].name == "이영희"
    assert student_map["이영희"].school is None
    assert student_map["이영희"].folder_name == "이영희"


def test_load_students_parses_student_folder_names(
    tmp_path: Path,
):
    student_root = tmp_path / "S반"

    (student_root / "김주훈").mkdir(parents=True)
    (student_root / "민윤기(달천고)").mkdir()
    (student_root / "민윤기(압구정고)").mkdir()

    students = load_students(student_root)

    assert len(students) == 3

    student_map = {
        student.folder_name: student
        for student in students
    }

    assert student_map["김주훈"].name == "김주훈"
    assert student_map["김주훈"].school is None
    assert student_map["김주훈"].folder_name == "김주훈"

    assert student_map["민윤기(달천고)"].name == "민윤기"
    assert student_map["민윤기(달천고)"].school == "달천고"
    assert (
        student_map["민윤기(달천고)"].folder_name
        == "민윤기(달천고)"
    )

    assert student_map["민윤기(압구정고)"].name == "민윤기"
    assert student_map["민윤기(압구정고)"].school == "압구정고"
    assert (
        student_map["민윤기(압구정고)"].folder_name
        == "민윤기(압구정고)"
    )


def test_ignore_system_directories(tmp_path: Path):
    (tmp_path / "김민수").mkdir()
    (tmp_path / "보류").mkdir()
    (tmp_path / "신규생").mkdir()
    (tmp_path / "review").mkdir()
    (tmp_path / "new_student").mkdir()

    students = load_students(tmp_path)

    assert len(students) == 1
    assert students[0].name == "김민수"
    assert students[0].school is None
    assert students[0].folder_name == "김민수"


def test_missing_directory_returns_empty_list(tmp_path: Path):
    missing = tmp_path / "없는폴더"

    students = load_students(missing)

    assert students == []