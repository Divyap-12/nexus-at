import re


RECURRENCE_MARKERS = (
    "again",
    "once more",
    "once again",
)


def is_recurrence(text: str) -> bool:
    normalized = text.lower()

    return any(
        re.search(
            rf"\b{re.escape(marker)}\b",
            normalized,
        )
        for marker in RECURRENCE_MARKERS
    )
