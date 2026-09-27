from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InputContext:
    group_type: str
    student_root: Path
    review_dir: Path
    school: str | None = None


def parse_input_context(
    input_dir: Path,
    answers_root: Path,
) -> InputContext:
    """
    입력 폴더명을 분석해 학생 검색 범위와
    보류 폴더를 결정한다.

    예:
        2026-09-27_S반
        2026-09-27_Y반
        특강_고려대
        2026-09-27-연세대
    """

    folder_name = input_dir.name.strip()

    if not folder_name:
        raise ValueError("입력 폴더명이 비어 있습니다.")

    if "S반" in folder_name:
        student_root = answers_root / "S반"

        return InputContext(
            group_type="S",
            student_root=student_root,
            review_dir=student_root / "보류",
        )

    if "Y반" in folder_name:
        student_root = answers_root / "Y반"

        return InputContext(
            group_type="Y",
            student_root=student_root,
            review_dir=student_root / "보류",
        )

    school = _extract_school_name(folder_name)

    if school:
        student_root = answers_root / school

        return InputContext(
            group_type="SPECIAL",
            student_root=student_root,
            review_dir=student_root / "보류",
            school=school,
        )

    raise ValueError(
        "입력 폴더에서 S반, Y반 또는 특강 학교명을 "
        f"판별할 수 없습니다: {folder_name}"
    )


def _extract_school_name(folder_name: str) -> str | None:
    """
    폴더명에서 대학명을 추출한다.

    현재 운영 정책상 특강 학교 폴더는
    '고려대', '연세대', '성균관대'처럼
    '대'로 끝나는 이름을 사용한다고 가정한다.
    """

    normalized = (
        folder_name
        .replace("_", " ")
        .replace("-", " ")
        .replace("(", " ")
        .replace(")", " ")
    )

    tokens = normalized.split()

    ignored_tokens = {
        "특강대",
    }

    for token in tokens:
        token = token.strip()

        if token in ignored_tokens:
            continue

        if len(token) >= 2 and token.endswith("대"):
            return token

    return None