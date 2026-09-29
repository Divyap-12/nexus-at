import re

from app.extraction.rules import ExtractionRule


RECURRENCE_MARKERS = (
    "again",
    "once more",
    "once again",
)


RECURRENCE_TERMS = {
    "walking_difficulty": (
        "struggle",
        "struggles",
        "struggling",
        "struggled",
        "trouble",
        "difficulty",
        "difficult",
        "hard",
        "walk",
        "walking",
        "walks",
    ),
    "limited_walking_distance": (
        "walk",
        "walking",
        "walks",
        "far",
        "distance",
        "distances",
    ),
}


def is_recurrence(text: str) -> bool:
    normalized = text.lower()

    return any(
        re.search(
            rf"\b{re.escape(marker)}\b",
            normalized,
        )
        for marker in RECURRENCE_MARKERS
    )


def find_recurrence_rule(
    text: str,
    previous_rules: list[ExtractionRule],
) -> ExtractionRule | None:
    if not is_recurrence(text):
        return None

    normalized = text.lower()

    for rule in reversed(previous_rules):
        terms = RECURRENCE_TERMS.get(rule.name)

        if not terms:
            continue

        if any(
            re.search(
                rf"\b{re.escape(term)}\b",
                normalized,
            )
            for term in terms
        ):
            return rule

    return None
