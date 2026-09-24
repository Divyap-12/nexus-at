from enum import Enum

from pydantic import BaseModel, Field


class EvidenceType(str, Enum):
    DIRECT = "DIRECT"
    OBSERVED = "OBSERVED"
    DOCUMENTED = "DOCUMENTED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"
    CONTRADICTED = "CONTRADICTED"


class EvidenceStrength(str, Enum):
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    WEAK = "WEAK"


class FunctionalDomain(str, Enum):
    MOBILITY = "MOBILITY"
    VISION = "VISION"
    HEARING = "HEARING"
    COMMUNICATION = "COMMUNICATION"
    COGNITION = "COGNITION"
    SELF_CARE = "SELF_CARE"
    MULTIPLE = "MULTIPLE"
    UNKNOWN = "UNKNOWN"


class TemporalStatus(str, Enum):
    CURRENT = "CURRENT"
    RECENT = "RECENT"
    HISTORICAL = "HISTORICAL"
    PLANNED = "PLANNED"
    UNKNOWN = "UNKNOWN"


class Evidence(BaseModel):
    evidence_id: str
    text_span: str = Field(min_length=1)
    source_text: str = Field(min_length=1)
    claim: str = Field(min_length=1)

    evidence_type: EvidenceType
    strength: EvidenceStrength
    functional_domain: FunctionalDomain
    temporal_status: TemporalStatus

    confidence: float = Field(ge=0.0, le=1.0)
