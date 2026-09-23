from app.schemas.evidence import Evidence
from app.reasoning.relationships import EvidenceRelationship


def build_explanation(
    claims,
    evidence: list[Evidence],
    relationships: list[EvidenceRelationship],
) -> list[str]:
    evidence_by_id = {
        item.evidence_id: item
        for item in evidence
    }

    explanation: list[str] = []

    for claim in claims:
        status = claim.status.value

        explanation.append(
            f'Claim "{claim.claim}" is {status}.'
        )

        linked = [
            evidence_by_id[evidence_id]
            for evidence_id in claim.evidence_ids
            if evidence_id in evidence_by_id
        ]

        direct = [
            item
            for item in linked
            if item.evidence_type.value == "DIRECT"
        ]

        inferred = [
            item
            for item in linked
            if item.evidence_type.value == "INFERRED"
        ]

        contradicted = [
            item
            for item in linked
            if item.evidence_type.value == "CONTRADICTED"
        ]

        if direct:
            ids = ", ".join(item.evidence_id for item in direct)
            explanation.append(
                f"Direct evidence: {ids}."
            )

        if inferred:
            ids = ", ".join(item.evidence_id for item in inferred)
            explanation.append(
                f"Inferred evidence: {ids}."
            )

        if contradicted:
            ids = ", ".join(
                item.evidence_id
                for item in contradicted
            )
            explanation.append(
                f"Contradicting evidence: {ids}."
            )

    for relationship in relationships:
        explanation.append(
            f"{relationship.source_evidence_id} "
            f"{relationship.relationship.value} "
            f"{relationship.target_evidence_id}."
        )

    return explanation
