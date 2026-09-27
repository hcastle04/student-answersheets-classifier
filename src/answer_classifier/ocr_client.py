import json
from pathlib import Path
import time
import uuid
from typing import Any

import requests

from answer_classifier.config import (
    get_clova_ocr_secret,
    get_clova_ocr_template_id,
    get_clova_ocr_invoke_url,
)


class OcrApiError(Exception):
    """CLOVA OCR API 요청 또는 응답 처리 실패."""


def request_template_ocr(
    pdf_path: Path,
) -> dict[str, Any]:
    """
    PDF 파일을 CLOVA Template OCR API로 전송하고
    원본 JSON 응답을 반환한다.
    """

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF does not exist: {pdf_path}"
        )

    if not pdf_path.is_file():
        raise ValueError(
            f"PDF path is not a file: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"File is not a PDF: {pdf_path}"
        )

    message = {
        "version": "V2",
        "requestId": str(uuid.uuid4()),
        "timestamp": int(time.time() * 1000),
        "lang": "ko",
        "images": [
            {
                "format": "pdf",
                "name": pdf_path.stem,
                "templateIds": [
                    get_clova_ocr_template_id()
                ],
            }
        ],
    }

    headers = {
        "X-OCR-SECRET": get_clova_ocr_secret(),
    }

    with pdf_path.open("rb") as pdf_file:
        files = {
            "file": (
                pdf_path.name,
                pdf_file,
                "application/pdf",
            )
        }

        data = {
            "message": json.dumps(
                message,
                ensure_ascii=False,
            )
        }

        try:
            response = requests.post(
                get_clova_ocr_invoke_url(),
                headers=headers,
                files=files,
                data=data,
                timeout=30,
            )

        except requests.RequestException as exc:
            raise OcrApiError(
                "Failed to call CLOVA OCR API."
            ) from exc

    if not response.ok:
        raise OcrApiError(
            f"CLOVA OCR API returned "
            f"HTTP {response.status_code}: "
            f"{response.text}"
        )

    try:
        return response.json()

    except ValueError as exc:
        raise OcrApiError(
            "CLOVA OCR API returned invalid JSON."
        ) from exc