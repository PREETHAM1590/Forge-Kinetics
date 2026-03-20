from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from forge.core.state import Feature, ForgeState, PRDSchema


@dataclass(slots=True)
class PMAgent:
    """Converts raw user input into a validated PRD schema."""

    default_target_users: str = "Technical agencies and dev teams"

    def run(self, state: ForgeState) -> ForgeState:
        prompt = state.user_input.strip()
        if not prompt:
            raise ValueError("PMAgent requires non-empty user_input")

        project_name = self._infer_project_name(prompt)
        complexity = self._estimate_complexity(prompt)
        skill_hints = self._infer_skill_hints(prompt)
        core_features = self._infer_core_features(prompt)
        estimated_credits = self._estimate_credits(complexity, len(core_features))

        state.prd = PRDSchema(
            project_name=project_name,
            one_liner=prompt[:120],
            target_users=self.default_target_users,
            core_features=core_features,
            out_of_scope=["Non-Phase-1 stacks", "Autonomous production deployment"],
            success_metrics=["First end-to-end pipeline run completes"],
            tech_constraints=["Next.js + Supabase only", "HITL required for deploy"],
            acceptance_criteria=[
                "PRD is schema-valid",
                "Requirements are clear enough for Architect handoff",
            ],
            estimated_complexity=complexity,
            estimated_credits=estimated_credits,
            skill_hints=skill_hints,
        )
        state.current_agent = "pm_agent"
        return state

    @staticmethod
    def _infer_project_name(user_input: str) -> str:
        tokens = [token.strip(" ,.:;!?\n\t") for token in user_input.split() if token.strip()]
        if not tokens:
            return "Untitled Forge Project"
        return " ".join(tokens[:5]).title()

    @staticmethod
    def _estimate_complexity(user_input: str) -> str:
        lowered = user_input.lower()
        complexity_hits = sum(
            keyword in lowered
            for keyword in ["payment", "webhook", "dashboard", "admin", "multi", "analytics", "workflow"]
        )
        if complexity_hits >= 4:
            return "complex"
        if complexity_hits >= 2:
            return "medium"
        return "simple"

    @staticmethod
    def _estimate_credits(complexity: str, feature_count: int) -> int:
        base = {"simple": 80, "medium": 180, "complex": 320}[complexity]
        return base + ceil(feature_count * 15)

    @staticmethod
    def _infer_skill_hints(user_input: str) -> list[str]:
        lowered = user_input.lower()
        hints = {"dashboard-layout.skill.md", "rest-crud.skill.md"}

        if any(keyword in lowered for keyword in ["auth", "login", "signup", "sign in"]):
            hints.add("supabase-auth.skill.md")
        if any(keyword in lowered for keyword in ["pricing", "subscription", "billing", "plan"]):
            hints.add("stripe-subscriptions.skill.md")
        if any(keyword in lowered for keyword in ["checkout", "one-time", "purchase", "buy"]):
            hints.add("stripe-one-time.skill.md")
        if any(keyword in lowered for keyword in ["landing", "marketing", "home page"]):
            hints.add("landing-page.skill.md")
        if any(keyword in lowered for keyword in ["table", "list", "crud", "manage"]):
            hints.add("data-table-crud.skill.md")
        if "webhook" in lowered:
            hints.add("webhook-handler.skill.md")

        return sorted(hints)

    @staticmethod
    def _infer_core_features(user_input: str) -> list[Feature]:
        lowered = user_input.lower()
        features: list[Feature] = [
            Feature(
                name="Core application flow",
                description="Implement the primary user journey requested in input.",
                priority="must_have",
                acceptance_criteria=["Core happy path works end-to-end"],
            )
        ]

        if any(keyword in lowered for keyword in ["auth", "login", "signup", "user"]):
            features.append(
                Feature(
                    name="Authentication",
                    description="Add auth aligned to Forge stack constraints.",
                    priority="must_have",
                    acceptance_criteria=["Protected routes require login"],
                )
            )

        if any(keyword in lowered for keyword in ["payment", "subscription", "checkout", "billing"]):
            features.append(
                Feature(
                    name="Payments",
                    description="Implement payment workflows with webhook-driven consistency.",
                    priority="should_have",
                    acceptance_criteria=["Payment state is persisted and auditable"],
                )
            )

        if any(keyword in lowered for keyword in ["dashboard", "admin", "analytics"]):
            features.append(
                Feature(
                    name="Dashboard",
                    description="Provide an operator dashboard for key workflows and status.",
                    priority="should_have",
                    acceptance_criteria=["Dashboard reflects live app state"],
                )
            )

        return features
