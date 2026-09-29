from app.pipeline import analyze_case
from app.reasoning.claim_status import ClaimStatus


def test_historical_and_current_opposite_polarity_are_not_conflicting():
    result = analyze_case(
        "CS005",
        "My father used to struggle to walk, "
        "but now he does not struggle to walk.",
    )

    assert len(result.claims) == 1
    assert result.claims[0].status == ClaimStatus.SUPPORTED


def test_current_opposite_polarity_remains_conflicting():
    result = analyze_case(
        "CS006",
        "My father struggles to walk. "
        "He does not struggle to walk.",
    )

    assert len(result.claims) == 1
    assert result.claims[0].status == ClaimStatus.CONFLICTING
