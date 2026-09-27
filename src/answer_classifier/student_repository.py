from pathlib import Path

from answer_classifier.classifier import Student


SYSTEM_FOLDER_NAMES = {
    "보류",
    "review",
    "new_student",
    "신규생",
}


def load_students(
    base_dir: Path,
    school: str | None = None,
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

        students.append(
            Student(
                name=path.name,
                school=school,
            )
        )

    return students