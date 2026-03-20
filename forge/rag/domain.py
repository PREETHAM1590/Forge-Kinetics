from __future__ import annotations


def select_domain(query: str) -> str:
	lowered = query.lower()
	if any(token in lowered for token in ["auth", "session", "login"]):
		return "auth"
	if any(token in lowered for token in ["billing", "stripe", "payment"]):
		return "billing"
	if any(token in lowered for token in ["pipeline", "agent", "langgraph"]):
		return "orchestration"
	return "general"

