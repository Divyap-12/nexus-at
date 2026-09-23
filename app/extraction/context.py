from enum import Enum
import re


class ContextType(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL = "HISTORICAL"
    NEGATED = "NEGATED"
    UNCERTAIN = "UNCERTAIN"
    PLANNED = "PLANNED"


HISTORICAL_MARKERS = (
    "used to",
    "previously",
    "in the past",
    "last year",
    "last month",
    "earlier",
    "formerly",
)

NEGATION_MARKERS = (
    "no longer",
    "does not",
    "doesn't",
    "do not",
    "don't",
    "isn't",
    "is not",
    "are not",
    "aren't",
    "was not",
    "wasn't",
    "were not",
    "weren't",
)

UNCERTAINTY_MARKERS = (
    "may",
    "might",
    "possibly",
    "perhaps",
    "could",
    "seems",
    "appears",
)

PLANNED_MARKERS = (
    "will",
    "plans to",
    "planning to",
    "scheduled to",
    "going to",
)


def _contains_marker(text: str, marker: str) -> bool:
    pattern = rf"\b{re.escape(marker)}\b"
    return re.search(pattern, text) is not None


def detect_context(text: str) -> ContextType:
    normalized = text.lower()

    if any(_contains_marker(normalized, marker) for marker in NEGATION_MARKERS):
        return ContextType.NEGATED

    if any(_contains_marker(normalized, marker) for marker in HISTORICAL_MARKERS):
        return ContextType.HISTORICAL

    if any(_contains_marker(normalized, marker) for marker in UNCERTAINTY_MARKERS):
        return ContextType.UNCERTAIN

    if any(_contains_marker(normalized, marker) for marker in PLANNED_MARKERS):
        return ContextType.PLANNED

    return ContextType.CURRENT
