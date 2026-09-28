from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ClassificationStatus(str, Enum):
    CLASSIFIED = "CLASSIFIED"
    REVIEW = "REVIEW"
    NEW_STUDENT = "NEW_STUDENT"


@dataclass(frozen=True)
class Student:
    name: str
    school: Optional[str] = None
    folder_name: Optional[str] = None


@dataclass(frozen=True)
class ClassificationResult:
    status: ClassificationStatus
    student: Optional[Student] = None
    reason: Optional[str] = None


def classify_student(
    recognized_name: Optional[str],
    recognized_school: Optional[str],
    candidates: list[Student],
) -> ClassificationResult:
    """
    OCR로 인식된 이름/학교와 기존 학생 후보 목록을 바탕으로
    학생 답안지의 분류 결과를 결정한다.
    """

    name = recognized_name.strip() if recognized_name else None
    school = recognized_school.strip() if recognized_school else None

    if not name:
        return ClassificationResult(
            status=ClassificationStatus.REVIEW,
            reason="학생 이름을 식별할 수 없음",
        )

    same_name_students = [
        student
        for student in candidates
        if student.name.strip() == name
    ]

    if not same_name_students:
        return ClassificationResult(
            status=ClassificationStatus.NEW_STUDENT,
            reason="기존 학생 목록에서 이름을 찾을 수 없음",
        )

    if len(same_name_students) == 1:
        return ClassificationResult(
            status=ClassificationStatus.CLASSIFIED,
            student=same_name_students[0],
            reason="동일 이름 학생이 1명임",
        )

    if not school:
        return ClassificationResult(
            status=ClassificationStatus.REVIEW,
            reason="동명이인이 존재하지만 학교 정보가 없음",
        )

    same_school_students = [
        student
        for student in same_name_students
        if student.school
        and student.school.strip() == school
    ]

    if len(same_school_students) == 1:
        return ClassificationResult(
            status=ClassificationStatus.CLASSIFIED,
            student=same_school_students[0],
            reason="이름과 학교가 모두 일치함",
        )

    return ClassificationResult(
        status=ClassificationStatus.REVIEW,
        reason="동명이인을 학교 정보로 명확히 구분할 수 없음",
    )