import pytest

from answer_classifier.ocr_parser import (
    parse_clova_response,
)


def test_parse_clova_response_extracts_student_info():
    payload = {
        "images": [
            {
                "fields": [
                    {
                        "name": "school",
                        "inferText": "휘문 고등학교",
                        "inferConfidence": 0.97,
                    },
                    {
                        "name": "student_name",
                        "inferText": "안우형",
                        "inferConfidence": 0.98,
                    },
                ]
            }
        ]
    }

    result = parse_clova_response(payload)

    assert result.student_name == "안우형"
    assert result.school == "휘문 고등학교"

    assert result.student_name_confidence == 0.98
    assert result.school_confidence == 0.97


def test_parse_clova_response_handles_missing_school():
    payload = {
        "images": [
            {
                "fields": [
                    {
                        "name": "student_name",
                        "inferText": "안우형",
                        "inferConfidence": 0.98,
                    }
                ]
            }
        ]
    }

    result = parse_clova_response(payload)

    assert result.student_name == "안우형"
    assert result.school is None
    assert result.school_confidence is None


def test_parse_clova_response_handles_empty_student_name():
    payload = {
        "images": [
            {
                "fields": [
                    {
                        "name": "student_name",
                        "inferText": "   ",
                        "inferConfidence": 0.15,
                    }
                ]
            }
        ]
    }

    result = parse_clova_response(payload)

    assert result.student_name is None
    assert result.student_name_confidence == 0.15


def test_parse_clova_response_raises_when_images_missing():
    payload = {
        "images": []
    }

    with pytest.raises(ValueError):
        parse_clova_response(payload)