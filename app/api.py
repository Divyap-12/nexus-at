from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.pipeline import analyze_case


app = FastAPI(
    title="Nexus-AT",
    description="Evidence and claim analysis engine",
    version="0.1.0",
)


class AnalysisRequest(BaseModel):
    case_id: str
    narrative: str


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/analyze")
def analyze(request: AnalysisRequest):
    result = analyze_case(
        request.case_id,
        request.narrative,
    )

    return result.model_dump(mode="json")
