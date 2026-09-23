from app.pipeline import analyze_case
from app.schemas.evidence import EvidenceType, TemporalStatus
from app.schemas.result import AnalysisStatus
from app.reasoning.relationships import (
    RelationshipType,
    compare_evidence,
)


def test_current_mobility_evidence():
    result = analyze_case(
        "C001",
        "My father is struggling to walk and uses a walking stick.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 2


def test_historical_mobility_evidence():
    result = analyze_case(
        "C002",
        "My father used to struggle to walk.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 1

    evidence = result.case.evidence[0]

    assert evidence.temporal_status == TemporalStatus.HISTORICAL
    assert evidence.evidence_type == EvidenceType.DIRECT
    assert evidence.confidence == 0.95


def test_negated_mobility_evidence():
    result = analyze_case(
        "C003",
        "My father does not struggle to walk.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 1

    evidence = result.case.evidence[0]

    assert evidence.evidence_type == EvidenceType.CONTRADICTED
    assert evidence.temporal_status == TemporalStatus.CURRENT
    assert evidence.confidence == 0.95


def test_uncertain_mobility_evidence():
    result = analyze_case(
        "C004",
        "My father may have difficulty walking.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 1

    evidence = result.case.evidence[0]

    assert evidence.evidence_type == EvidenceType.INFERRED
    assert evidence.confidence == 0.60


def test_planned_mobility_evidence():
    result = analyze_case(
        "C005",
        "My father is planning to use a wheelchair.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 1

    evidence = result.case.evidence[0]

    assert evidence.temporal_status == TemporalStatus.PLANNED
    assert evidence.confidence == 0.90


def test_unrelated_narrative():
    result = analyze_case(
        "C006",
        "My father enjoys reading newspapers every morning.",
    )

    assert result.status == AnalysisStatus.PARTIAL
    assert result.case.evidence == []


def test_sentence_level_contexts():
    result = analyze_case(
        "C007",
        "My father used to struggle to walk. He is planning to use a wheelchair.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 2

    historical = result.case.evidence[0]
    planned = result.case.evidence[1]

    assert historical.temporal_status == TemporalStatus.HISTORICAL
    assert historical.confidence == 0.95

    assert planned.temporal_status == TemporalStatus.PLANNED
    assert planned.confidence == 0.90


def test_unrelated_sentence_does_not_inherit_context():
    result = analyze_case(
        "C008",
        "My father used to struggle to walk. He enjoys reading newspapers.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 1

    evidence = result.case.evidence[0]

    assert evidence.temporal_status == TemporalStatus.HISTORICAL
    assert evidence.source_text == "My father used to struggle to walk"


def test_direct_and_contradicted_evidence_conflict():
    relationship = compare_evidence(
        "E001",
        "Person reports difficulty walking.",
        "DIRECT",
        "E002",
        "Person reports difficulty walking.",
        "CONTRADICTED",
    )

    assert relationship.relationship == RelationshipType.CONTRADICTS


def test_different_claims_are_unrelated():
    relationship = compare_evidence(
        "E001",
        "Person reports difficulty walking.",
        "DIRECT",
        "E002",
        "Person uses a mobility aid.",
        "DIRECT",
    )

    assert relationship.relationship == RelationshipType.UNRELATED


def test_same_direct_claim_supports():
    relationship = compare_evidence(
        "E001",
        "Person reports difficulty walking.",
        "DIRECT",
        "E002",
        "Person reports difficulty walking.",
        "DIRECT",
    )

    assert relationship.relationship == RelationshipType.SUPPORTS
def test_contradictory_sentences_create_relationship():
    result = analyze_case(
        "C011",
        "My father struggles to walk. My father does not struggle to walk.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 2
    assert len(result.relationships) == 1

    first = result.case.evidence[0]
    second = result.case.evidence[1]
    relationship = result.relationships[0]

    assert first.evidence_type == EvidenceType.DIRECT
    assert second.evidence_type == EvidenceType.CONTRADICTED

    assert relationship.source_evidence_id == first.evidence_id
    assert relationship.target_evidence_id == second.evidence_id
    assert relationship.relationship == RelationshipType.CONTRADICTS
from app.reasoning.aggregation import group_evidence_by_domain


def test_evidence_grouped_by_functional_domain():
    result = analyze_case(
        "C012",
        "My father struggles to walk. "
        "He uses a walking stick. "
        "He cannot walk long distances.",
    )

    grouped = group_evidence_by_domain(result.case.evidence)

    assert "MOBILITY" in grouped
    assert len(grouped["MOBILITY"]) == 3


def test_evidence_grouping_preserves_evidence_ids():
    result = analyze_case(
        "C013",
        "My father struggles to walk. "
        "He uses a wheelchair.",
    )

    grouped = group_evidence_by_domain(result.case.evidence)

    mobility = grouped["MOBILITY"]

    assert [item.evidence_id for item in mobility] == [
        "C013-E001",
        "C013-E002",
    ]
from app.pipeline import analyze_case
from app.reasoning.claims import group_evidence_by_claim
from app.reasoning.claim_status import (
    ClaimStatus,
    determine_claim_status,
)


def test_supported_claim():
    result = analyze_case(
        "C016",
        "My father struggles to walk. He cannot walk long distances.",
    )

    groups = group_evidence_by_claim(result.case.evidence)

    status = determine_claim_status(
        groups["Person reports difficulty walking."]
    )

    assert status == ClaimStatus.SUPPORTED


def test_conflicting_claim():
    result = analyze_case(
        "C017",
        "My father struggles to walk. My father does not struggle to walk.",
    )

    groups = group_evidence_by_claim(result.case.evidence)

    status = determine_claim_status(
        groups["Person reports difficulty walking."]
    )

    assert status == ClaimStatus.CONFLICTING


def test_contradicted_claim():
    result = analyze_case(
        "C018",
        "My father does not struggle to walk.",
    )

    groups = group_evidence_by_claim(result.case.evidence)

    status = determine_claim_status(
        groups["Person reports difficulty walking."]
    )

    assert status == ClaimStatus.CONTRADICTED


def test_uncertain_claim():
    result = analyze_case(
        "C019",
        "My father may have difficulty walking.",
    )

    groups = group_evidence_by_claim(result.case.evidence)

    status = determine_claim_status(
        groups["Person reports difficulty walking."]
    )

    assert status == ClaimStatus.UNCERTAIN


def test_historical_claim():
    result = analyze_case(
        "C020",
        "My father used to struggle to walk.",
    )

    groups = group_evidence_by_claim(result.case.evidence)

    status = determine_claim_status(
        groups["Person reports difficulty walking."]
    )

    assert status == ClaimStatus.HISTORICAL
from app.pipeline import analyze_case
from app.reasoning.case_summary import (
    CaseSummaryStatus,
    determine_case_summary,
)


def test_case_summary_supported():
    result = analyze_case(
        "C024",
        "My father struggles to walk. He uses a walking stick.",
    )

    summary = determine_case_summary(result.claims)

    assert summary == CaseSummaryStatus.SUPPORTED


def test_case_summary_conflicting():
    result = analyze_case(
        "C025",
        "My father struggles to walk. My father does not struggle to walk.",
    )

    summary = determine_case_summary(result.claims)

    assert summary == CaseSummaryStatus.CONFLICTING


def test_case_summary_historical():
    result = analyze_case(
        "C026",
        "My father used to struggle to walk.",
    )

    summary = determine_case_summary(result.claims)

    assert summary == CaseSummaryStatus.HISTORICAL


def test_case_summary_uncertain():
    result = analyze_case(
        "C027",
        "My father may have difficulty walking.",
    )

    summary = determine_case_summary(result.claims)

    assert summary == CaseSummaryStatus.UNCERTAIN


def test_case_summary_mixed():
    result = analyze_case(
        "C028",
        "My father struggles to walk. He may have difficulty walking.",
    )

    summary = determine_case_summary(result.claims)

    assert summary == CaseSummaryStatus.MIXED
def test_full_analysis_result_contains_summary():
    result = analyze_case(
        "C029",
        "My father struggles to walk. He may have difficulty walking.",
    )

    assert result.status == AnalysisStatus.SUCCESS
    assert len(result.case.evidence) == 2
    assert len(result.claims) == 1
    assert result.claims[0].status == ClaimStatus.MIXED
    assert result.summary == CaseSummaryStatus.MIXED
