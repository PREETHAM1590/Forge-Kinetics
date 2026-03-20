#!/bin/bash
# ============================================================
# FORGE — One-command setup script
# Run: chmod +x scripts/setup.sh && ./scripts/setup.sh
# ============================================================

set -e  # Exit on any error

echo ""
echo "⬡ FORGE — Setup Script"
echo "======================"
echo ""

# ── Check prerequisites ───────────────────────────────────
echo "Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3.11+ required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node 20+ required"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker required"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git required"; exit 1; }
echo "✓ Prerequisites OK"
echo ""

# ── Copy env file ─────────────────────────────────────────
if [ ! -f .env.local ]; then
  cp .env.example .env.local
  echo "✓ Created .env.local — fill in your API keys before running"
  echo ""
fi

# ── Start local services ──────────────────────────────────
echo "Starting local services (Redis, Neo4j, PostgreSQL, ChromaDB)..."
docker-compose up -d postgres redis neo4j chromadb
echo "Waiting for services to be ready..."
sleep 10
echo "✓ Services started"
echo ""

# ── Python setup ──────────────────────────────────────────
echo "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install poetry
poetry install
echo "✓ Python dependencies installed"
echo ""

# ── Platform (Next.js) setup ──────────────────────────────
echo "Setting up Next.js platform..."
cd platform
npm install
cd ..
echo "✓ Next.js dependencies installed"
echo ""

# ── Initialize database ───────────────────────────────────
echo "Running database migrations..."
# supabase db push (if using Supabase)
# or: python scripts/migrate.py
echo "✓ Database ready"
echo ""

# ── Index skills into ChromaDB ────────────────────────────
echo "Indexing Forge Skills library..."
source .venv/bin/activate
python scripts/seed_skills.py
echo "✓ Skills indexed"
echo ""

# ── Run Stage 1 smoke test ────────────────────────────────
echo "Running Stage 1 smoke test..."
source .venv/bin/activate
python tests/integration/test_stage1.py
echo "✓ Smoke test passed"
echo ""

echo "================================================"
echo "✅ FORGE SETUP COMPLETE"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Fill in .env.local with your API keys"
echo "  2. Start API:      source .venv/bin/activate && uvicorn forge.api.main:app --reload"
echo "  3. Start platform: cd platform && npm run dev"
echo "  4. Open:           http://localhost:3000"
echo ""
echo "Build stages: see stages/ directory"
echo "Current task: see forge-memory/NOW.md"
echo ""