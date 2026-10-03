# Snape - Competitive Intelligence Platform

AI-powered competitive intelligence for founders, marketers, and creators. Enter a brand name, get comprehensive analysis with competitor comparisons, sentiment tracking, and actionable insights.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   Next.js FE    │────▶│  FastAPI (Python)│────▶│  Redis + BullMQ     │
│   (Vercel)      │◀─── │  API Gateway     │     │  Job Queue          │
└─────────────────┘     └────────┬─────────┘     └──────────┬──────────┘
                                 │                          │
                    ┌────────────┼────────────┐             │
                    ▼            ▼            ▼             ▼
            ┌─────────────┐ ┌─────────┐ ┌──────────┐ ┌────────────┐
            │ Search Svc  │ │Scrape   │ │ Agent    │ │ Vector DB  │
            │ (Tavily/    │ │ Pool    │ │ Workers  │ │ (pgvector) │
            │  Context)   │ │(Playwri)│ │(LangGraph)           │
            └─────────────┘ └─────────┘ └──────────┘ └────────────┘
                                 │                          │
                                 ▼                          ▼
                        ┌─────────────────┐       ┌──────────────────┐
                        │  PostgreSQL     │       │  Brand Memory    │
                        │  (Prisma)       │◀─────▶│  (Context Store) │
                        └─────────────────┘       └──────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14 + TypeScript + Tailwind CSS |
| **API** | FastAPI (Python 3.11+) + Pydantic v2 |
| **Agents** | LangGraph + LangChain |
| **Queue** | BullMQ (Redis) |
| **Database** | PostgreSQL + pgvector |
| **Search** | Tavily API + Context.dev (free tiers) |
| **Scraping** | Playwright |
| **Auth** | Clerk |
| **Email** | Resend |
| **Deploy** | Vercel (FE) + Railway/Render (API) |

## Project Structure

```
snape/
├── apps/
│   ├── api/                 # FastAPI backend
│   │   └── src/
│   │       ├── api/         # Routes (analyze, brands, memory, comparisons)
│   │       ├── agents/      # LangGraph agents (planner, search, extract, analyze, synthesize)
│   │       ├── memory/      # BrandMemory, JobContext, Embedder, Retriever
│   │       ├── services/    # Search, Scrape, LLM services
│   │       ├── workers/     # BullMQ workers
│   │       ├── db/          # SQLAlchemy models, session
│   │       └── core/        # Config, settings
│   └── web/                 # Next.js frontend
│       └── src/
│           ├── app/         # App Router pages
│           ├── components/  # React components
│           ├── lib/         # Utilities
│           ├── hooks/       # Custom hooks
│           ├── store/       # Zustand stores
│           └── types/       # TypeScript types
├── packages/
│   ├── shared-types/        # Generated from OpenAPI
│   └── prompts/             # Shared prompt templates
└── turbo.json               # Turborepo config
```

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 15+ with pgvector extension
- Redis 7+
- API keys: Tavily, Context.dev, OpenAI, Clerk

### Installation

```bash
# Install dependencies
npm install

# Setup API
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Copy env files
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env.local

# Run database migrations
cd apps/api
alembic upgrade head

# Start development servers
npm run dev
```

### Environment Variables

See `.env.example` files in each app for required variables.

#### API Keys (Free Tiers)
- **Tavily**: 1,000 credits/month free
- **Context.dev**: 1,000 credits/month free
- **OpenAI**: Pay-per-use
- **Clerk**: Free tier available

## Development

### Running Locally

```bash
# Start all services
npm run dev

# Or individually:
# Terminal 1: Frontend
cd apps/web && npm run dev

# Terminal 2: API
cd apps/api && uvicorn src.main:app --reload

# Terminal 3: Worker
cd apps/api && python -m src.workers.analysis_worker
```

### Database

```bash
# Generate Prisma client
npm run db:generate

# Push schema changes
npm run db:push

# Open Prisma Studio
npm run db:studio
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key Features

### Analysis Types
1. **Brand Deep Dive** - Single brand sentiment, news, reviews, public opinion
2. **Competitor Comparison** - Side-by-side vs 1-5 rivals
3. **Market Landscape** - Category view of top 10-20 players
4. **Campaign Tracking** - Specific event/launch impact measurement

### Data Sources
- Web search (articles, blogs)
- News & press outlets
- Social media (X, LinkedIn, Reddit)
- Review sites (Trustpilot, G2, App Store)
- E-commerce (Amazon, Shopify)

### Competitive Metrics
- Share of Voice
- Sentiment Score & Trends
- Pricing & Positioning
- Product Features
- Marketing Channels
- Audience Overlap
- Crisis Events

### AI Analysis Levels
1. **Descriptive** - What happened
2. **Diagnostic** - Why it happened
3. **Predictive** - What will happen
4. **Prescriptive** - What to do

## Multi-Agent Pipeline

```
Planner → Search → Extract → Analyze → Synthesize
   │         │         │         │          │
   ▼         ▼         ▼         ▼          ▼
Sub-tasks  Tavily   Playwright  LLM      Final Report
           Context   Scraping   Analysis  + Citations
```

Each agent:
- Reads/writes to shared `JobContext` in Redis
- Accesses `BrandMemory` (RAG) for brand knowledge
- Checkpoints progress for resilience
- Structured outputs via Pydantic/Instructor

## Context Memory System

Two-layer memory for 100x agent reuse:

1. **Persistent Brand Knowledge** (PostgreSQL + pgvector)
   - Brand profiles with embeddings
   - Facts, insights, opinions, metrics, news
   - Semantic search with hybrid vector + keyword

2. **Working Memory** (Redis)
   - JobContext per analysis run
   - Sub-tasks, search results, extracted docs
   - Analysis cache, synthesis draft
   - Token budget tracking

## Pricing (MVP)

| Tier | Price | Analyses/Mo | Brands | Features |
|------|-------|-------------|--------|----------|
| Free | $0 | 2 | 1 | Basic metrics |
| Pro | $25/mo | 20 | 5 | All metrics, email digests |

## License

MIT