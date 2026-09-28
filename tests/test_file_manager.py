from pathlib import Path

import pytest

from answer_classifier.classifier import (
    ClassificationResult,
    ClassificationStatus,
    Student,
)
from answer_classifier.input_parser import InputContext
from answer_classifier.file_manager import (
    get_destination_dir,
    move_classified_pdf,
)

from answer_classifier.file_manager import (
    get_unique_destination,
    move_pdf,
)


def test_get_unique_destination_returns_original_when_file_does_not_exist(
    tmp_path: Path,
):
    destination = tmp_path / "answer.pdf"

    result = get_unique_destination(destination)

    assert result == destination


def test_get_unique_destination_adds_suffix_when_file_exists(
    tmp_path: Path,
):
    destination = tmp_path / "answer.pdf"
    destination.write_text("existing file")

    result = get_unique_destination(destination)

    assert result == tmp_path / "answer_1.pdf"


def test_get_unique_destination_increments_suffix(
    tmp_path: Path,
):
    (tmp_path / "answer.pdf").write_text("original")
    (tmp_path / "answer_1.pdf").write_text("duplicate")

    result = get_unique_destination(tmp_path / "answer.pdf")

    assert result == tmp_path / "answer_2.pdf"


def test_move_pdf_moves_file_to_destination(
    tmp_path: Path,
):
    source_dir = tmp_path / "input"
    destination_dir = tmp_path / "student"

    source_dir.mkdir()

    source = source_dir / "answer.pdf"
    source.write_text("test pdf")

    result = move_pdf(source, destination_dir)

    assert result == destination_dir / "answer.pdf"
    assert result.exists()
    assert not source.exists()


def test_move_pdf_does_not_overwrite_existing_file(
    tmp_path: Path,
):
    source_dir = tmp_path / "input"
    destination_dir = tmp_path / "student"

    source_dir.mkdir()
    destination_dir.mkdir()

    source = source_dir / "answer.pdf"
    source.write_text("new answer")

    existing = destination_dir / "answer.pdf"
    existing.write_text("existing answer")

    result = move_pdf(source, destination_dir)

    assert result == destination_dir / "answer_1.pdf"
    assert existing.read_text() == "existing answer"
    assert result.read_text() == "new answer"


def test_move_pdf_raises_error_when_source_does_not_exist(
    tmp_path: Path,
):
    source = tmp_path / "missing.pdf"
    destination_dir = tmp_path / "student"

    with pytest.raises(FileNotFoundError):
        move_pdf(source, destination_dir)


def test_classified_result_uses_existing_student_directory( ##classified 된 김철수 목적지가 실제 김철수 폴더인지 검증
    tmp_path: Path,
):
    student_root = tmp_path / "S반"
    student_dir = student_root / "김민수"
    review_dir = student_root / "보류"

    student_dir.mkdir(parents=True)

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=review_dir,
        ##school=None,
    )

    result = ClassificationResult(
        status=ClassificationStatus.CLASSIFIED,
        student=Student(name="김민수"),
    )

    destination = get_destination_dir(
        result=result,
        context=context,
    )

    assert destination == student_dir


def test_classified_result_does_not_create_missing_student_directory( ##
    tmp_path: Path,
):
    student_root = tmp_path / "S반"
    review_dir = student_root / "보류"

    student_root.mkdir()

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=review_dir,
        ##school=None,
    )

    result = ClassificationResult(
        status=ClassificationStatus.CLASSIFIED,
        student=Student(name="김민수"),
    )

    with pytest.raises(FileNotFoundError):
        get_destination_dir(
            result=result,
            context=context,
        )

    assert not (student_root / "김민수").exists()


def test_review_result_uses_review_directory( ##보류폴더 테스트 : 보류폴더 없으면 생성, 있으면 보류 폴더에 넣기
    tmp_path: Path,
):
    student_root = tmp_path / "S반"
    review_dir = student_root / "보류"

    student_root.mkdir()

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=review_dir,
        ##school=None,
    )

    result = ClassificationResult(
        status=ClassificationStatus.REVIEW,
        reason="학생 이름을 식별할 수 없음",
    )

    destination = get_destination_dir(
        result=result,
        context=context,
    )

    assert destination == review_dir
    assert review_dir.exists()


