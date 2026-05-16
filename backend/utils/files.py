from pathlib import Path

from core.constants import ALLOWED_EXTENSIONS


def validate_file(filename: str):
    ext = Path(filename).suffix.lstrip(".").lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: .{ext}")

    return ext


def validate_text_length(text: str):
    char_count = len(text)
    if char_count < 200:
        raise ValueError(f"Text is too short ({char_count} chars). Minimum is 200.")
    if char_count > 50000:
        raise ValueError(f"Text is too long ({char_count} chars). Maximum is 50000.")
