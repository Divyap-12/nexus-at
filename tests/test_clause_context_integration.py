from app.pipeline import analyze_case
from app.schemas.evidence import EvidenceType, TemporalStatus


def test_historical_and_current_context_stay_with_their_clauses():
    result = analyze_case(
        "P001",
        "My father used to struggle to walk, but now he has trouble walking.",
    )

    assert len(result.case.evidence) == 2

    historical, current = result.case.evidence

    assert historical.claim == "Person reports difficulty walking."
    assert historical.temporal_status == TemporalStatus.HISTORICAL
    assert historical.evidence_type == EvidenceType.DIRECT

    assert current.claim == "Person reports difficulty walking."
    assert current.temporal_status == TemporalStatus.CURRENT
    assert current.evidence_type == EvidenceType.DIRECT


def test_negated_and_planned_context_stay_with_their_clauses():
    result = analyze_case(
        "P002",
        "My father does not have trouble walking, but he plans to use a wheelchair.",
    )

    assert len(result.case.evidence) == 2

    negated, planned = result.case.evidence

    assert negated.claim == "Person reports difficulty walking."
    assert negated.evidence_type == EvidenceType.CONTRADICTED
    assert negated.temporal_status == TemporalStatus.CURRENT

    assert planned.claim == "Person uses a mobility aid."
    assert planned.evidence_type == EvidenceType.DIRECT
    assert planned.temporal_status == TemporalStatus.PLANNED


def test_uncertain_and_current_context_stay_with_their_clauses():
    result = analyze_case(
        "P003",
        "My father might have trouble walking, but he currently uses a wheelchair.",
    )

    assert len(result.case.evidence) == 2

    uncertain, current = result.case.evidence

    assert uncertain.claim == "Person reports difficulty walking."
    assert uncertain.evidence_type == EvidenceType.INFERRED
    assert uncertain.temporal_status == TemporalStatus.CURRENT

    assert current.claim == "Person uses a mobility aid."
    assert current.evidence_type == EvidenceType.DIRECT
    assert current.temporal_status == TemporalStatus.CURRENT
