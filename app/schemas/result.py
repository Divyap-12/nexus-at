from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.case import Case
from app.schemas.evidence import FunctionalDomain
from app.reasoning.claim_status import ClaimStatus
from app.reasoning.case_summary import CaseSummaryStatus
from app.reasoning.relationships import EvidenceRelationship


class AnalysisStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class ClaimAssessment(BaseModel):
    claim: str
    status: ClaimStatus
    functional_domain: FunctionalDomain
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float


class AnalysisResult(BaseModel):
    status: AnalysisStatus
    case: Case
    relationships: list[EvidenceRelationship] = Field(default_factory=list)
    claims: list[ClaimAssessment] = Field(default_factory=list)
    summary: CaseSummaryStatus = CaseSummaryStatus.INCONCLUSIVE
