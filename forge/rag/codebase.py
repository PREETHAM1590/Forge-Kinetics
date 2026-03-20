from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class CodebaseRAG:
    """Simple text-search scaffold for per-project code retrieval."""

    project_id: str
    index_data: dict[str, str] = field(default_factory=dict)

    async def index_codebase(self, project_path: str) -> None:
        root = Path(project_path)
        if not root.exists():
            return

        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in {".py", ".md", ".ts", ".tsx", ".json", ".toml"}:
                continue
            try:
                self.index_data[str(file_path)] = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

    async def search(self, query: str, top_k: int = 5) -> list[str]:
        q = query.lower().strip()
        if not q:
            return []

        ranked: list[tuple[int, str]] = []
        for path, content in self.index_data.items():
            score = content.lower().count(q)
            if score > 0:
                ranked.append((score, path))

        ranked.sort(reverse=True, key=lambda item: item[0])
        return [path for _, path in ranked[:top_k]]
