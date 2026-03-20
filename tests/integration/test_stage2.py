from __future__ import annotations

import uuid

from forge.agents.architect import ArchitectAgent
from forge.agents.pm_agent import PMAgent
from forge.core.state import make_initial_state
from forge.skills.loader import SkillLoader


def test_stage2_skill_loader_metadata() -> None:
	skills = SkillLoader().load_all_metadata()
	assert len(skills) >= 10
	ids = {skill.id for skill in skills}
	assert "supabase-auth" in ids
	assert "dashboard-layout" in ids


def test_stage2_pm_architect_skill_assignments() -> None:
	state = make_initial_state(
		project_id=str(uuid.uuid4()),
		user_id="stage2-user",
		session_id=str(uuid.uuid4()),
		user_input="Build a SaaS dashboard with auth and subscription billing",
		total_allocated_tokens=4000,
	)

	state = PMAgent().run(state)
	state = ArchitectAgent().run(state)

	assert state.prd is not None
	assert state.tech_spec is not None
	assert "supabase-auth.skill.md" in state.prd.skill_hints
	assignments = state.tech_spec.skill_assignments
	assert any(value == "supabase-auth.skill.md" for value in assignments.values())
	assert any(value == "stripe-subscriptions.skill.md" for value in assignments.values())
