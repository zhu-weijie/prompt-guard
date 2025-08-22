from pydantic import BaseModel, Field


class Vulnerability(BaseModel):
    category: str = Field(
        ..., description="The type of vulnerability, e.g., 'Data Exfiltration'."
    )
    description: str = Field(
        ..., description="A detailed explanation of the vulnerability."
    )
    confidence: float = Field(
        ..., description="The confidence level of the finding (0.0 to 1.0)."
    )


class AnalysisResult(BaseModel):
    vulnerabilities: list[Vulnerability] = Field(
        default_factory=list, description="A list of vulnerabilities found."
    )


class PromptRequest(BaseModel):
    prompt: str
