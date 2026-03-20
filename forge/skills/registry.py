from __future__ import annotations

from dataclasses import dataclass

from forge.core.state import SkillMetadata
from forge.skills.loader import SkillLoader


@dataclass(slots=True)
class SkillRegistry:
	loader: SkillLoader

	def __init__(self, loader: SkillLoader | None = None) -> None:
		self.loader = loader or SkillLoader()

	def all(self) -> list[SkillMetadata]:
		return self.loader.load_all_metadata()

	def by_id(self, skill_id: str) -> SkillMetadata | None:
		for skill in self.all():
			if skill.id == skill_id:
				return skill
		return None

