from app.pipeline import analyze_case


def test_recurrence_can_refer_to_previous_claim_without_repeating_keyword():
    result = analyze_case(
        "RV301",
        "My father struggles to walk. "
        "The problem has returned.",
    )

    assert len(result.case.evidence) == 2

    current = result.case.evidence[-1]

    assert current.claim == "Person reports difficulty walking."
    assert current.functional_domain.value == "MOBILITY"
    assert current.temporal_status.value == "CURRENT"


def test_recurrence_does_not_guess_when_multiple_claims_are_ambiguous():
    result = analyze_case(
        "RV302",
        "My father struggles to walk. "
        "He uses a wheelchair. "
        "The problem has returned.",
    )

    assert len(result.case.evidence) == 2


def test_recurrence_still_supports_existing_explicit_pattern():
    result = analyze_case(
        "RV303",
        "My father struggles to walk. "
        "He struggles again.",
    )

    assert len(result.case.evidence) == 2

    current = result.case.evidence[-1]

    assert current.claim == "Person reports difficulty walking."
