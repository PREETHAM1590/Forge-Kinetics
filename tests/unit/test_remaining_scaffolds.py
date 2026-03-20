from __future__ import annotations

import asyncio
import uuid

import pytest

from forge.core.state import make_initial_state
from forge.finops.tracker import TokenUsageTracker
from forge.hitl.payload import build_hitl_payload
from forge.memory.archival import ArchivalMemory
from forge.memory.compressor import compress_summary
from forge.memory.core import MemoryCore
from forge.rag.differential_privacy import add_noise
from forge.rag.domain import select_domain
from forge.scheduler.workers import run_scheduled_tasks
from forge.skills.registry import SkillRegistry


def test_api_health_and_projects_route() -> None:
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from forge.api.main import create_app

    app = create_app()
    client = TestClient(app)

    health = client.get("/health")
    assert health.status_code == 200

    created = client.post("/api/projects", json={"name": "Forge Project"})
    assert created.status_code == 200
    project_id = created.json()["project_id"]

    fetched = client.get(f"/api/projects/{project_id}")
    assert fetched.status_code == 200


def test_token_usage_tracker() -> None:
    tracker = TokenUsageTracker(total_allocated=100)
    state = tracker.record("pm_agent", 70)
    assert state["is_exceeded"] is False

    state = tracker.record("architect_agent", 40)
    assert state["is_exceeded"] is True


def test_hitl_payload_builder() -> None:
    state = make_initial_state(
        project_id=str(uuid.uuid4()),
        user_id="u1",
        session_id=str(uuid.uuid4()),
        user_input="Build dashboard",
        total_allocated_tokens=1000,
    )
    payload = build_hitl_payload(state)
    assert payload.project_id == state.project_id


def test_memory_helpers() -> None:
    async def _run() -> None:
        core = MemoryCore()
        await core.put("k1", "v1")
        assert await core.get("k1") == "v1"

        archival = ArchivalMemory()
        await archival.archive("ns", "entry")
        records = await archival.query("ns")
        assert records == ["entry"]

    asyncio.run(_run())

    summary = compress_summary("hello world", max_chars=20)
    assert summary == "hello world"


def test_rag_helpers_and_scheduler() -> None:
    assert select_domain("stripe billing webhook") == "billing"
    assert isinstance(add_noise(10.0, epsilon=1.0), float)

    async def _run() -> None:
        results = await run_scheduled_tasks()
        assert len(results) >= 3

    asyncio.run(_run())


def test_skill_registry_lookup() -> None:
    registry = SkillRegistry()
    all_skills = registry.all()
    assert len(all_skills) >= 10
    assert registry.by_id("supabase-auth") is not None
