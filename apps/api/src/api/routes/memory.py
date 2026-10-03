from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.db.models import BrandMemory, MemoryType
from src.memory.brand_memory import BrandMemoryStore, MemoryQuery
from src.memory.retriever import HybridRetriever
from src.memory.embedder import get_embedder

router = APIRouter(prefix="/memory", tags=["memory"])


class MemorySearchRequest(BaseModel):
    query: str
    brand_id: UUID
    types: Optional[List[MemoryType]] = None
    tags: Optional[List[str]] = None
    limit: int = 10
    min_confidence: float = 0.5
    since_days: Optional[int] = None


class MemorySearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int


class MemoryStatsResponse(BaseModel):
    total: int
    by_type: Dict[str, Dict[str, Any]]


@router.post("/search", response_model=MemorySearchResponse)
async def search_memory(
    request: MemorySearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """Semantic search over brand memories."""
    embedder = get_embedder()
    query_embedding = await embedder.embed_query(request.query)

    store = BrandMemoryStore(db)
    results = await store.search(
        query_embedding=query_embedding,
        brand_id=request.brand_id,
        limit=request.limit,
        types=request.types,
        tags=request.tags,
        min_confidence=request.min_confidence,
        since_days=request.since_days,
    )

    return MemorySearchResponse(
        results=[
            {
                "id": str(r.id),
                "type": r.type.value,
                "content": r.content,
                "confidence": r.confidence,
                "source_url": r.source_url,
                "source_title": r.source_title,
                "tags": r.tags,
                "extracted_at": r.extracted_at.isoformat(),
                "similarity": r.similarity,
            }
            for r in results
        ],
        total=len(results),
    )


@router.get("/brand/{brand_id}/stats", response_model=MemoryStatsResponse)
async def get_memory_stats(brand_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get memory statistics for a brand."""
    store = BrandMemoryStore(db)
    stats = await store.get_stats(brand_id)
    return MemoryStatsResponse(
        total=stats.pop("total", 0),
        by_type=stats,
    )


@router.get("/brand/{brand_id}/recent", response_model=List[Dict[str, Any]])
async def get_recent_memories(
    brand_id: UUID,
    limit: int = 20,
    type: Optional[MemoryType] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get most recent memories for a brand."""
    store = BrandMemoryStore(db)
    types = [type] if type else None
    memories = await store.get_recent_memories(brand_id, limit=limit, types=types)

    return [
        {
            "id": str(m.id),
            "type": m.type.value,
            "content": m.content[:500] + "..." if len(m.content) > 500 else m.content,
            "confidence": m.confidence,
            "source_url": m.source_url,
            "source_title": m.source_title,
            "tags": m.tags,
            "extracted_at": m.extracted_at.isoformat(),
        }
        for m in memories
    ]


@router.get("/brand/{brand_id}/by-type/{type}", response_model=List[Dict[str, Any]])
async def get_memories_by_type(
    brand_id: UUID,
    type: MemoryType,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Get all memories of a specific type."""
    store = BrandMemoryStore(db)
    memories = await store.get_memories_by_type(brand_id, type, limit=limit)

    return [
        {
            "id": str(m.id),
            "content": m.content,
            "confidence": m.confidence,
            "source_url": m.source_url,
            "source_title": m.source_title,
            "tags": m.tags,
            "extracted_at": m.extracted_at.isoformat(),
        }
        for m in memories
    ]


@router.post("/brand/{brand_id}/refresh")
async def refresh_brand_memory(brand_id: UUID, db: AsyncSession = Depends(get_db)):
    """Trigger re-crawl and re-embedding of brand data."""
    # This would trigger a new analysis job to refresh memory
    # For now, return success
    return {"status": "refresh_triggered", "brand_id": str(brand_id)}