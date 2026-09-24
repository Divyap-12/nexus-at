from app.pipeline import analyze_case
from app.schemas.evidence import EvidenceStrength


def test_direct_evidence_is_strong():
    result = analyze_case(
        "T006",
        "My father struggles to walk."
    )

    assert result.case.evidence
    assert result.case.evidence[0].strength == EvidenceStrength.STRONG


def test_inferred_evidence_is_weak():
    result = analyze_case(
        "T007",
        "He may have difficulty walking."
    )

    assert result.case.evidence
    assert result.case.evidence[0].strength == EvidenceStrength.WEAK


def test_contradicted_evidence_is_strong():
    result = analyze_case(
        "T008",
        "He does not struggle to walk."
    )

    assert result.case.evidence
    assert result.case.evidence[0].strength == EvidenceStrength.STRONG


def test_strength_is_returned_for_multiple_evidence_items():
    result = analyze_case(
        "T009",
        "My father struggles to walk. "
        "He may have difficulty walking."
    )

    assert len(result.case.evidence) == 2

    strengths = [
        item.strength
        for item in result.case.evidence
    ]

    assert strengths == [
        EvidenceStrength.STRONG,
        EvidenceStrength.WEAK,
    ]
