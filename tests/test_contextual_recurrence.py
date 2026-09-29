from app.pipeline import analyze_case
from app.reasoning.claim_status import ClaimStatus


def test_repeated_claim_after_intervening_contradiction_is_extracted():
    result = analyze_case(
        "CS007",
        "My father used to struggle to walk. "
        "He does not struggle to walk. "
        "But now he struggles again.",
    )

    assert len(result.case.evidence) == 3

    historical, contradicted, current = result.case.evidence

    assert historical.temporal_status.value == "HISTORICAL"
    assert historical.evidence_type.value == "DIRECT"

    assert contradicted.temporal_status.value == "CURRENT"
    assert contradicted.evidence_type.value == "CONTRADICTED"

    assert current.claim == "Person reports difficulty walking."
    assert current.temporal_status.value == "CURRENT"
    assert current.evidence_type.value == "DIRECT"

    assert result.claims[0].status != ClaimStatus.CONFLICTING
