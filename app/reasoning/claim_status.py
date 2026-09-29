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

    direct_items = [
        item
        for item in evidence
        if item.evidence_type.value == "DIRECT"
    ]

    inferred_items = [
        item
        for item in evidence
        if item.evidence_type.value == "INFERRED"
    ]

    contradicted_items = [
        item
        for item in evidence
        if item.evidence_type.value == "CONTRADICTED"
    ]

    # Opposing evidence is only a conflict when it refers
    # to the same temporal context and there is no later
    # direct statement resolving that contradiction.
    if direct_items and contradicted_items:
        for contradicted in contradicted_items:
            same_temporal_directs = [
                direct
                for direct in direct_items
                if direct.temporal_status == contradicted.temporal_status
            ]

            if not same_temporal_directs:
                continue

            latest_direct = same_temporal_directs[-1]

            contradicted_index = evidence.index(contradicted)
            direct_index = evidence.index(latest_direct)

            # A later direct statement resolves the earlier
            # contradiction.
            if direct_index > contradicted_index:
                return ClaimStatus.SUPPORTED

            # Otherwise the current evidence genuinely conflicts.
            return ClaimStatus.CONFLICTING

        # Historical/current opposition is temporally distinct.
        return ClaimStatus.SUPPORTED

    if contradicted_items and not direct_items and not inferred_items:
        return ClaimStatus.CONTRADICTED

    if inferred_items and not direct_items and not contradicted_items:
        return ClaimStatus.UNCERTAIN

    if direct_items and inferred_items:
        return ClaimStatus.MIXED

    if all(
        item.temporal_status.value == "HISTORICAL"
        for item in evidence
    ):
        return ClaimStatus.HISTORICAL

    return ClaimStatus.SUPPORTED
