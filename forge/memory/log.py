from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class MemoryLog:
	events: list[dict[str, Any]] = field(default_factory=list)

	async def append(self, event: str, payload: dict[str, Any]) -> None:
		self.events.append(
			{
				"event": event,
				"payload": payload,
				"timestamp": datetime.now(tz=timezone.utc).isoformat(),
			}
		)

