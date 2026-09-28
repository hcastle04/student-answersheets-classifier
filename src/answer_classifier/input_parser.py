import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InputContext:
    group_type: str
    student_root: Path
    review_dir: Path

def parse_input_context(
    input_dir: Path,
    answers_root: Path,
) -> InputContext:
    """
    실전특강 입력 폴더명에서 S/Y 반을 판별하고
    해당 학생 저장소 경로를 반환한다.
    """

    folder_name = input_dir.name.strip()

    if not folder_name:
        raise ValueError("입력 폴더명이 비어 있습니다.")

    group_type = _extract_group_type(folder_name)

    if group_type is None:
        raise ValueError(
            "입력 폴더에서 실전특강 반 정보를 "
            f"판별할 수 없습니다: {folder_name}"
        )
    
    student_root = answers_root / f"{group_type}반"

    return InputContext(
        group_type=group_type,
        student_root=student_root,
        review_dir=student_root / "보류",
    )

def _extract_group_type(
    folder_name: str,
) -> str | None:
    """
    실전특강 폴더명에서 S/Y 반을 추출한다.

    예:
        오T실전특강1회S일610(박정외T)_채점후
        -> S

        오T실전특강1회Y금610(박종관T)_채점후
        -> Y
    """
    match = re.search(
        r"실전특강\d+회([SY])",
        folder_name,
    )

    if match is None:
        return None

    return match.group(1)
