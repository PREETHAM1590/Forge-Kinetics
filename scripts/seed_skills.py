"""
seed_skills.py — Index all Forge Skill files into ChromaDB.
Run once after setup, and again whenever skill files are added/updated.
Usage: python scripts/seed_skills.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from forge.skills.loader import SkillLoader
from forge.skills.registry import SkillRegistry


async def seed():
    print("\n⬡ FORGE — Seeding Skills Library")
    print("=" * 40)

    loader = SkillLoader()
    registry = SkillRegistry()

    # Load all skill metadata (L1)
    skills = loader.load_all_metadata()
    print(f"\nFound {len(skills)} skill files:")

    for skill in skills:
        print(f"  [{skill.category:12}] {skill.id:35} {skill.description[:50]}")

    # Register all skills
    await registry.register_all(skills)

    print(f"\n✅ {len(skills)} skills indexed into registry")
    print("\nSkills available:")
    for category in ["auth", "payments", "ui", "api", "deploy", "testing"]:
        cat_skills = [s for s in skills if s.category == category]
        if cat_skills:
            print(f"  {category}: {', '.join(s.id for s in cat_skills)}")

    print("\nDone. Architects can now map tasks → skills.")


if __name__ == "__main__":
    asyncio.run(seed())
