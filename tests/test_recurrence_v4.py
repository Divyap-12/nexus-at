from app.pipeline import analyze_case


def test_recurrence_can_refer_to_returned_walking_problem():
    result = analyze_case(
        "RV401",
        "My father struggles to walk. "
        "His walking problem has returned.",
    )

    assert len(result.case.evidence) == 2

    current = result.case.evidence[-1]

    assert current.claim == "Person reports difficulty walking."
    assert current.functional_domain.value == "MOBILITY"
    assert current.temporal_status.value == "CURRENT"


def test_recurrence_does_not_guess_between_multiple_previous_claims():
    result = analyze_case(
        "RV402",
        "My father struggles to walk. "
        "He uses a wheelchair. "
        "The problem has returned.",
    )

    assert len(result.case.evidence) == 2


def test_recurrence_can_refer_to_returned_issue():
    result = analyze_case(
        "RV403",
        "My father struggles to walk. "
        "The issue has returned.",
    )

    assert len(result.case.evidence) == 2

    current = result.case.evidence[-1]

    assert current.claim == "Person reports difficulty walking."
    assert current.functional_domain.value == "MOBILITY"


def test_existing_explicit_recurrence_still_works():
    result = analyze_case(
        "RV404",
        "My father struggles to walk. "
        "He struggles again.",
    )

    assert len(result.case.evidence) == 2

    current = result.case.evidence[-1]

    assert current.claim == "Person reports difficulty walking."
from app.pipeline import analyze_case


def test_reference_recurrence_without_previous_claim_creates_no_evidence():
    result = analyze_case(
        "RV405",
        "The problem has returned.",
    )

    assert len(result.case.evidence) == 0


def test_reference_recurrence_does_not_copy_unrelated_previous_claim():
    result = analyze_case(
        "RV406",
        "My father uses a wheelchair. "
        "The problem has returned.",
    )

    assert len(result.case.evidence) == 1


def test_reference_recurrence_prefers_unique_compatible_claim():
    result = analyze_case(
        "RV407",
        "My father struggles to walk. "
        "He uses a wheelchair. "
        "The walking problem has returned.",
    )

    assert len(result.case.evidence) == 3

    current = result.case.evidence[-1]

    assert current.claim == "Person reports difficulty walking."
    assert current.functional_domain.value == "MOBILITY"
