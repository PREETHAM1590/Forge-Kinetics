from __future__ import annotations


def compress_summary(text: str, max_chars: int = 500) -> str:
	normalized = " ".join(text.split())
	if len(normalized) <= max_chars:
		return normalized
	return normalized[: max_chars - 3] + "..."

