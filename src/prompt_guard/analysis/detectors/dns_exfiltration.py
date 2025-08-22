import re
from typing import Iterator

from ..schemas import Vulnerability

DNS_COMMAND_PATTERN = re.compile(
    r"\b(nslookup|dig|host|ping)\s+.*[$\(`'" "]", re.IGNORECASE
)


class DnsExfiltrationDetector:
    def run(self, prompt: str) -> Iterator[Vulnerability]:
        matches = DNS_COMMAND_PATTERN.finditer(prompt)
        for match in matches:
            command_found = match.group(0).strip()
            yield Vulnerability(
                category="Data Exfiltration",
                description=(
                    "A command known for DNS lookups was found with suspicious "
                    "patterns, suggesting data could be exfiltrated via DNS queries. "
                    f"Command snippet found: `{command_found}`"
                ),
                confidence=0.7,
            )
