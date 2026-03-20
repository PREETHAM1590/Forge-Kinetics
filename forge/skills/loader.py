from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from forge.core.state import SkillMetadata


class SkillLoader:
    """Loads skill metadata from `forge-features/skills/**/*.skill.md` (Level 1)."""

    def __init__(self, root_dir: Path | None = None) -> None:
        if root_dir is None:
            root_dir = Path(__file__).resolve().parents[2]
        self.root_dir = root_dir
        self.skills_dir = self.root_dir / "forge-features" / "skills"

    def load_all_metadata(self) -> list[SkillMetadata]:
        metadata: list[SkillMetadata] = []
        for skill_file in sorted(self.skills_dir.rglob("*.skill.md")):
            metadata.append(self._parse_metadata(skill_file))
        return metadata

    def _parse_metadata(self, skill_file: Path) -> SkillMetadata:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
        title = lines[0].lstrip("# ") if lines else skill_file.stem
        description = lines[2].strip() if len(lines) > 2 else ""

        tags: list[str] = []
        category = "general"
        stack_requirements: list[str] = []

        if "| Category:" in (lines[1] if len(lines) > 1 else ""):
            meta_line = lines[1]
            parts = [part.strip() for part in meta_line.split("|") if part.strip()]
            for part in parts:
                if part.lower().startswith("category:"):
                    category = part.split(":", 1)[1].strip().lower()
                if part.lower().startswith("stack:"):
                    stack_requirements = [item.strip().lower() for item in part.split(":", 1)[1].split("+")]

        tags.extend(stack_requirements)
        tags.append(category)

        return SkillMetadata(
            id=skill_file.stem.replace(".skill", ""),
            name=title,
            description=description,
            category=category,
            tags=sorted(set([tag for tag in tags if tag])),
            stack_requirements=stack_requirements,
            success_rate=0.0,
            last_updated=datetime.now(tz=timezone.utc),
        )
