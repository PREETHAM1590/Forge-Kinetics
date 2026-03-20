from __future__ import annotations

from dataclasses import dataclass

from forge.core.state import APIRoute, DataModel, ForgeState, TechSpecSchema


@dataclass(slots=True)
class ArchitectAgent:
    """Converts PRD into a minimal initial TechSpec."""

    def run(self, state: ForgeState) -> ForgeState:
        if state.prd is None:
            raise ValueError("ArchitectAgent requires state.prd")

        has_auth = any(feature.name.lower() == "authentication" for feature in state.prd.core_features)
        has_payments = any(feature.name.lower() == "payments" for feature in state.prd.core_features)

        api_routes = [
            APIRoute(
                method="GET",
                path="/api/tasks",
                description="List user tasks",
                auth_required=True,
                request_body=None,
                response_schema={"type": "array", "items": {"type": "object"}},
            ),
            APIRoute(
                method="POST",
                path="/api/tasks",
                description="Create user task",
                auth_required=True,
                request_body={"title": "string"},
                response_schema={"type": "object"},
            ),
        ]

        data_models = [
            DataModel(
                name="tasks",
                fields={"id": "uuid", "title": "text", "is_done": "boolean", "user_id": "uuid"},
                relationships=["tasks.user_id -> auth.users.id"],
                supabase_rls_policy="auth.uid() = user_id",
            )
        ]

        env_vars_needed = ["NEXT_PUBLIC_SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_ANON_KEY"]
        third_party_integrations = ["supabase"]
        agent_task_breakdown = {
            "frontend": ["Create task UI", "Connect dashboard views"],
            "backend": ["Create tasks API", "Add validation and auth guard"],
        }
        skill_assignments = {
            "Create task UI": "dashboard-layout.skill.md",
            "Create tasks API": "rest-crud.skill.md",
        }

        if has_auth:
            api_routes.append(
                APIRoute(
                    method="GET",
                    path="/api/me",
                    description="Resolve current authenticated user",
                    auth_required=True,
                    request_body=None,
                    response_schema={"type": "object"},
                )
            )
            agent_task_breakdown["backend"].append("Integrate auth flow")
            skill_assignments["Integrate auth flow"] = "supabase-auth.skill.md"

        if has_payments:
            api_routes.append(
                APIRoute(
                    method="POST",
                    path="/api/stripe/create-checkout",
                    description="Create checkout session",
                    auth_required=True,
                    request_body={"price_id": "string"},
                    response_schema={"checkout_url": "string"},
                )
            )
            data_models.append(
                DataModel(
                    name="subscriptions",
                    fields={"id": "uuid", "user_id": "uuid", "status": "text", "stripe_subscription_id": "text"},
                    relationships=["subscriptions.user_id -> auth.users.id"],
                    supabase_rls_policy="auth.uid() = user_id",
                )
            )
            env_vars_needed.extend([
                "STRIPE_SECRET_KEY",
                "STRIPE_WEBHOOK_SECRET",
                "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY",
            ])
            third_party_integrations.append("stripe")
            agent_task_breakdown["backend"].append("Implement Stripe checkout and webhook")
            skill_assignments["Implement Stripe checkout and webhook"] = "stripe-subscriptions.skill.md"

        state.tech_spec = TechSpecSchema(
            data_models=data_models,
            api_routes=api_routes,
            component_tree={
                "app": ["dashboard", "tasks-list", "settings"],
                "marketing": ["landing-page"],
            },
            env_vars_needed=sorted(set(env_vars_needed)),
            third_party_integrations=sorted(set(third_party_integrations)),
            estimated_files=14 + len(api_routes),
            supabase_schema_sql=self._build_schema_sql(data_models),
            agent_task_breakdown=agent_task_breakdown,
            skill_assignments=skill_assignments,
        )
        state.current_agent = "architect_agent"
        return state

    @staticmethod
    def _build_schema_sql(data_models: list[DataModel]) -> str:
        lines: list[str] = ["-- generated scaffold SQL"]
        for model in data_models:
            lines.append(f"create table if not exists {model.name} (")
            field_defs = []
            for field_name, field_type in model.fields.items():
                sql_type = "text"
                if field_type == "uuid":
                    sql_type = "uuid"
                elif field_type == "boolean":
                    sql_type = "boolean"
                field_defs.append(f"  {field_name} {sql_type}")
            lines.append(",\n".join(field_defs))
            lines.append(");")
            lines.append(f"alter table {model.name} enable row level security;")
        return "\n".join(lines)
