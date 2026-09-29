from app.pipeline import analyze_case


def test_recurrence_reuses_previous_compatible_claim():
    result = analyze_case(
        "RC001",
        "My father struggles to walk. "
        "He does not struggle to walk. "
        "But now he struggles again.",
    )

    assert len(result.case.evidence) == 3

    current = result.case.evidence[-1]

    assert current.claim == "Person reports difficulty walking."
    assert current.temporal_status.value == "CURRENT"
    assert current.evidence_type.value == "DIRECT"


def test_recurrence_without_previous_claim_creates_no_evidence():
    result = analyze_case(
        "RC002",
        "But now he struggles again.",
    )

    assert len(result.case.evidence) == 0
