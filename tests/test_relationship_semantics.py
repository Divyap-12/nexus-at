from app.pipeline import analyze_case
from app.reasoning.relationships import RelationshipType


def test_same_temporal_opposite_polarity_contradicts():
    result = analyze_case(
        "R002",
        "My father struggles to walk. "
        "He does not struggle to walk.",
    )

    assert len(result.relationships) == 1
    assert (
        result.relationships[0].relationship
        == RelationshipType.CONTRADICTS
    )


def test_different_temporal_same_polarity_is_temporally_distinct():
    result = analyze_case(
        "R003",
        "My father used to struggle to walk. "
        "He struggles to walk.",
    )

    assert len(result.relationships) == 1
    assert (
        result.relationships[0].relationship
        == RelationshipType.TEMPORALLY_DISTINCT
    )


def test_different_temporal_opposite_polarity_is_temporally_distinct():
    result = analyze_case(
        "R004",
        "My father used to struggle to walk. "
        "He does not struggle to walk.",
    )

    assert len(result.relationships) == 1
    assert (
        result.relationships[0].relationship
        == RelationshipType.TEMPORALLY_DISTINCT
    )
