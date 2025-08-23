from .detectors.config_file_write import ConfigFileWriteDetector
from .detectors.dns_exfiltration import DnsExfiltrationDetector
from .detectors.invisible_character import InvisibleCharacterDetector
from .detectors.markdown_exfiltration import MarkdownImageExfiltrationDetector
from .schemas import AnalysisResult


class PromptAnalyzer:
    def __init__(self):
        self._detectors = [
            MarkdownImageExfiltrationDetector(),
            DnsExfiltrationDetector(),
            ConfigFileWriteDetector(),
            InvisibleCharacterDetector(),
        ]

    def analyze(self, prompt: str) -> AnalysisResult:
        all_vulnerabilities = []
        for detector in self._detectors:
            all_vulnerabilities.extend(detector.run(prompt))

        return AnalysisResult(vulnerabilities=all_vulnerabilities)
