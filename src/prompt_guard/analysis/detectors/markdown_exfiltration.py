import re
from typing import Iterator

from ..schemas import Vulnerability

MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[.*?\]\((https?://.*?)\)")


class MarkdownImageExfiltrationDetector:
    def run(self, prompt: str) -> Iterator[Vulnerability]:
        matches = MARKDOWN_IMAGE_PATTERN.finditer(prompt)
        for match in matches:
            url = match.group(1)
            yield Vulnerability(
                category="Data Exfiltration",
                description=(
                    "A Markdown image tag was found with a remote URL. "
                    "This can be used to exfiltrate data if the prompt is rendered "
                    f"by another system or user. URL found: {url}"
                ),
                confidence=0.8,
            )
