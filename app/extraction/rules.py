from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractionRule:
    name: str
    keywords: tuple[str, ...]
    claim: str
    functional_domain: str


MOBILITY_RULES = (
    ExtractionRule(
        name="walking_difficulty",
        keywords=(
            "difficulty walking",
            "struggling to walk",
            "struggle to walk",
            "struggles to walk",
            "cannot walk",
            "can't walk",
            "unable to walk",
            "trouble walking",
        ),
        claim="Person reports difficulty walking.",
        functional_domain="MOBILITY",
    ),
    ExtractionRule(
        name="walking_aid",
        keywords=(
            "walking stick",
            "walker",
            "wheelchair",
            "cane",
            "crutches",
        ),
        claim="Person uses a mobility aid.",
        functional_domain="MOBILITY",
    ),
)


def find_matching_keyword(
    text: str,
    rule: ExtractionRule,
) -> str:
    normalized_text = text.lower()

    for keyword in rule.keywords:
        if keyword in normalized_text:
            return keyword

    raise ValueError(
        f"No matching keyword found for rule: {rule.name}"
    )


def find_matching_rules(text: str) -> list[ExtractionRule]:
    normalized_text = text.lower()

    matches: list[ExtractionRule] = []

    for rule in MOBILITY_RULES:
        if any(
            keyword in normalized_text
            for keyword in rule.keywords
        ):
            matches.append(rule)

    return matches
