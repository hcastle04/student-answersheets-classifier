from pathlib import Path
import sys

from answer_classifier.ocr_client import request_template_ocr
from answer_classifier.ocr_parser import parse_clova_response


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/clova_smoke_test.py "
            "<answer_pdf_path>"
        )
        return

    pdf_path = Path(sys.argv[1])

    print(f"OCR request: {pdf_path.name}")

    raw_response = request_template_ocr(pdf_path)

    student_info = parse_clova_response(raw_response)

    print()
    print("OCR result")
    print("--------------------")
    print(f"student_name: {student_info.student_name}")
    print(
        "student_name confidence: "
        f"{student_info.student_name_confidence}"
    )
    print(f"school: {student_info.school}")
    print(
        "school confidence: "
        f"{student_info.school_confidence}"
    )


if __name__ == "__main__":
    main()