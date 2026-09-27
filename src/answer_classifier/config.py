import os

from dotenv import load_dotenv


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable is not configured: {name}"
        )

    return value


def get_clova_ocr_invoke_url() -> str:
    return get_required_env(
        "CLOVA_OCR_INVOKE_URL"
    )


def get_clova_ocr_secret() -> str:
    return get_required_env("CLOVA_OCR_SECRET")


def get_clova_ocr_template_id() -> int:
    value = get_required_env("CLOVA_OCR_TEMPLATE_ID")

    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(
            "CLOVA_OCR_TEMPLATE_ID must be an integer."
        ) from exc