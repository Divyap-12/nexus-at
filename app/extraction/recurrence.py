import re

from app.extraction.rules import ExtractionRule


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


def find_recurrence_rule(
    text: str,
    previous_rules: list[ExtractionRule],
) -> ExtractionRule | None:
    if not is_recurrence(text):
        return None

    normalized = text.lower()

    # Try to match a meaningful verb/activity from the recurrence
    # against previously established rules, preferring the most
    # semantically compatible rule rather than simply using the
    # immediately previous rule.
    recurrence_terms = (
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
    )

    if not any(term in normalized for term in recurrence_terms):
        return None

    for rule in reversed(previous_rules):
        if rule.name == "walking_difficulty":
            return rule

    return None
