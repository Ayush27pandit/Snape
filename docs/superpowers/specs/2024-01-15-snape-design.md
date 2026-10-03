# Snape - Competitive Intelligence Platform Design Specification

**Date**: 2024-01-15
**Version**: 1.0
**Status**: Approved for Implementation

---

## 1. Executive Summary

Snape is an AI-powered competitive intelligence platform for founders, CTOs, marketers, creators, and influencers. Users enter a brand name, and Snape's multi-agent system searches the entire web, collects data from 5+ source categories, analyzes competitive metrics, and presents actionable insights with citations.

**Core Value Proposition**: Transform weeks of manual competitive research into minutes of AI-driven analysis.

---

## 2. Product Scope (MVP)

### 2.1 Analysis Types (All at Launch)
| Type | Description |
|------|-------------|
| **Brand Deep Dive** | Single brand: sentiment, news, reviews, public opinion, key metrics |
| **Competitor Comparison** | 1 primary vs 3-5 rivals across all dimensions |
| **Market Landscape** | Category view: top 10-20 brands, positioning map, trends |
| **Campaign/Launch Tracking** | Specific event/campaign impact measurement |

### 2.2 Data Sources (5 Categories)
1. **Web Search** — General web, articles, blogs (Tavily/Context.dev)
2. **News & Press** — Major outlets, industry press, PR wires
3. **Social Media** — X/Twitter, LinkedIn, Reddit (public posts)
4. **Review Sites** — Trustpilot, G2, App Store, Google Reviews
5. **E-commerce** — Amazon, Shopify stores (pricing, listings, reviews)

### 2.3 Competitive Metrics (All 7)
- Share of Voice (mention volume)
- Sentiment Score & Trends
- Pricing & Positioning Analysis
- Product Feature Comparison
- Marketing Channel Performance
- Audience Overlap & Demographics
- Crisis/Reputation Events

### 2.4 AI Analysis Maturity (All 4 Levels)
1. **Descriptive** — What happened (cited synthesis)
2. **Diagnostic** — Why it happened (root cause correlation)
3. **Predictive** — What will happen (trend projection, scenarios)
4. **Prescriptive** — What to do (actionable strategies, prioritized)

### 2.5 Output & Delivery
- **Interactive Web Dashboard** — Charts, filters, drill-downs, real-time progress
- **Weekly/Monthly Email Digests** — Automated summaries with key changes
- *Deferred: PDF export, Slack/Discord alerts, API access*

### 2.6 Onboarding Flow
**Wizard + Auto-Discover Hybrid**
1. User enters brand name
2. AI auto-discovers: domain, social handles, industry, description
3. User confirms/edits, adds known competitors, focus keywords
4. System creates BrandProfile + initial memory embeddings

### 2.7 Pricing (MVP)
| Tier | Price | Analyses/Mo | Brands | Features |
|------|-------|-------------|--------|----------|
| **Free** | $0 | 2 | 1 | Basic metrics, dashboard only |
| **Pro** | $25/mo | 20 | 5 | All metrics, email digests, priority queue |

### 2.8 Collaboration
- **MVP: Single-user only** — No teams, workspaces, or sharing
- Post-MVP: Multi-user orgs, read-only client links, RBAC

---

## 3. Technical Architecture

### 3.1 System Overview

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
                        │  PostgreSQL     │◀─────▶│  Brand Memory    │
                        │  (SQLAlchemy)   │       │  (Context Store) │
                        └─────────────────┘       └──────────────────┘
