from collections import defaultdict

from app.schemas.evidence import Evidence


def group_evidence_by_domain(
    evidence: list[Evidence],
) -> dict[str, list[Evidence]]:
    grouped: dict[str, list[Evidence]] = defaultdict(list)

    for item in evidence:
        grouped[item.functional_domain.value].append(item)

    return dict(grouped)
