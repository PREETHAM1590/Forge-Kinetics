from __future__ import annotations

import asyncio

from forge.memory.knowledge_graph import TemporalKnowledgeGraph


def test_temporal_knowledge_graph_store_and_retrieve() -> None:
	async def _run() -> None:
		graph = TemporalKnowledgeGraph()
		await graph.store_decision("p1", {"decision": "Use Next.js"})
		await graph.store_brand_memory("p1", {"tone": "professional"})

		context = await graph.get_client_context("p1")
		assert context["project_id"] == "p1"
		assert context["decisions"][0]["decision"] == "Use Next.js"
		assert context["brand_memory"]["tone"] == "professional"

	asyncio.run(_run())
