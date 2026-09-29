from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractionRule:
    name: str
    keywords: tuple[str, ...]
    claim: str
    functional_domain: str


MOBILITY_RULES = (
    ExtractionRule(
        name="limited_walking_distance",
        keywords=(
            "cannot walk long distances",
            "can't walk long distances",
            "unable to walk long distances",
            "cannot walk far",
            "can't walk far",
            "unable to walk far",
        ),
        claim="Person has limited walking distance.",
        functional_domain="MOBILITY",
    ),
    ExtractionRule(
        name="walking_difficulty",
        keywords=(
            "difficulty walking",
            "struggling to walk",
            "struggle to walk",
            "previously struggled to walk",
            "struggles to walk",
            "cannot walk",
            "can't walk",
            "unable to walk",
            "trouble walking",
            "walking has become difficult",
            "walking is difficult",
            "finds it hard to walk",
            "struggled to walk",
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

    matches: list[tuple[ExtractionRule, str]] = []

    for rule in MOBILITY_RULES:
        matching_keywords = [
            keyword
            for keyword in rule.keywords
            if keyword in normalized_text
        ]

        if matching_keywords:
            longest_keyword = max(
                matching_keywords,
                key=len,
            )
            matches.append((rule, longest_keyword))

    selected: list[ExtractionRule] = []

    for rule, keyword in matches:
        is_shadowed = any(
            other_keyword != keyword
            and len(other_keyword) > len(keyword)
            and keyword in other_keyword
            for _, other_keyword in matches
        )

        if not is_shadowed:
            selected.append(rule)

    return selected
