from pathlib import Path

import pytest

from answer_classifier.input_parser import parse_input_context

## 테스트케이스 
def test_parse_s_group(tmp_path: Path):
    input_dir = (
        tmp_path
        / "오T실전특강1회S일610(박정외T)_채점후"
    )
    answers_root = tmp_path / "학생별답안"

    context = parse_input_context(
        input_dir=input_dir,
        answers_root=answers_root,
    )

    assert context.group_type == "S"
    assert context.student_root == answers_root / "S반"
    assert context.review_dir == answers_root / "S반" / "보류"


def test_parse_y_group(tmp_path: Path):
    input_dir = (
        tmp_path
        / "오T실전특강1회Y금610(박종관T)_채점후"
    )
    answers_root = tmp_path / "학생별답안"

    context = parse_input_context(
        input_dir=input_dir,
        answers_root=answers_root,
    )

    assert context.group_type == "Y"
    assert context.student_root == answers_root / "Y반"
    assert context.review_dir == answers_root / "Y반" / "보류"

def test_parse_unknown_group_raises_error(tmp_path):
    input_dir = tmp_path / "알수없는폴더"
    answers_root = tmp_path / "학생별답안"

    with pytest.raises(ValueError):
        parse_input_context(
            input_dir=input_dir,
            answers_root=answers_root,
        )

def test_parse_later_practical_round(tmp_path: Path):
    input_dir = (
        tmp_path
        / "오T실전특강12회S토140(박정외T)_채점후"
    )
    answers_root = tmp_path / "학생별답안지"

    context = parse_input_context(
        input_dir=input_dir,
        answers_root=answers_root,
    )

    assert context.group_type == "S"


def test_unknown_folder_raises_error():
    with pytest.raises(ValueError):
        parse_input_context(
            Path("2026-09-27_답안지"),
            Path("학생별답안지"),
        )