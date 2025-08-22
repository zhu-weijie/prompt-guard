from .schemas import AnalysisResult, Vulnerability


class PromptAnalyzer:
    def analyze(self, prompt: str) -> AnalysisResult:
        if "test" in prompt.lower():
            dummy_vulnerability = Vulnerability(
                category="Placeholder",
                description="This is a dummy vulnerability for testing purposes.",
                confidence=0.9,
            )
            return AnalysisResult(vulnerabilities=[dummy_vulnerability])

        return AnalysisResult()
