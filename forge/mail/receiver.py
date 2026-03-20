from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MailForgeReceiver:
    async def process_inbound(self, email: dict) -> dict:
        subject = email.get("subject", "")
        body = email.get("body", "")
        intent = (subject + " " + body).strip() or "No intent detected"
        return {
            "status": "accepted",
            "intent": intent,
            "trigger": "pm_agent",
        }
