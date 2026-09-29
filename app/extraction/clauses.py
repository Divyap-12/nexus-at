import re


def split_clauses(text: str) -> list[str]:
    clauses: list[str] = []

    for sentence in text.split("."):
        sentence = sentence.strip()

        if not sentence:
            continue

        parts = [
            part.strip()
            for part in re.split(
                r"\bbut\b",
                sentence,
                flags=re.IGNORECASE,
            )
            if part.strip()
        ]

        clauses.extend(parts)

    return clauses
