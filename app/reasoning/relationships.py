from dataclasses import dataclass
from enum import Enum


class RelationshipType(str, Enum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    TEMPORALLY_DISTINCT = "TEMPORALLY_DISTINCT"
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
    source_temporal_status: str = "CURRENT",
    target_temporal_status: str = "CURRENT",
) -> EvidenceRelationship:

    if source_claim != target_claim:
        relationship = RelationshipType.UNRELATED

    elif source_temporal_status != target_temporal_status:
        relationship = RelationshipType.TEMPORALLY_DISTINCT

    elif (
        source_type == "CONTRADICTED"
        or target_type == "CONTRADICTED"
    ):
        relationship = RelationshipType.CONTRADICTS

    else:
        relationship = RelationshipType.SUPPORTS

    return EvidenceRelationship(
        source_evidence_id=source_evidence_id,
        target_evidence_id=target_evidence_id,
        relationship=relationship,
    )
