from pathlib import Path

import pytest

from answer_classifier.input_parser import parse_input_context


def test_parse_s_class():
    context = parse_input_context(
        Path("2026-09-27_S반"),
        Path("학생별답안지"),
    )

    assert context.group_type == "S"
    assert context.student_root == Path("학생별답안지") / "S반"
    assert context.review_dir == Path("학생별답안지") / "S반" / "보류"
    assert context.school is None


def test_parse_y_class():
    context = parse_input_context(
        Path("2026-09-27_Y반"),
        Path("학생별답안지"),
    )

    assert context.group_type == "Y"
    assert context.student_root == Path("학생별답안지") / "Y반"
    assert context.review_dir == Path("학생별답안지") / "Y반" / "보류"
    assert context.school is None


def test_parse_special_school_with_underscore():
    context = parse_input_context(
        Path("2026-09-27_고려대"),
        Path("학생별답안지"),
    )

    assert context.group_type == "SPECIAL"
    assert context.school == "고려대"
    assert context.student_root == Path("학생별답안지") / "고려대"
    assert context.review_dir == Path("학생별답안지") / "고려대" / "보류"


def test_parse_special_school_with_hyphen():
    context = parse_input_context(
        Path("특강-연세대"),
        Path("학생별답안지"),
    )

    assert context.group_type == "SPECIAL"
    assert context.school == "연세대"


def test_parse_special_school_name():
    context = parse_input_context(
        Path("2026_성균관대_특강"),
        Path("학생별답안지"),
    )

    assert context.school == "성균관대"


def test_unknown_folder_raises_error():
    with pytest.raises(ValueError):
        parse_input_context(
            Path("2026-09-27_답안지"),
            Path("학생별답안지"),
        )