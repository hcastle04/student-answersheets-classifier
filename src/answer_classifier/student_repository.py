from pathlib import Path

from answer_classifier.classifier import Student


SYSTEM_FOLDER_NAMES = {
    "보류",
    "review",
    "new_student",
    "신규생",
}

def parse_student_folder_name( 
    folder_name: str,
) -> tuple[str, str | None]:
    """
    학생 폴더명에서 학생 이름과 학교명을 분리한다.

    예:
        김주훈
        -> ("김주훈", None)

        민윤기(달천고)
        -> ("민윤기", "달천고")
    """

    normalized = folder_name.strip()

    if not normalized:
        raise ValueError("학생 폴더명이 비어 있습니다.")

    if normalized.endswith(")") and "(" in normalized:
        name, school_part = normalized.rsplit("(", 1)

        name = name.strip()
        school = school_part[:-1].strip()

        if name and school:
            return name, school

    return normalized, None


def load_students(
    base_dir: Path, ##school을 넘길 필요 없음
) -> list[Student]:
    """
    학생 폴더를 읽어 Student 목록으로 변환한다.


    각 하위 디렉터리명을 학생 이름으로 간주한다.
    시스템용 폴더는 제외한다.
    """

    if not base_dir.exists():
        return []

    if not base_dir.is_dir():
        return []

    students: list[Student] = []

    for path in sorted(base_dir.iterdir()):
        if not path.is_dir():
            continue

        if path.name in SYSTEM_FOLDER_NAMES:
            continue
        
        name, school = parse_student_folder_name(path.name)

        students.append(
            Student(
                name=name,
                school=school,
                folder_name=path.name,
            )
        )
    return students

