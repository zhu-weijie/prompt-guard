import re
from typing import Iterator

from ..schemas import Vulnerability

SENSITIVE_FILES = (
    r"(settings\.json|\.bashrc|\.zshrc|\.profile|config\.toml|credentials)"
)
FILE_WRITE_PATTERN = re.compile(
    rf"(?:>|>>|sed|vim|nano|echo|cat)\s*.*?{SENSITIVE_FILES}", re.IGNORECASE
)


class ConfigFileWriteDetector:
    def run(self, prompt: str) -> Iterator[Vulnerability]:
        matches = FILE_WRITE_PATTERN.finditer(prompt)
        for match in matches:
            snippet = match.group(0).strip()
            filename = match.group(1)
            yield Vulnerability(
                category="Privilege Escalation",
                description=(
                    "An attempt to write to or edit a sensitive configuration file was "
                    f"detected. This could be an attempt to alter system behavior or "
                    f"escalate privileges. Sensitive file '{filename}' targeted in "
                    f"snippet: `{snippet}`"
                ),
                confidence=0.9,
            )
