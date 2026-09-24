from dataclasses import dataclass
from enum import Enum


class RelationshipType(str, Enum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    UNRELATED = "UNRELATED"


@dataclass(frozen=True)
class EvidenceRelationship:
    source_evidence_id: str
    target_evidence_id: str
    relationship: RelationshipType


def compare_evidence(
    source_evidence_id: str,
    source_claim: str,
    source_type: str,
    target_evidence_id: str,
    target_claim: str,
    target_type: str,
) -> EvidenceRelationship:
    if source_claim != target_claim:
        return EvidenceRelationship(
            source_evidence_id=source_evidence_id,
            target_evidence_id=target_evidence_id,
            relationship=RelationshipType.UNRELATED,
        )

    if (
        source_type == "CONTRADICTED"
        or target_type == "CONTRADICTED"
    ):
        return EvidenceRelationship(
            source_evidence_id=source_evidence_id,
            target_evidence_id=target_evidence_id,
            relationship=RelationshipType.CONTRADICTS,
        )

    return EvidenceRelationship(
        source_evidence_id=source_evidence_id,
        target_evidence_id=target_evidence_id,
        relationship=RelationshipType.SUPPORTS,
    )