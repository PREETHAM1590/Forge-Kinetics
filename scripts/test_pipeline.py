"""
test_pipeline.py — Quick smoke test to verify pipeline is working.
Run: python scripts/test_pipeline.py "Build a todo app with auth"
"""

import asyncio
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from forge.core.state import ForgeState, TokenBudget


async def run_test(user_input: str):
    print("\n⬡ FORGE — Pipeline Smoke Test")
    print("=" * 50)
    print(f"Input: {user_input}")
    print("=" * 50)

    from forge.core.graph import app

    state = ForgeState(
        project_id=str(uuid.uuid4()),
        user_id="smoke-test-user",
        session_id=str(uuid.uuid4()),
        user_input=user_input,
        token_budget=TokenBudget(total_allocated=500_000),
    )

    print("\nStarting pipeline...\n")
    result = await app.ainvoke(state)

    print("\n" + "=" * 50)
    print("PIPELINE RESULT")
    print("=" * 50)

    if result.get("prd"):
        print(f"✓ PM Agent    → PRD: {result['prd']['project_name']}")
        print(f"              → Complexity: {result['prd']['estimated_complexity']}")
        print(f"              → Credits est: {result['prd']['estimated_credits']}")

    if result.get("tech_spec"):
        spec = result["tech_spec"]
        print(f"✓ Architect   → {len(spec.get('api_routes', []))} routes")
        print(f"              → Skills: {spec.get('skill_assignments', {})}")

    if result.get("frontend_code"):
        print(f"✓ Frontend    → {result['frontend_code']['status']}")

    if result.get("backend_code"):
        print(f"✓ Backend     → {result['backend_code']['status']}")

    if result.get("security_report"):
        print(f"✓ Security    → {result['security_report']['verdict']}")

    if result.get("test_results"):
        print(f"✓ Tests       → {result['test_results']['verdict']}")

    if result.get("critic_verdict"):
        print(f"✓ Critic      → {result['critic_verdict']['verdict']}")

    hitl = result.get("hitl_status", "unknown")
    print(f"\n⏸  HITL Status: {hitl.upper()}")

    if result.get("deploy_url"):
        print(f"🚀 Deploy URL: {result['deploy_url']}")

    # Cost report
    budget = result.get("token_budget", {})
    total = budget.get("total_used", 0) if isinstance(budget, dict) else 0
    print(f"\n💰 Tokens used: {total:,}")
    print(f"   Credits:     {max(1, total // 10_000)}")
    print(f"   Cost est:    ${total * 0.000005:.4f}")

    print("\n✅ Smoke test complete")


if __name__ == "__main__":
    input_text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "Build a SaaS project management tool with auth and Stripe billing"
    asyncio.run(run_test(input_text))
