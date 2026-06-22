from pathlib import Path

from core.constants import ALLOWED_EXTENSIONS
from fastapi import HTTPException, status


def validate_file(filename: str) -> str:
    ext = Path(filename).suffix.lstrip(".").lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension: .{ext}. Allowed extensions are: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    return ext


def validate_text_length(text: str) -> None:
    char_count = len(text)
    if char_count < 200:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Text is too short ({char_count} chars). Minimum required is 200.",
        )
    if char_count > 50000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Text is too long ({char_count} chars). Maximum allowed is 50000.",
        )
