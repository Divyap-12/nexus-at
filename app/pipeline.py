from app.extraction.context import ContextType, detect_context
from app.extraction.rules import find_matching_keyword, find_matching_rules
from app.reasoning.aggregation import group_evidence_by_domain
from app.reasoning.claim_status import determine_claim_status
from app.reasoning.claims import group_evidence_by_claim
from app.reasoning.graph import build_relationships
from app.reasoning.case_summary import determine_case_summary
from app.schemas.case import Case
from app.schemas.evidence import (
    Evidence,
    EvidenceType,
    FunctionalDomain,
    TemporalStatus,
)
from app.schemas.result import (
    AnalysisResult,
    AnalysisStatus,
    ClaimAssessment,
)


def _temporal_status(context: ContextType) -> TemporalStatus:
    if context == ContextType.HISTORICAL:
        return TemporalStatus.HISTORICAL

    if context == ContextType.PLANNED:
        return TemporalStatus.PLANNED

    return TemporalStatus.CURRENT


def _evidence_type(context: ContextType) -> EvidenceType:
    if context == ContextType.NEGATED:
        return EvidenceType.CONTRADICTED

    if context == ContextType.UNCERTAIN:
        return EvidenceType.INFERRED

    return EvidenceType.DIRECT


def _confidence(context: ContextType) -> float:
    if context == ContextType.NEGATED:
        return 0.95

    if context == ContextType.UNCERTAIN:
        return 0.60

    if context == ContextType.HISTORICAL:
        return 0.95

    if context == ContextType.PLANNED:
        return 0.90

    return 1.0


def _split_sentences(narrative: str) -> list[str]:
    return [
        sentence.strip()
        for sentence in narrative.split(".")
        if sentence.strip()
    ]


def _build_claim_assessments(
    evidence: list[Evidence],
) -> list[ClaimAssessment]:
    grouped = group_evidence_by_claim(evidence)

    assessments: list[ClaimAssessment] = []

    for claim, claim_evidence in grouped.items():
        confidence = max(
            item.confidence
            for item in claim_evidence
        )

        assessments.append(
            ClaimAssessment(
                claim=claim,
                status=determine_claim_status(claim_evidence),
                functional_domain=claim_evidence[0].functional_domain,
                evidence_ids=[
                    item.evidence_id
                    for item in claim_evidence
                ],
                evidence_types=[
                    item.evidence_type
                    for item in claim_evidence
                ],
                confidence=confidence,
            )
        )

    return assessments


def analyze_case(case_id: str, narrative: str) -> AnalysisResult:
    evidence: list[Evidence] = []

    for sentence in _split_sentences(narrative):
        rules = find_matching_rules(sentence)
        context = detect_context(sentence)

        for rule in rules:
            matched_text = find_matching_keyword(sentence, rule)

            evidence.append(
                Evidence(
                    evidence_id=f"{case_id}-E{len(evidence) + 1:03d}",
                    text_span=matched_text,
                    source_text=sentence,
                    claim=rule.claim,
                    evidence_type=_evidence_type(context),
                    functional_domain=FunctionalDomain(
                        rule.functional_domain
                    ),
                    temporal_status=_temporal_status(context),
                    confidence=_confidence(context),
                )
            )

    relationships = build_relationships(evidence)
    claims = _build_claim_assessments(evidence)
    summary = determine_case_summary(claims)

    status = (
        AnalysisStatus.SUCCESS
        if evidence
        else AnalysisStatus.PARTIAL
    )

    case = Case(
        case_id=case_id,
        narrative=narrative,
        evidence=evidence,
    )
    return AnalysisResult(
        status=status,
        case=case,
        relationships=relationships,
        claims=claims,
        summary=summary,
    )

