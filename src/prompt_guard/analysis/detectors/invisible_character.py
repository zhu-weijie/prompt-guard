import unicodedata
from typing import Iterator

from ..schemas import Vulnerability

INVISIBLE_CATEGORIES = ("Cf", "Cc", "Zs")
ALLOWED_CHARS = (" ", "\n", "\r")


class InvisibleCharacterDetector:
    def run(self, prompt: str) -> Iterator[Vulnerability]:
        for i, char in enumerate(prompt):
            if char in ALLOWED_CHARS:
                continue

            category = unicodedata.category(char)
            if category in INVISIBLE_CATEGORIES:
                yield Vulnerability(
                    category="Obfuscation",
                    description=(
                        f"An invisible or non-printable character was found at "
                        f"position {i}. This could be an attempt to hide malicious"
                        f" instructions. Character: '{char}' (U+{ord(char):04X}), "
                        f"Category: {category}."
                    ),
                    confidence=0.9,
                )
                break
