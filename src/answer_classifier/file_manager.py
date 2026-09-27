from pathlib import Path
import shutil

from answer_classifier.classifier import (
    ClassificationResult,
    ClassificationStatus,
)
from answer_classifier.input_parser import InputContext


def get_unique_destination(destination: Path) -> Path:
    """
    목적지에 같은 이름의 파일이 이미 존재하면
    _1, _2, ... suffix를 붙여 중복되지 않는 경로를 반환한다.
    """

    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix

    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"

        if not candidate.exists():
            return candidate

        counter += 1


def move_pdf(source: Path, destination_dir: Path) -> Path:
    """
    PDF 파일을 목적지 디렉터리로 이동한다.

    동일한 파일명이 이미 존재하면 기존 파일을 덮어쓰지 않고
    _1, _2, ... suffix가 붙은 이름으로 이동한다.
    """

    if not source.exists():
        raise FileNotFoundError(
            f"Source PDF does not exist: {source}"
        )

    if not source.is_file():
        raise ValueError(
            f"Source path is not a file: {source}"
        )

    destination_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = destination_dir / source.name
    destination = get_unique_destination(destination)

    shutil.move(
        str(source),
        str(destination),
    )

    return destination


def get_destination_dir( ##추가
    result: ClassificationResult,
    context: InputContext,
) -> Path:
    """
    ClassificationResult에 따라
    PDF가 이동해야 할 목적지 폴더를 결정한다.
    """

    if result.status == ClassificationStatus.CLASSIFIED:
        if result.student is None:
            raise ValueError(
                "CLASSIFIED result must contain a student."
            )

        student_dir = context.student_root / result.student.name

        # 기존 학생 폴더는 자동 생성하지 않는다.
        if not student_dir.exists():
            raise FileNotFoundError(
                f"Student directory does not exist: {student_dir}"
            )

        if not student_dir.is_dir():
            raise NotADirectoryError(
                f"Student path is not a directory: {student_dir}"
            )

        return student_dir

    if result.status == ClassificationStatus.REVIEW:
        # 보류 폴더는 시스템 폴더이므로 없으면 생성한다.
        context.review_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return context.review_dir

    if result.status == ClassificationStatus.NEW_STUDENT:
        # 신규생 역시 기존 학생 개인 폴더가 아니라
        # 확인 대기용 시스템 폴더이다.
        new_student_dir = context.student_root / "신규생"

        new_student_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return new_student_dir

    raise ValueError(
        f"Unsupported classification status: {result.status}"
    )


def move_classified_pdf( ##추가
    source: Path,
    result: ClassificationResult,
    context: InputContext,
) -> Path:
    """
    분류 결과를 기준으로 목적지를 결정한 뒤
    PDF 파일을 실제로 이동한다.
    """

    destination_dir = get_destination_dir(
        result=result,
        context=context,
    )

    return move_pdf(
        source=source,
        destination_dir=destination_dir,
    )