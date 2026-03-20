from __future__ import annotations

from importlib import import_module

from forge.agents.architect import ArchitectAgent
from forge.agents.backend import BackendAgent
from forge.agents.critic import CriticAgent
from forge.agents.frontend import FrontendAgent
from forge.agents.pm_agent import PMAgent
from forge.agents.security import SecurityAgent
from forge.agents.testing import TestingAgent
from forge.agents.devops import DevOpsAgent
from forge.core.state import ForgeState
from forge.hitl.gate import HITLGate


def route_after_critic(state: ForgeState) -> str:
    if state.critic_verdict and state.critic_verdict.verdict == "APPROVE":
        return "hitl"
    return "rebuild"


def route_after_hitl(state: ForgeState) -> str:
    gate = HITLGate()
    approval = gate.require_approval(state)
    if approval.approved:
        return "deploy"
    return "end"


def build_stage(state: ForgeState) -> ForgeState:
    state = FrontendAgent().run(state)
    state = BackendAgent().run(state)
    return state


def quality_stage(state: ForgeState) -> ForgeState:
    state = SecurityAgent().run(state)
    state = TestingAgent().run(state)
    state = CriticAgent().run(state)
    return state


def hitl_stage(state: ForgeState) -> ForgeState:
    gate = HITLGate()
    return gate.pause_for_approval(state)


def deploy_stage(state: ForgeState) -> ForgeState:
    return DevOpsAgent().run(state)

def run_pipeline(state: ForgeState) -> ForgeState:
    """Simple synchronous scaffold pipeline for early development."""
    state = PMAgent().run(state)
    state = ArchitectAgent().run(state)
    state = build_stage(state)
    state = quality_stage(state)
    route = route_after_critic(state)
    if route == "rebuild":
        state.pipeline_status = "failed"
        return state

    state = hitl_stage(state)
    hitl_route = route_after_hitl(state)
    if hitl_route == "deploy":
        state = deploy_stage(state)
    return state


def build_langgraph() -> object:
    """
    Build a LangGraph StateGraph when dependency is installed.

    This keeps the scaffold import-safe even before langgraph is added.
    """
    try:
        langgraph_graph = import_module("langgraph.graph")
        state_graph_cls = getattr(langgraph_graph, "StateGraph")
    except ImportError as error:
        raise ImportError("langgraph is not installed. Install dependencies before using build_langgraph().") from error

    graph = state_graph_cls(ForgeState)

    graph.add_node("pm", PMAgent().run)
    graph.add_node("architect", ArchitectAgent().run)
    graph.add_node("build", build_stage)
    graph.add_node("quality", quality_stage)
    graph.add_node("hitl", hitl_stage)
    graph.add_node("deploy", deploy_stage)
    graph.add_node("rebuild", build_stage)

    graph.set_entry_point("pm")
    graph.add_edge("pm", "architect")
    graph.add_edge("architect", "build")
    graph.add_edge("build", "quality")
    graph.add_conditional_edges("quality", route_after_critic, {"hitl": "hitl", "rebuild": "rebuild"})
    graph.add_conditional_edges("hitl", route_after_hitl, {"deploy": "deploy", "end": "__end__"})
    graph.add_edge("deploy", "__end__")
    graph.add_edge("rebuild", "quality")

    return graph


def compile_graph() -> object:
    graph = build_langgraph()
    return graph.compile()
