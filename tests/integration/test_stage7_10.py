from __future__ import annotations

import asyncio

from forge.agents.design import DesignAgent
from forge.agents.docs import DocsAgent
from forge.agents.maintenance import MaintenanceAgent
from forge.agents.research import WideResearchMode
from forge.mail.receiver import MailForgeReceiver
from forge.platform.white_label import WhiteLabelConfig, apply_white_label
from forge.rag.collective_brain import CollectiveBrain
from forge.scheduler.tasks import SCHEDULED_TASKS


def test_stage7_white_label_config() -> None:
    config = WhiteLabelConfig(
        agency_id="agency-1",
        custom_domain="clients.example.com",
        brand_logo_url="https://example.com/logo.png",
        brand_colors={"primary": "#111827", "accent": "#facc15"},
        custom_email_from="forge@example.com",
    )
    applied = apply_white_label(config)
    assert applied["domain"] == "clients.example.com"


def test_stage8_agents_scaffold() -> None:
    async def _run() -> None:
        maintenance = MaintenanceAgent()
        docs = DocsAgent()
        result = await maintenance.run_nightly_scan("p1", "https://app.local")
        doc = await docs.generate_on_commit("diff")
        assert result["status"] == "healthy"
        assert "Auto Docs Update" in doc

    asyncio.run(_run())


def test_stage9_scaffold_features() -> None:
    async def _run() -> None:
        research = WideResearchMode()
        design = DesignAgent()
        receiver = MailForgeReceiver()

        report = await research.research("auth dependencies", depth=3)
        spec = await design.extract_spec_from_screenshot(b"fake")
        built = await design.build_from_spec(spec)
        score = await design.visual_verify(b"img", "http://localhost")
        inbound = await receiver.process_inbound({"subject": "Build auth flow", "body": "Please start"})

        assert "angle 1" in report
        assert spec["pass"] == 1
        assert "Built UI" in built
        assert score >= 0.88
        assert inbound["status"] == "accepted"

    asyncio.run(_run())


def test_stage10_collective_brain() -> None:
    brain = CollectiveBrain()
    brain.contribute_build_patterns("project-1", {"fixed": "auth bug"})
    brain.update_skill("supabase-auth", {"improvement": "add callback checks"})

    assert len(brain.patterns) == 1
    assert "supabase-auth" in brain.skill_updates
    assert len(SCHEDULED_TASKS) >= 3
