from app.pipeline import analyze_case
from tests.evaluation.cases import EVALUATION_CASES


def main() -> None:
    passed = 0
    failed = 0

    print()
    print("NEXUS-AT EVALUATION")
    print("=" * 50)

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

        checks = (
            len(evidence) == case.expected_evidence_count,
            actual_claims == case.expected_claims,
            actual_temporal_statuses == case.expected_temporal_statuses,
            actual_evidence_types == case.expected_evidence_types,
        )

        if all(checks):
            print(f"{case.case_id}  PASS")
            passed += 1
        else:
            print(f"{case.case_id}  FAIL")
            failed += 1

            print(
                f"  Expected evidence count: "
                f"{case.expected_evidence_count}"
            )
            print(
                f"  Actual evidence count:   "
                f"{len(evidence)}"
            )

            print(
                f"  Expected claims: "
                f"{case.expected_claims}"
            )
            print(
                f"  Actual claims:   "
                f"{actual_claims}"
            )

            print(
                f"  Expected temporal: "
                f"{case.expected_temporal_statuses}"
            )
            print(
                f"  Actual temporal:   "
                f"{actual_temporal_statuses}"
            )

            print(
                f"  Expected types: "
                f"{case.expected_evidence_types}"
            )
            print(
                f"  Actual types:   "
                f"{actual_evidence_types}"
            )

    total = passed + failed
    pass_rate = (passed / total * 100) if total else 0.0

    print()
    print("=" * 50)
    print(f"Cases evaluated: {total}")
    print(f"Passed:          {passed}")
    print(f"Failed:          {failed}")
    print(f"Pass rate:       {pass_rate:.1f}%")
    print("=" * 50)


if __name__ == "__main__":
    main()
