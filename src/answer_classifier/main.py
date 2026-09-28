from pathlib import Path
import sys

from answer_classifier.input_parser import parse_input_context
from answer_classifier.pipeline import process_answer_directory

def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python -m answer_classifier.main "
            "<input_dir> <answers_root>"
        )
        raise SystemExit(1)

    input_dir = Path(sys.argv[1])
    answers_root = Path(sys.argv[2])

    context = parse_input_context(
        input_dir=input_dir,
        answers_root=answers_root,
    )

    results = process_answer_directory(
        input_dir=input_dir,
        context=context,
    )

    print(f"처리 완료: {len(results)}개 PDF")

    for result in results:
        print(
            f"{result.classification.status.value} "
            f"-> {result.destination}"
        )

if __name__ == "__main__":
    main()