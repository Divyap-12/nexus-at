from app.pipeline import analyze_case
from app.reasoning.claim_status import ClaimStatus
from app.reasoning.relationships import RelationshipType


def test_direct_and_inferred_evidence_produces_mixed_claim():
    result = analyze_case(
        "T001",
        "My father struggles to walk. "
        "He may have difficulty walking."
    )

    assert len(result.claims) == 1

    claim = result.claims[0]

    assert claim.status == ClaimStatus.MIXED
    assert len(claim.evidence_ids) == 2


def test_mobility_aid_claim_is_supported():
    result = analyze_case(
        "T002",
        "He uses a walking stick."
    )

    assert len(result.claims) == 1

    claim = result.claims[0]

    assert claim.status == ClaimStatus.SUPPORTED
    assert claim.functional_domain.value == "MOBILITY"


def test_explanation_contains_claim_status_and_evidence():
    result = analyze_case(
        "T003",
        "My father struggles to walk. "
        "He uses a walking stick. "
        "He may have difficulty walking."
    )

    assert result.explanation

    explanation = "\n".join(result.explanation)

    assert "is MIXED" in explanation
    assert "Direct evidence:" in explanation
    assert "Inferred evidence:" in explanation
    assert "SUPPORTS" in explanation


def test_support_relationship_is_created():
    result = analyze_case(
        "T004",
        "My father struggles to walk. "
        "He may have difficulty walking."
    )

    assert result.relationships

    relationship = result.relationships[0]

    assert relationship.relationship == RelationshipType.SUPPORTS


def test_contradicted_evidence_is_reported():
    result = analyze_case(
        "T005",
        "My father struggles to walk. "
        "He does not struggle to walk."
    )

    assert result.claims

    claim = result.claims[0]

    assert claim.status == ClaimStatus.CONFLICTING
