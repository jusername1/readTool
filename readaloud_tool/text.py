import re
from typing import Iterable


_WHITESPACE_RE = re.compile(r"[ \t\f\v]+")
_LINEBREAK_RE = re.compile(r"\r\n|\r|\n")


def clean_text(text: str) -> str:
    # Normalize newlines then unwrap hard line breaks that commonly come from PDFs.
    text = _LINEBREAK_RE.sub("\n", text)
    lines = [ln.strip() for ln in text.split("\n")]
    lines = [ln for ln in lines if ln != ""]
    text = " ".join(lines)
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


def chunk_text(text: str, max_chars: int) -> Iterable[str]:
    if len(text) <= max_chars:
        yield text
        return

    # Prefer splitting on sentence-ish boundaries.
    parts: list[str] = []
    buf = ""
    for token in re.split(r"(?<=[.!?])\s+", text):
        if not token:
            continue
        candidate = (buf + " " + token).strip() if buf else token
        if len(candidate) <= max_chars:
            buf = candidate
            continue

        if buf:
            parts.append(buf)
            buf = token
        else:
            # Very long token: hard split.
            for i in range(0, len(token), max_chars):
                parts.append(token[i : i + max_chars])
            buf = ""

    if buf:
        parts.append(buf)

    for p in parts:
        if p.strip():
            yield p.strip()
