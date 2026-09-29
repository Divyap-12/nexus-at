from app.pipeline import analyze_case
from tests.evaluation.cases import EVALUATION_CASES


def test_evaluation_cases_match_expected_output():
    failures = []

    for case in EVALUATION_CASES:
        result = analyze_case(case.case_id, case.narrative)
        evidence = result.case.evidence

        actual_claims = tuple(
            item.claim
            for item in evidence
        )

        actual_temporal_statuses = tuple(
            item.temporal_status.value
            for item in evidence
        )

        actual_evidence_types = tuple(
            item.evidence_type.value
            for item in evidence
        )

        if len(evidence) != case.expected_evidence_count:
            failures.append(
                f"{case.case_id}: evidence count "
                f"expected {case.expected_evidence_count}, "
                f"got {len(evidence)}"
            )

        if actual_claims != case.expected_claims:
            failures.append(
                f"{case.case_id}: claims "
                f"expected {case.expected_claims}, "
                f"got {actual_claims}"
            )

        if actual_temporal_statuses != case.expected_temporal_statuses:
            failures.append(
                f"{case.case_id}: temporal statuses "
                f"expected {case.expected_temporal_statuses}, "
                f"got {actual_temporal_statuses}"
            )

        if actual_evidence_types != case.expected_evidence_types:
            failures.append(
                f"{case.case_id}: evidence types "
                f"expected {case.expected_evidence_types}, "
                f"got {actual_evidence_types}"
            )

    assert not failures, "\n".join(failures)
