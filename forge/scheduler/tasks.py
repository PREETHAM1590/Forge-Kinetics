from __future__ import annotations

SCHEDULED_TASKS = [
    {"name": "nightly_maintenance", "cron": "0 2 * * *", "agent": "maintenance"},
    {"name": "weekly_report", "cron": "0 9 * * 1", "agent": "docs"},
    {"name": "monthly_billing", "cron": "0 9 1 * *", "agent": "finops"},
]
