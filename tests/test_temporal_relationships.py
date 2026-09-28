from app.pipeline import analyze_case
from app.reasoning.relationships import RelationshipType


def test_historical_and_current_evidence_are_temporally_distinct():
    result = analyze_case(
        "T011",
        "My father used to struggle to walk. "
        "He does not struggle to walk."
    )

    assert len(result.relationships) == 1

    relationship = result.relationships[0]

    assert relationship.relationship == RelationshipType.TEMPORALLY_DISTINCT


def test_historical_and_current_positive_evidence_are_temporally_distinct():
    result = analyze_case(
        "T012",
        "My father used to struggle to walk. "
        "He struggles to walk."
    )

    assert len(result.relationships) == 1

    relationship = result.relationships[0]

    assert relationship.relationship == RelationshipType.TEMPORALLY_DISTINCT


def test_same_temporal_claims_still_support():
    result = analyze_case(
        "T013",
        "My father struggles to walk. "
        "He cannot walk long distances."
    )

    assert result.relationships == []


def test_historical_same_claim_supports_historical_evidence():
    result = analyze_case(
        "T014",
        "My father used to struggle to walk. "
        "He previously had difficulty walking."
    )

    assert len(result.relationships) == 1

    relationship = result.relationships[0]

    assert relationship.relationship == RelationshipType.SUPPORTS