```

### 3.2 Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Frontend** | Next.js 14 + TypeScript + Tailwind | Modern React, great SEO, Vercel deploy |
| **API** | FastAPI (Python 3.11+) + Pydantic v2 | Best ML/AI ecosystem, async, LangGraph native |
| **Agents** | LangGraph + LangChain | First-class multi-agent support, stateful |
| **Queue** | BullMQ (Redis) | Reliable, priority, delayed jobs, rate limiting |
| **Database** | PostgreSQL + pgvector | Single DB, ACID, vector search built-in |
| **Search** | Tavily (primary) + Context.dev (fallback) | Best agent search + brand intelligence |
| **Scraping** | Playwright pool | Handles JS-heavy sites, stealth |
| **Auth** | Clerk | User management, organizations, subscriptions |
| **Email** | Resend | Transactional email |
| **Observability** | LangSmith + Sentry + PostHog | Agent tracing, errors, analytics |

### 3.3 Repo Structure (Turborepo Monorepo)

```
snape/
├── apps/
│   ├── web/                 # Next.js frontend
│   └── api/                 # FastAPI backend
│       ├── src/
│       │   ├── api/         # Routes (analyze, brands, memory, comparisons)
│       │   ├── agents/      # LangGraph agents (planner, search, extract, analyze, synthesize)
│       │   ├── memory/      # BrandMemory, JobContext, Embedder, Retriever
│       │   ├── services/    # Search, Scrape, LLM services
│       │   ├── workers/     # BullMQ processors
│       │   ├── db/          # SQLAlchemy models, session
│       │   └── core/        # Config, settings
├── packages/
│   ├── shared-types/        # Generated from OpenAPI (TS)
│   └── prompts/             # Shared prompt templates (JSON/YAML)
├── turbo.json
└── package.json
```

---

## 4. Data Models

### 4.1 Core Entities (SQLAlchemy + pgvector)

```python
# User - Founder, CTO, Marketer, Creator, Influencer
User {
  id, email, name, role, plan, clerk_id
  brands[], analyses[], comparisons[]
}

# Brand - Tracked entity with memory
Brand {
  id, user_id, name, domain, industry, description
  competitors[], focus_keywords[]
  profile_embedding (vector(1536))
  analyses[], memories[]
}

# Analysis - Single job execution
Analysis {
  id, brand_id, user_id, type, status
  input_config {query, competitors[], date_range, focus_areas, depth}
  result (JSON report), job_id, progress, stages
  started_at, completed_at
}

# BrandMemory - Persistent knowledge base (RAG)
BrandMemory {
  id, brand_id, type (FACT/INSIGHT/OPINION/METRIC/NEWS/REVIEW)
  content, embedding (vector(1536)), confidence
  source_url, source_title, tags[]
  extracted_at, expires_at (TTL)
}

# Comparison - Side-by-side results
Comparison {
  id, user_id, primary_brand_id, competitor_brand_ids[]
  metrics (side-by-side), insights (AI-generated)
  analysis_ids[], created_at
}
```

### 4.2 Key Indexes
- `brands(user_id, name)`, `brands(domain)`
- `analyses(user_id, status)`, `analyses(brand_id, created_at)`
- `brand_memories(brand_id, type)`, `brand_memories(expires_at)`
- `brand_memories(embedding)` — HNSW vector index

---

## 5. Multi-Agent Pipeline (LangGraph)

### 5.1 Agent Flow

```
User Query → Planner Agent → Search Agent → Extract Agent → Analyze Agent → Synthesize Agent → Response
                │               │              │               │                │
                ▼               ▼              ▼               ▼                ▼
           Sub-queries    Raw HTML/JSON   Structured     Insights +        Final Report
           + Strategy     + Metadata      Data Points    Scores            + Citations
