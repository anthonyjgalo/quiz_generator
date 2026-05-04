from pathlib import Path

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}
MAX_SIZE = 10 * 1024 * 1024


def validate_file(filename: str):
    ext = Path(filename).suffix.lstrip(".").lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: .{ext}")


def validate_text_length(text: str):
    char_count = len(text)
    if char_count < 200:
        raise ValueError(f"Text is too short ({char_count} chars). Minimum is 200.")
    if char_count > 50000:
        raise ValueError(f"Text is too long ({char_count} chars). Maximum is 50000.")
