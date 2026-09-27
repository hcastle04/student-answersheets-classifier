from pathlib import Path

from answer_classifier.student_repository import load_students


def test_load_students_from_directories(tmp_path: Path):
    (tmp_path / "김민수").mkdir()
    (tmp_path / "이영희").mkdir()

    students = load_students(tmp_path)

    assert len(students) == 2
    assert students[0].name == "김민수"
    assert students[1].name == "이영희"


def test_ignore_system_directories(tmp_path: Path):
    (tmp_path / "김민수").mkdir()
    (tmp_path / "보류").mkdir()

    students = load_students(tmp_path)

    assert len(students) == 1
    assert students[0].name == "김민수"


def test_assign_school_to_students(tmp_path: Path):
    (tmp_path / "김민수").mkdir()

    students = load_students(
        tmp_path,
        school="고려대",
    )

    assert len(students) == 1
    assert students[0].school == "고려대"


def test_missing_directory_returns_empty_list(tmp_path: Path):
    missing = tmp_path / "없는폴더"

    students = load_students(missing)

    assert students == []