```

### 5.2 Agent Responsibilities

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Planner** | Decomposes request into parallel sub-tasks | Brand, type, config | `SubTask[]` (search/extract/analyze) |
| **Search** | Calls Tavily/Context.dev for web, news, social, reviews | SubTask queries | `SearchResult[]` (ranked URLs + snippets) |
| **Extract** | Playwright scrapes top-N URLs → clean markdown | URLs from Search | `ExtractedDoc[]` (content + metadata) |
| **Analyze** | Sentiment, entity extraction, metric computation | ExtractedDocs + BrandMemory (RAG) | `AnalysisResult[]` (insights, metrics, citations) |
| **Synthesize** | Structures final report with citations, comparisons | All AnalysisResults | `FinalReport` (executive summary, tables, charts data) |

### 5.3 State Management

**AgentState (LangGraph)** — Shared across all agents:
```python
AgentState {
  job_id, analysis_id, brand_id, user_id, analysis_type, config
  sub_tasks: SubTask[]
  search_results: SearchResult[]
  extracted_docs: ExtractedDoc[]
  analysis_cache: Dict[task_id, AnalysisResult]
  synthesis_draft, final_report
  current_stage, stage_progress, overall_progress
  token_budget, tokens_used
  error, retry_count
}
```

**JobContext (Redis)** — Working memory per job:
- Checkpointed after each agent
- Enables resume on failure
- Real-time progress for frontend
- TTL: job_timeout + 1 hour

---

## 6. Context Memory System (100x Agent Reuse)

### 6.1 Two-Layer Architecture

#### Layer 1: Persistent Brand Knowledge Base (PostgreSQL + pgvector)
```
BrandProfile {
  id, name, domain, industry, description
  profile_embedding (vector(1536))
}

BrandMemory {
  brand_id, type (FACT/INSIGHT/OPINION/METRIC/NEWS/REVIEW)
  content, embedding, confidence
  source_url, source_title, tags[]
  extracted_at, expires_at
}
```

#### Layer 2: Agent Working Memory (Redis)
```
JobContext {
  job_id, analysis_id, brand_id, user_id
  sub_tasks, search_results, extracted_docs
  analysis_cache, synthesis_draft
  token_budget, progress tracking
}
```

### 6.2 "100x Reuse" Mechanisms

| Mechanism | Implementation |
|-----------|----------------|
| **Prompt Templates** | Versioned in `packages/prompts/`, loaded at runtime |
| **Brand RAG Injection** | `BrandMemory.retrieveRelevant(query, k=10)` → injected into every agent system prompt |
| **Tool Definitions** | Shared `tools/` registry (search, scrape, calculate, compare) |
| **State Schema** | Zod-validated state per agent, enables hot-swapping nodes |
| **Evaluation Harness** | `packages/evals/` — test agents against golden datasets |
| **Observability** | LangSmith tracing on every node execution |

### 6.3 Retrieval Strategy

**HybridRetriever** combines:
- **Vector similarity** (pgvector cosine distance) — weighted 0.7
- **Keyword search** (PostgreSQL tsvector/tsquery) — weighted 0.3
- **RRF (Reciprocal Rank Fusion)** for robust merging
- Agent-specific type filters (planner→facts/insights, analyzer→metrics/news, synthesizer→insights/opinions)

---

## 7. API Contracts

### 7.1 Start Analysis
```
POST /api/v1/analyze/start
{
  "brandId": "uuid",
  "type": "COMPETITOR_COMPARISON",
  "competitors": ["uuid1", "uuid2"],
  "dateRange": "LAST_30_DAYS",
  "focusAreas": ["sentiment", "pricing", "product", "marketing"],
  "depth": "deep"
}

