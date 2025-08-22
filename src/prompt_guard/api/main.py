from fastapi import FastAPI

from ..analysis.analyzer import PromptAnalyzer
from ..analysis.schemas import AnalysisResult, PromptRequest

app = FastAPI(title="PromptGuard API")
analyzer = PromptAnalyzer()


@app.get("/")
def read_root():
    return {"message": "Welcome to the PromptGuard API"}


@app.post("/analyze", response_model=AnalysisResult)
def analyze_prompt(request: PromptRequest) -> AnalysisResult:
    result = analyzer.analyze(request.prompt)
    return result
