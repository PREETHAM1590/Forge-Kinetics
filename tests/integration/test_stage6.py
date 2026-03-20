from __future__ import annotations

import asyncio
import uuid

from forge.memory.knowledge_graph import TemporalKnowledgeGraph
from forge.memory.recall import RecallMemory
from forge.rag.codebase import CodebaseRAG


def test_stage6_knowledge_graph_and_recall() -> None:
    async def _run() -> None:
        project_id = str(uuid.uuid4())
        user_id = "memory-user"

        graph = TemporalKnowledgeGraph()
        await graph.store_decision(project_id, {"decision": "Use Next.js + Supabase"})
        await graph.store_brand_memory(project_id, {"tone": "playful"})

        context = await graph.get_client_context(project_id)
        assert context["decisions"][0]["decision"] == "Use Next.js + Supabase"
        assert context["brand_memory"]["tone"] == "playful"

        recall = RecallMemory()
        await recall.store_session("s1", "Implemented stage 6", user_id)
        recent = await recall.get_recent_context(user_id)
        assert "Implemented stage 6" in recent

    asyncio.run(_run())


def test_stage6_codebase_rag_search() -> None:
    async def _run() -> None:
        rag = CodebaseRAG(project_id="stage6")
        await rag.index_codebase("d:/FORGE/forge")

        results = await rag.search("ForgeState", top_k=5)
        assert isinstance(results, list)

    asyncio.run(_run())
