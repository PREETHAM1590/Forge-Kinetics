from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RecallMemory:
    """Local recall memory scaffold to emulate Redis/Mem0 behavior."""

    sessions: dict[str, list[str]] = field(default_factory=dict)

    async def store_session(self, session_id: str, summary: str, user_id: str) -> None:
        key = f"{user_id}:{session_id}"
        self.sessions.setdefault(key, []).append(summary)

    async def get_recent_context(self, user_id: str) -> str:
        collected: list[str] = []
        prefix = f"{user_id}:"
        for key, summaries in self.sessions.items():
            if key.startswith(prefix):
                collected.extend(summaries)
        return "\n".join(collected[-10:])
