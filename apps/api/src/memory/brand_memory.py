from typing import List, Optional, Dict, Any
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

from sqlalchemy import select, func, and_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from pgvector.sqlalchemy import Vector

from src.db.models import BrandMemory, Brand, MemoryType
from src.core.config import settings


@dataclass
class MemoryQuery:
    query: str
    brand_id: UUID
    types: Optional[List[MemoryType]] = None
    tags: Optional[List[str]] = None
    limit: int = 10
    min_confidence: float = 0.5
    since_days: Optional[int] = None


@dataclass
class MemoryResult:
    id: UUID
    type: MemoryType
    content: str
    confidence: float
    source_url: Optional[str]
    source_title: Optional[str]
    tags: List[str]
    extracted_at: datetime
    similarity: float


class BrandMemoryStore:
    """Persistent brand knowledge base with vector search."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_memory(
        self,
        brand_id: UUID,
        type: MemoryType,
        content: str,
        embedding: List[float],
        confidence: float = 1.0,
        source_url: Optional[str] = None,
        source_title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        ttl_days: Optional[int] = None,
    ) -> BrandMemory:
        """Add a new memory entry for a brand."""
        expires_at = None
        if ttl_days:
            expires_at = datetime.utcnow() + timedelta(days=ttl_days)

        memory = BrandMemory(
            brand_id=brand_id,
            type=type,
            content=content,
            embedding=embedding,
            confidence=confidence,
            source_url=source_url,
            source_title=source_title,
            tags=tags or [],
            expires_at=expires_at,
        )
        self.db.add(memory)
        await self.db.flush()
        return memory

    async def add_memories_batch(
        self,
        brand_id: UUID,
        memories: List[Dict[str, Any]],
    ) -> List[BrandMemory]:
        """Batch add memories for efficiency."""
        results = []
        for mem in memories:
            memory = await self.add_memory(
                brand_id=brand_id,
                type=mem["type"],
                content=mem["content"],
                embedding=mem["embedding"],
                confidence=mem.get("confidence", 1.0),
                source_url=mem.get("source_url"),
                source_title=mem.get("source_title"),
                tags=mem.get("tags"),
                ttl_days=mem.get("ttl_days"),
            )
            results.append(memory)
        return results

    async def search(
        self,
        query_embedding: List[float],
        brand_id: UUID,
        limit: int = 10,
        types: Optional[List[MemoryType]] = None,
        tags: Optional[List[str]] = None,
        min_confidence: float = 0.5,
        since_days: Optional[int] = None,
    ) -> List[MemoryResult]:
        """Semantic search over brand memories using pgvector."""
        conditions = [
            BrandMemory.brand_id == brand_id,
            BrandMemory.confidence >= min_confidence,
        ]

        if types:
            conditions.append(BrandMemory.type.in_(types))

        if tags:
            conditions.append(BrandMemory.tags.op("&&")(tags))

        if since_days:
            cutoff = datetime.utcnow() - timedelta(days=since_days)
            conditions.append(BrandMemory.extracted_at >= cutoff)

        # Exclude expired memories
        conditions.append(
            or_(
                BrandMemory.expires_at.is_(None),
                BrandMemory.expires_at > datetime.utcnow(),
            )
        )

        # Vector similarity search using cosine distance
        stmt = (
            select(
                BrandMemory,
                (1 - BrandMemory.embedding.cosine_distance(query_embedding)).label("similarity"),
            )
            .where(and_(*conditions))
            .order_by(text("similarity DESC"))
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
                similarity=float(row.similarity),
            )
            for row in rows
        ]

    async def get_recent_memories(
        self,
        brand_id: UUID,
        limit: int = 20,
        types: Optional[List[MemoryType]] = None,
    ) -> List[BrandMemory]:
        """Get most recent memories for a brand (non-vector)."""
        conditions = [BrandMemory.brand_id == brand_id]
        if types:
            conditions.append(BrandMemory.type.in_(types))

        stmt = (
            select(BrandMemory)
            .where(and_(*conditions))
            .order_by(BrandMemory.extracted_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_memories_by_type(
        self,
        brand_id: UUID,
        type: MemoryType,
        limit: int = 50,
    ) -> List[BrandMemory]:
        """Get all memories of a specific type."""
        stmt = (
            select(BrandMemory)
            .where(
                and_(
                    BrandMemory.brand_id == brand_id,
                    BrandMemory.type == type,
                    or_(
                        BrandMemory.expires_at.is_(None),
                        BrandMemory.expires_at > datetime.utcnow(),
                    ),
                )
            )
            .order_by(BrandMemory.extracted_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def delete_expired(self) -> int:
        """Clean up expired memories. Returns count deleted."""
        stmt = (
            select(BrandMemory)
            .where(
                and_(
                    BrandMemory.expires_at.is_not(None),
                    BrandMemory.expires_at < datetime.utcnow(),
                )
            )
        )
        result = await self.db.execute(stmt)
        expired = result.scalars().all()
        count = len(expired)
        for mem in expired:
            await self.db.delete(mem)
        return count

    async def get_stats(self, brand_id: UUID) -> Dict[str, Any]:
        """Get memory statistics for a brand."""
        stmt = select(
            BrandMemory.type,
            func.count(BrandMemory.id).label("count"),
            func.avg(BrandMemory.confidence).label("avg_confidence"),
        ).where(BrandMemory.brand_id == brand_id).group_by(BrandMemory.type)

        result = await self.db.execute(stmt)
        rows = result.all()

        stats = {row.type.value: {"count": row.count, "avg_confidence": float(row.avg_confidence or 0)} for row in rows}
        total = sum(s["count"] for s in stats.values())
        stats["total"] = total
        return stats


class BrandProfileManager:
    """Manages brand profile embeddings and metadata."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_profile_embedding(self, brand_id: UUID, embedding: List[float]) -> Brand:
        """Update the brand's profile embedding."""
        stmt = select(Brand).where(Brand.id == brand_id)
        result = await self.db.execute(stmt)
        brand = result.scalar_one_or_none()
        if brand:
            brand.profile_embedding = embedding
            await self.db.flush()
        return brand

    async def get_similar_brands(
        self,
        brand_id: UUID,
        limit: int = 10,
        min_similarity: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """Find brands with similar profile embeddings."""
        stmt = select(Brand).where(Brand.id == brand_id)
        result = await self.db.execute(stmt)
        brand = result.scalar_one_or_none()
        if not brand or brand.profile_embedding is None:
            return []

        stmt = (
            select(
                Brand,
                (1 - Brand.profile_embedding.cosine_distance(brand.profile_embedding)).label("similarity"),
            )
            .where(
                and_(
                    Brand.id != brand_id,
                    Brand.profile_embedding.is_not(None),
                )
            )
            .order_by(text("similarity DESC"))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        rows = result.all()

        return [
            {
                "id": row.Brand.id,
                "name": row.Brand.name,
                "domain": row.Brand.domain,
                "industry": row.Brand.industry,
                "similarity": float(row.similarity),
            }
            for row in rows
            if float(row.similarity) >= min_similarity
        ]