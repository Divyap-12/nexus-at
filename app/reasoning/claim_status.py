from enum import Enum

from app.schemas.evidence import Evidence


class ClaimStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    CONFLICTING = "CONFLICTING"
    CONTRADICTED = "CONTRADICTED"
    UNCERTAIN = "UNCERTAIN"
    HISTORICAL = "HISTORICAL"
    MIXED = "MIXED"


def determine_claim_status(evidence: list[Evidence]) -> ClaimStatus:
    if not evidence:
        raise ValueError("At least one evidence item is required.")

    types = {item.evidence_type.value for item in evidence}
    temporal_statuses = {item.temporal_status.value for item in evidence}

    if "DIRECT" in types and "CONTRADICTED" in types:
        return ClaimStatus.CONFLICTING

    if types == {"CONTRADICTED"}:
        return ClaimStatus.CONTRADICTED

    if types == {"INFERRED"}:
        return ClaimStatus.UNCERTAIN

    if "DIRECT" in types and "INFERRED" in types:
        return ClaimStatus.MIXED

    if temporal_statuses == {"HISTORICAL"}:
        return ClaimStatus.HISTORICAL

    return ClaimStatus.SUPPORTED
