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
    evidence_ids: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


class AnalysisResult(BaseModel):
    status: AnalysisStatus
    case: Case
    relationships: list[EvidenceRelationship] = []
    claims: list[ClaimAssessment] = []
    summary: CaseSummaryStatus = CaseSummaryStatus.INCONCLUSIVE
    explanation: list[str] = []
