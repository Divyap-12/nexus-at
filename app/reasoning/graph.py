from app.schemas.evidence import Evidence
from app.reasoning.relationships import EvidenceRelationship, compare_evidence


def build_relationships(
    evidence: list[Evidence],
) -> list[EvidenceRelationship]:
    relationships: list[EvidenceRelationship] = []

    for index, source in enumerate(evidence):
        for target in evidence[index + 1:]:
            relationship = compare_evidence(
                source_evidence_id=source.evidence_id,
                source_claim=source.claim,
                source_type=source.evidence_type.value,
                target_evidence_id=target.evidence_id,
                target_claim=target.claim,
                target_type=target.evidence_type.value,
            )

            if relationship.relationship.value != "UNRELATED":
                relationships.append(relationship)

    return relationships
