from app.pipeline import analyze_case
from app.reasoning.relationships import RelationshipType


def test_direct_and_contradicted_evidence_creates_contradiction():
    result = analyze_case(
        "T006",
        "My father struggles to walk. "
        "He does not struggle to walk."
    )

    assert len(result.relationships) == 1

    relationship = result.relationships[0]

    assert relationship.source_evidence_id == "T006-E001"
    assert relationship.target_evidence_id == "T006-E002"
    assert relationship.relationship == RelationshipType.CONTRADICTS


def test_mixed_evidence_creates_support_and_contradiction_edges():
    result = analyze_case(
        "T007",
        "My father struggles to walk. "
        "He may have difficulty walking. "
        "He does not struggle to walk."
    )

    relationships = {
        (
            item.source_evidence_id,
            item.target_evidence_id,
            item.relationship,
        )
        for item in result.relationships
    }

    assert (
        "T007-E001",
        "T007-E002",
        RelationshipType.SUPPORTS,
    ) in relationships

    assert (
        "T007-E001",
        "T007-E003",
        RelationshipType.CONTRADICTS,
    ) in relationships

    assert (
        "T007-E002",
        "T007-E003",
        RelationshipType.CONTRADICTS,
    ) in relationships


def test_different_claims_are_not_related():
    result = analyze_case(
        "T008",
        "My father struggles to walk. "
        "He uses a walking stick."
    )

    assert result.relationships == []


def test_direct_and_inferred_evidence_support_same_claim():
    result = analyze_case(
        "T009",
        "My father struggles to walk. "
        "He may have difficulty walking."
    )

    assert len(result.relationships) == 1

    relationship = result.relationships[0]

    assert relationship.relationship == RelationshipType.SUPPORTS
