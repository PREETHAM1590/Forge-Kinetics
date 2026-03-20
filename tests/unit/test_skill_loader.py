from __future__ import annotations

from forge.skills.loader import SkillLoader


def test_skill_loader_reads_metadata() -> None:
	loader = SkillLoader()
	skills = loader.load_all_metadata()
	assert len(skills) >= 10

	ids = {skill.id for skill in skills}
	assert "dashboard-layout" in ids
	assert "supabase-auth" in ids

	first = skills[0]
	assert first.name
	assert isinstance(first.tags, list)
