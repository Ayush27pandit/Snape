from typing import List, Dict, Any, Optional
from uuid import UUID
from dataclasses import dataclass

from sqlalchemy import select, func, and_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import BrandMemory, MemoryType
from src.memory.brand_memory import BrandMemoryStore, MemoryQuery, MemoryResult
from src.memory.embedder import get_embedder


@dataclass
class RetrievalResult:
    memory: MemoryResult
    retrieval_method: str  # "vector", "keyword", "hybrid"
    score: float


class HybridRetriever:
    """Combines vector similarity + keyword search for brand memories."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.store = BrandMemoryStore(db)
        self.embedder = get_embedder()

    async def retrieve(
        self,
        query: str,
        brand_id: UUID,
        limit: int = 10,
        types: Optional[List[MemoryType]] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.5,
        since_days: Optional[int] = None,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> List[RetrievalResult]:
        """Hybrid retrieval: vector similarity + keyword matching."""

        # Get query embedding
        query_embedding = await self.embedder.embed_query(query)

        # Vector search
        vector_results = await self.store.search(
            query_embedding=query_embedding,
            brand_id=brand_id,
            limit=limit * 2,  # Get more for merging
            types=types,
            tags=tags,
            min_confidence=min_confidence,
            since_days=since_days,
        )

        # Keyword search (PostgreSQL full-text)
        keyword_results = await self._keyword_search(
            query=query,
            brand_id=brand_id,
            limit=limit * 2,
            types=types,
            tags=tags,
            min_confidence=min_confidence,
            since_days=since_days,
        )

        # Merge and re-rank
        merged = self._merge_results(
            vector_results,
            keyword_results,
            vector_weight,
            keyword_weight,
        )

        # Convert to RetrievalResult
        results = [
            RetrievalResult(
                memory=mem,
                retrieval_method="hybrid",
                score=mem.similarity,
            )
            for mem in merged[:limit]
        ]

        return results

    async def _keyword_search(
        self,
        query: str,
        brand_id: UUID,
        limit: int,
        types: Optional[List[MemoryType]] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.5,
        since_days: Optional[int] = None,
    ) -> List[MemoryResult]:
        """PostgreSQL full-text search using tsvector."""
        from sqlalchemy import func as sql_func

        conditions = [
            BrandMemory.brand_id == brand_id,
            BrandMemory.confidence >= min_confidence,
        ]

        if types:
            conditions.append(BrandMemory.type.in_(types))

        if tags:
            conditions.append(BrandMemory.tags.op("&&")(tags))

        if since_days:
            from datetime import datetime, timedelta
            cutoff = datetime.utcnow() - timedelta(days=since_days)
            conditions.append(BrandMemory.extracted_at >= cutoff)

        conditions.append(
            or_(
                BrandMemory.expires_at.is_(None),
                BrandMemory.expires_at > datetime.utcnow(),
            )
        )

        # Use PostgreSQL full-text search
        stmt = (
            select(
                BrandMemory,
                sql_func.ts_rank_cd(
                    sql_func.to_tsvector("english", BrandMemory.content),
                    sql_func.plainto_tsquery("english", query),
                ).label("rank"),
            )
            .where(and_(*conditions))
            .order_by(text("rank DESC"))
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        return [
            MemoryResult(
                id=row.BrandMemory.id,
                type=row.BrandMemory.type,
                content=row.BrandMemory.content,
                confidence=row.BrandMemory.confidence,
                source_url=row.BrandMemory.source_url,
                source_title=row.BrandMemory.source_title,
                tags=row.BrandMemory.tags,
                extracted_at=row.BrandMemory.extracted_at,
                similarity=float(row.rank),
            )
            for row in rows
        ]

    def _merge_results(
        self,
        vector_results: List[MemoryResult],
        keyword_results: List[MemoryResult],
        vector_weight: float,
        keyword_weight: float,
    ) -> List[MemoryResult]:
        """Merge and re-rank vector + keyword results using RRF (Reciprocal Rank Fusion)."""
        # Use RRF for robust fusion
        k = 60  # RRF constant
        scores: Dict[str, float] = {}
        all_results: Dict[str, MemoryResult] = {}

        # Score vector results
        for rank, result in enumerate(vector_results, 1):
            key = str(result.id)
            scores[key] = scores.get(key, 0) + vector_weight / (k + rank)
            all_results[key] = result

        # Score keyword results
        for rank, result in enumerate(keyword_results, 1):
            key = str(result.id)
            scores[key] = scores.get(key, 0) + keyword_weight / (k + rank)
            if key not in all_results:
                all_results[key] = result

        # Sort by combined score
        sorted_keys = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)

        return [all_results[key] for key in sorted_keys]

    async def retrieve_for_agent(
        self,
        query: str,
        brand_id: UUID,
        agent_type: str,  # "planner", "analyzer", "synthesizer"
        limit: int = 10,
    ) -> List[RetrievalResult]:
        """Agent-specific retrieval with tuned parameters."""
        # Different agents need different memory types
        type_filters = {
            "planner": [MemoryType.FACT, MemoryType.INSIGHT, MemoryType.METRIC],
            "analyzer": [MemoryType.FACT, MemoryType.METRIC, MemoryType.NEWS, MemoryType.REVIEW],
            "synthesizer": [MemoryType.INSIGHT, MemoryType.OPINION, MemoryType.METRIC],
        }

        types = type_filters.get(agent_type)

        # Recency matters more for news/analysis
        since_days = 90 if agent_type == "analyzer" else None

        return await self.retrieve(
            query=query,
            brand_id=brand_id,
            limit=limit,
            types=types,
            since_days=since_days,
        )