from answer_classifier.classifier import (
    ClassificationStatus,
    Student,
    classify_student,
)


def test_classified_when_single_student_matches_name(): ## 이름O 학교X 동명이인X
    students = [
        Student(name="김민수", school="고려대"),
    ]

    result = classify_student(
        recognized_name="김민수",
        recognized_school=None,
        candidates=students,
    )

    assert result.status == ClassificationStatus.CLASSIFIED
    assert result.student == students[0]


def test_review_when_name_is_missing(): ## 이름X 학교X : 리뷰로
    students = [
        Student(name="김민수", school="고려대"),
    ]

    result = classify_student(
        recognized_name=None,
        recognized_school="고려대",
        candidates=students,
    )

    assert result.status == ClassificationStatus.REVIEW


def test_new_student_when_name_does_not_exist(): ##명단에 이름X : 신규생
    students = [
        Student(name="김민수", school="고려대"),
    ]

    result = classify_student(
        recognized_name="이영희",
        recognized_school="연세대",
        candidates=students,
    )

    assert result.status == ClassificationStatus.NEW_STUDENT


def test_review_when_duplicate_names_and_school_is_missing(): ## 이름 같은데 학교 다름 : 리뷰
    students = [
        Student(name="김민수", school="고려대"),
        Student(name="김민수", school="연세대"),
    ]

    result = classify_student(
        recognized_name="김민수",
        recognized_school=None,
        candidates=students,
    )

    assert result.status == ClassificationStatus.REVIEW


def test_classified_when_duplicate_name_is_resolved_by_school(): ##이름O 학교다름 : 분류
    students = [
        Student(name="김민수", school="고려대"),
        Student(name="김민수", school="연세대"),
    ]

    result = classify_student(
        recognized_name="김민수",
        recognized_school="연세대",
        candidates=students,
    )

    assert result.status == ClassificationStatus.CLASSIFIED
    assert result.student == students[1]


def test_review_when_duplicate_name_school_does_not_match(): ## 이름같고 학교같음 =동명이인 : 리뷰
    students = [
        Student(name="김민수", school="고려대"),
        Student(name="김민수", school="연세대"),
    ]

    result = classify_student(
        recognized_name="김민수",
        recognized_school="성균관대",
        candidates=students,
    )

    assert result.status == ClassificationStatus.REVIEW