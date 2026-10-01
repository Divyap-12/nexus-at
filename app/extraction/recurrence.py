import re

from app.extraction.rules import ExtractionRule


RECURRENCE_MARKERS = (
    "again",
    "once more",
    "once again",
    "returned",
    "has returned",
    "have returned",
    "came back",
    "come back",
    "returned again",
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


def find_recurrence_rule_from_claims(
    text: str,
    previous_rules: list[ExtractionRule],
) -> ExtractionRule | None:
    if not is_recurrence(text):
        return None

    if not previous_rules:
        return None

    normalized = text.lower()

    if any(
        re.search(
            rf"\b{re.escape(marker)}\b",
            normalized,
        )
        for marker in (
            "the problem has returned",
            "the problem returned",
            "the problem came back",
            "the issue has returned",
            "the issue returned",
            "the issue came back",
        )
    ):
        unique_rules = []

        for rule in previous_rules:
            if rule not in unique_rules:
                unique_rules.append(rule)

        if len(unique_rules) == 1:
            return unique_rules[0]

    return None