Response: { "jobId": "uuid", "analysisId": "uuid", "status": "PENDING", "estimatedDurationSec": 120 }
```

### 7.2 Get Status (Real-time)
```
GET /api/v1/analyze/status/{jobId}
Response: {
  "jobId": "uuid",
  "status": "RUNNING",
  "progress": 45,
  "currentStage": "EXTRACT",
  "stageProgress": { "search": 100, "extract": 45, "analyze": 0, "synthesize": 0 }
}
```

### 7.3 Get Result
```
GET /api/v1/analyze/result/{jobId}
Response: {
  "analysisId": "uuid",
  "report": {
    "executiveSummary": "...",
    "brandOverview": { ... },
    "competitorComparison": [
      { "brand": "Nike", "metrics": {...}, "strengths": [...], "weaknesses": [...] }
    ],
    "sentimentAnalysis": { "overall": 0.72, "byChannel": {...}, "trends": [...] },
    "newsAndArticles": [{ "title": "...", "url": "...", "source": "...", "date": "...", "sentiment": 0.6 }],
    "publicOpinion": { "reddit": [...], "twitter": [...], "reviews": [...] },
    "recommendations": [...],
    "citations": [{ "claim": "...", "sourceUrl": "...", "relevance": 0.9 }]
  }
}
```

### 7.4 Brand Memory Search
```
POST /api/v1/memory/search
{ "query": "pricing strategy", "brandId": "uuid", "types": ["METRIC", "INSIGHT"], "limit": 10 }
```

---

## 8. Job Queue (BullMQ)

### 8.1 Job Schema
```typescript
interface AnalysisJobData {
  analysisId: string;
  brandId: string;
  userId: string;
  type: AnalysisType;
  config: {
    competitors: string[];
    dateRange: string;
    focusAreas: string[];
    maxSources: number;
    depth: 'quick' | 'deep' | 'comprehensive';
  };
  priority: number; // 1=high, 5=low
}
```

### 8.2 Worker Config
- **Concurrency**: 3-5 per agent type
- **Retries**: 2x with exponential backoff
- **Timeout**: 10 min per job (configurable by depth)
- **Priority**: Pro users get priority=1, Free=5

---

## 9. Frontend Pages (Next.js App Router)

| Route | Purpose |
|-------|---------|
| `/` | Landing, auth |
| `/dashboard` | User's brands, recent analyses, usage bar |
| `/dashboard/brands/[id]` | Brand profile, memory viewer |
| `/dashboard/analyze/new` | 4-step wizard: brand → type → config → review |
| `/dashboard/analyze/[jobId]` | Real-time progress + streaming result |
| `/dashboard/comparisons/[id]` | Side-by-side dashboard with charts |
| `/dashboard/settings` | Plan, API keys, brand management |

---

## 10. Search/Scrape Strategy (Free Tiers)

### 9.1 Primary: Tavily + Context.dev Hybrid

| Service | Role | Free Tier |
|---------|------|-----------|
| **Tavily** | Search + cited extraction (LangChain-native) | 1,000 credits/mo |
| **Context.dev** | Brand intelligence + deep scrape + monitors | 1,000 credits/mo |

### 9.2 Why This Combo?
- Tavily: Best agent search, structured output, cited answers
- Context.dev: **Only provider with native brand data** (logos, colors, firmographics, monitors)
- Together cover 95% of needs without vendor lock-in

### 9.3 Estimated Monthly Cost (Pro Tier)
| Service | Plan | Credits | Cost |
|---------|------|---------|------|
| Tavily | Startup | 38,000 | $220 |
| Context.dev | Pro | 200,000 | $149 |
| **Total** | | | **~$370/mo** |

At 20 analyses/user × 5 brands × 10 sources = ~1,000 credits/analysis → supports ~200 analyses/mo

---

## 11. Key User Journeys

### Journey 1: Founder Monthly Competitive Review
1. Login → Dashboard shows 3 tracked brands
2. Click "New Analysis" → Select "Competitor Comparison"
3. Primary brand pre-selected, pick 3 rivals from suggestions
4. Choose focus: "Pricing + Marketing + Sentiment"
5. Hit "Run" → Real-time progress (Search→Extract→Analyze→Synthesize)
6. 2-3 min later: Interactive comparison dashboard
7. Schedule monthly email digest for this comparison

### Journey 2: Marketing Lead Tracking Campaign Launch
1. Select "Campaign Tracking" analysis type
2. Enter campaign hashtag/keywords + date range
3. System monitors all sources for 2 weeks
4. Daily email: mention volume, sentiment, top voices
5. Final report: ROI estimate, competitor response, lessons

### Journey 3: Creator/Influencer Audience Analysis
1. Enter own handle + 5 peer creators
2. Select "Audience Overlap + Demographics"
3. Get: shared followers %, platform breakdown, content gaps
4. Prescriptive: "Post more Reels on Tuesdays, cover Topic X"

---

## 12. Implementation Phases

### Phase 1: Foundation (Week 1-2) ✅ COMPLETE
- [x] Monorepo setup (Turbo)
- [x] FastAPI + Next.js scaffolding
- [x] Database models (SQLAlchemy + pgvector)
- [x] BrandMemory system (store, retriever, embedder)
- [x] JobContext (Redis + BullMQ)
- [x] Search/Scrape services (Tavily + Context.dev)
- [x] LLM service (Instructor + OpenAI)
- [x] Multi-agent pipeline (LangGraph: planner, search, extract, analyze, synthesize)
- [x] API routes (analyze, brands, memory, comparisons)
- [x] Frontend pages (landing, dashboard, analyze wizard)

### Phase 2: Integration & Testing (Week 3)
- [ ] End-to-end pipeline execution
- [ ] Real-time progress via WebSocket/polling
- [ ] Email digest scheduler
- [ ] Clerk auth integration
- [ ] Rate limiting, error handling
- [ ] Load testing with free tier limits

### Phase 3: Polish & Launch (Week 4)
- [ ] UI/UX refinements
- [ ] Analytics (PostHog)
- [ ] Documentation
- [ ] Deploy to Vercel + Railway
- [ ] Beta user onboarding

---

## 13. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Free tier rate limits | High | Medium | Implement caching, request batching, fallback to Context.dev |
| Scraping blocking | Medium | High | Playwright stealth, rotate user agents, respect robots.txt |
| LLM token costs | Medium | Medium | Token budget per job, gpt-4o-mini for extract/analyze |
| Vector search performance | Low | Medium | HNSW index, limit to 1536 dims, pgvector is fast enough <1M vectors |
| Agent hallucination | Medium | High | Structured outputs (Instructor), citations required, confidence scoring |

---

## 14. Success Criteria (MVP)

- [ ] User can create brand → run analysis → see results in <3 min
- [ ] All 4 analysis types functional
- [ ] Competitor comparison shows side-by-side metrics
- [ ] Email digests deliver weekly
- [ ] Free tier limits enforced
- [ ] 99% job success rate (retries handled)
- [ ] <500ms API p95 for status checks
- [ ] Zero critical security issues

---

## 15. Appendix: File Inventory

### API (`apps/api/src/`)
```
core/config.py                 # Pydantic settings
db/models.py                   # SQLAlchemy models (User, Brand, Analysis, BrandMemory, Comparison)
db/session.py                  # Async engine, session, init_db
memory/brand_memory.py         # BrandMemoryStore, BrandProfileManager
memory/job_context.py          # JobContext, JobContextManager, PipelineStage
memory/embedder.py             # OpenAI embeddings wrapper
memory/retriever.py            # HybridRetriever (vector + keyword)
services/search_service.py     # Tavily + Context.dev search + brand intel
services/scrape_service.py     # Playwright pool + Context.dev extract
services/llm_service.py        # Instructor + OpenAI/Anthropic
agents/state.py                # AgentState, create_initial_state
agents/planner.py              # Planner agent (structured output)
agents/search.py               # Search agent node
agents/extract.py              # Extract agent node
agents/analyze.py              # Analyze agent node
agents/synthesize.py           # Synthesize agent node
agents/pipeline.py             # LangGraph compilation + checkpointer
workers/analysis_worker.py     # BullMQ worker + event handlers
api/routes/analyze.py          # Start, status, result, list
api/routes/brands.py           # CRUD, discover, similar
api/routes/memory.py           # Search, stats, recent, by-type
api/routes/comparisons.py      # CRUD, aggregation
main.py                        # FastAPI app + lifespan
```

### Web (`apps/web/src/`)
```
app/layout.tsx                 # Root layout + providers
app/page.tsx                   # Landing page
app/providers.tsx              # QueryClient + Clerk + Toaster
app/globals.css                # Tailwind + custom components
app/(dashboard)/layout.tsx     # Sidebar + header + auth
app/(dashboard)/dashboard/page.tsx  # Brands/analyses tabs + usage
app/(dashboard)/analyze/new/page.tsx # 4-step wizard
lib/utils.ts                   # cn(), formatDate, truncate
```

---

**Approval**: ✅ Design approved. Proceed to implementation Phase 2.