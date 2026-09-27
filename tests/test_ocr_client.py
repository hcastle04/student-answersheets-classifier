from pathlib import Path

import pytest
import requests

from answer_classifier.ocr_client import (
    OcrApiError,
    request_template_ocr,
)


def test_request_template_ocr_raises_when_pdf_does_not_exist(
    tmp_path: Path,
):
    missing_pdf = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        request_template_ocr(missing_pdf)


def test_request_template_ocr_raises_when_path_is_not_file(
    tmp_path: Path,
):
    directory = tmp_path / "answer.pdf"
    directory.mkdir()

    with pytest.raises(ValueError):
        request_template_ocr(directory)


def test_request_template_ocr_raises_when_file_is_not_pdf(
    tmp_path: Path,
):
    text_file = tmp_path / "answer.txt"
    text_file.write_text("not pdf")

    with pytest.raises(ValueError):
        request_template_ocr(text_file)


def test_request_template_ocr_raises_api_error_when_request_fails(
    tmp_path: Path,
    monkeypatch,
):
    pdf_path = tmp_path / "answer.pdf"
    pdf_path.write_bytes(b"fake pdf")

    monkeypatch.setenv(
        "CLOVA_OCR_INVOKE_URL",
        "https://example.com/ocr",
    )
    monkeypatch.setenv(
        "CLOVA_OCR_SECRET",
        "test-secret",
    )
    monkeypatch.setenv(
        "CLOVA_OCR_TEMPLATE_ID",
        "43573",
    )

    def fake_post(*args, **kwargs):
        raise requests.RequestException(
            "network error"
        )

    monkeypatch.setattr(
        requests,
        "post",
        fake_post,
    )

    with pytest.raises(OcrApiError):
        request_template_ocr(pdf_path)