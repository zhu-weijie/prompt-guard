from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..analysis.analyzer import PromptAnalyzer
from ..analysis.schemas import AnalysisResult, PromptRequest

app = FastAPI(title="PromptGuard API")
analyzer = PromptAnalyzer()

app.mount(
    "/static", StaticFiles(directory="src/prompt_guard/api/static"), name="static"
)

templates = Jinja2Templates(directory="src/prompt_guard/api/templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze", response_model=AnalysisResult)
def analyze_prompt(request: PromptRequest) -> AnalysisResult:
    result = analyzer.analyze(request.prompt)
    return result
