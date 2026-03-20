"""
approve_hitl.py — CLI to approve a pending HITL gate from terminal.
Usage: python scripts/approve_hitl.py <project_id> <approver_id>
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


async def approve(project_id: str, approver_id: str):
    from forge.hitl.gate import HITLGate

    gate = HITLGate()
    token = gate.generate_approval_token(project_id, approver_id)

    print(f"\n⬡ FORGE — HITL Approval")
    print("=" * 50)
    print(f"Project: {project_id}")
    print(f"Approver: {approver_id}")
    print(f"Token: {token[:20]}...")
    print(f"\n✅ Approval token generated")
    print(f"\nTo use: set this token in the pipeline state and resume.")
    print(f"Full token: {token}")

    return token


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/approve_hitl.py <project_id> <approver_id>")
        sys.exit(1)

    project_id = sys.argv[1]
    approver_id = sys.argv[2]
    asyncio.run(approve(project_id, approver_id))