def test_new_student_result_uses_new_student_directory( ##신규생 테스트
    tmp_path: Path,
):
    student_root = tmp_path / "S반"
    review_dir = student_root / "보류"

    student_root.mkdir()

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=review_dir,
        ##school=None,
    )

    result = ClassificationResult(
        status=ClassificationStatus.NEW_STUDENT,
        reason="기존 학생 목록에서 이름을 찾을 수 없음",
    )

    destination = get_destination_dir(
        result=result,
        context=context,
    )

    assert destination == student_root / "신규생"
    assert destination.exists()


def test_classified_result_without_student_raises_error( ##classified인데 없는경우 review로
    tmp_path: Path,
):
    student_root = tmp_path / "S반"
    review_dir = student_root / "보류"

    student_root.mkdir()

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=review_dir,
        ##school=None,
    )

    result = ClassificationResult(
        status=ClassificationStatus.CLASSIFIED,
        student=None,
    )

    with pytest.raises(ValueError):
        get_destination_dir(
            result=result,
            context=context,
        )


def test_move_classified_pdf_moves_pdf_to_student_directory( ##classified된 파일 이동 테스트
    tmp_path: Path,
):
    input_dir = tmp_path / "input"
    student_root = tmp_path / "S반"
    student_dir = student_root / "김민수"
    review_dir = student_root / "보류"

    input_dir.mkdir()
    student_dir.mkdir(parents=True)

    source = input_dir / "answer.pdf"
    source.write_text("student answer")

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=review_dir,
        ##school=None,
    )

    result = ClassificationResult(
        status=ClassificationStatus.CLASSIFIED,
        student=Student(name="김민수"),
    )

    moved_path = move_classified_pdf(
        source=source,
        result=result,
        context=context,
    )

    assert moved_path == student_dir / "answer.pdf"
    assert moved_path.exists()
    assert not source.exists()


def test_move_classified_pdf_renames_duplicate_file( ##실제 이동, 중복 파일 테스트 : _1, _2 등
    tmp_path: Path,
):
    input_dir = tmp_path / "input"
    student_root = tmp_path / "S반"
    student_dir = student_root / "김민수"
    review_dir = student_root / "보류"

    input_dir.mkdir()
    student_dir.mkdir(parents=True)

    existing = student_dir / "answer.pdf"
    existing.write_text("existing answer")

    source = input_dir / "answer.pdf"
    source.write_text("new answer")

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=review_dir,
        ##school=None,
    )

    result = ClassificationResult(
        status=ClassificationStatus.CLASSIFIED,
        student=Student(name="김민수"),
    )

    moved_path = move_classified_pdf(
        source=source,
        result=result,
        context=context,
    )

    assert moved_path == student_dir / "answer_1.pdf"

    assert existing.read_text() == "existing answer"
    assert moved_path.read_text() == "new answer"



def test_get_destination_dir_uses_student_folder_name( ##테스트 추가 : 폴더명 오류
    tmp_path: Path,
):
    student_root = tmp_path / "S반"
    student_dir = student_root / "민윤기(달천고)"
    student_dir.mkdir(parents=True)

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=student_root / "보류",
    )

    student = Student(
        name="민윤기",
        school="달천고",
        folder_name="민윤기(달천고)",
    )

    result = ClassificationResult(
        status=ClassificationStatus.CLASSIFIED,
        student=student,
    )

    destination = get_destination_dir(
        result=result,
        context=context,
    )

    assert destination == student_dir    


def test_get_destination_dir_falls_back_to_student_name( ##테스트 추가 : 기존 folder_name이 없어도 작동하는지.
    tmp_path: Path,
):
    student_root = tmp_path / "S반"
    student_dir = student_root / "김민수"
    student_dir.mkdir(parents=True)

    context = InputContext(
        group_type="S",
        student_root=student_root,
        review_dir=student_root / "보류",
    )

    student = Student(
        name="김민수",
    )

    result = ClassificationResult(
        status=ClassificationStatus.CLASSIFIED,
        student=student,
    )

    destination = get_destination_dir(
        result=result,
        context=context,
    )

    assert destination == student_dir