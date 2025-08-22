from .detectors.dns_exfiltration import DnsExfiltrationDetector
from .detectors.markdown_exfiltration import MarkdownImageExfiltrationDetector
from .schemas import AnalysisResult


class PromptAnalyzer:
    def __init__(self):
        self._detectors = [
            MarkdownImageExfiltrationDetector(),
            DnsExfiltrationDetector(),
        ]

    def analyze(self, prompt: str) -> AnalysisResult:
        all_vulnerabilities = []
        for detector in self._detectors:
            all_vulnerabilities.extend(detector.run(prompt))

        return AnalysisResult(vulnerabilities=all_vulnerabilities)
