from pydantic import BaseModel, Field

from app.schemas.evidence import Evidence


class Case(BaseModel):
    case_id: str = Field(min_length=1)
    narrative: str = Field(min_length=1)
    evidence: list[Evidence] = Field(default_factory=list)
