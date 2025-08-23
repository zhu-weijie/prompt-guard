from src.prompt_guard.analysis.detectors.invisible_character import (
    InvisibleCharacterDetector,
)


def test_invisible_char_positive_case():
    detector = InvisibleCharacterDetector()
    prompt = "ignore​this"
    vulnerabilities = list(detector.run(prompt))

    assert len(vulnerabilities) == 1
    vuln = vulnerabilities[0]
    assert vuln.category == "Obfuscation"
    assert "U+200B" in vuln.description


def test_invisible_char_negative_case():
    detector = InvisibleCharacterDetector()
    prompt = "This is a normal, safe prompt."
    vulnerabilities = list(detector.run(prompt))

    assert len(vulnerabilities) == 0


def test_invisible_char_handles_newlines_safely():
    detector = InvisibleCharacterDetector()
    prompt = "This is a safe prompt\nwith multiple lines."
    vulnerabilities = list(detector.run(prompt))

    assert len(vulnerabilities) == 0
