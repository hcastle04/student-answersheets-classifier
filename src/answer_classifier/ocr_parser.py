from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class OCRStudentInfo:
    student_name: Optional[str]
    school: Optional[str]
    student_name_confidence: Optional[float]
    school_confidence: Optional[float]


def parse_clova_response(
    payload: dict[str, Any],
) -> OCRStudentInfo:
    images = payload.get("images")

    if not images:
        raise ValueError(
            "CLOVA OCR response does not contain images."
        )

    fields = images[0].get("fields", [])

    field_map = {
        field.get("name"): field
        for field in fields
        if field.get("name")
    }

    student_name_field = field_map.get("student_name")
    school_field = field_map.get("school")

    return OCRStudentInfo(
        student_name=_extract_text(student_name_field),
        school=_extract_text(school_field),
        student_name_confidence=_extract_confidence(
            student_name_field
        ),
        school_confidence=_extract_confidence(
            school_field
        ),
    )


def _extract_text(
    field: Optional[dict[str, Any]],
) -> Optional[str]:
    if not field:
        return None

    text = field.get("inferText")

    if not text:
        return None

    text = text.strip()

    return text or None


def _extract_confidence(
    field: Optional[dict[str, Any]],
) -> Optional[float]:
    if not field:
        return None

    confidence = field.get("inferConfidence")

    if confidence is None:
        return None

    return float(confidence)