from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.pipeline import analyze_case


app = FastAPI(
    title="Nexus-AT",
    description="Evidence and claim analysis engine",
    version="0.2.0",
)


class AnalysisRequest(BaseModel):
    case_id: str = Field(min_length=1, max_length=100)
    narrative: str = Field(min_length=1, max_length=10000)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {
        "service": "Nexus-AT",
        "status": "healthy",
        "version": "0.2.0",
    }


@app.post("/analyze")
def analyze(request: AnalysisRequest):
    result = analyze_case(
        request.case_id,
        request.narrative,
    )

    return result.model_dump(mode="json")
