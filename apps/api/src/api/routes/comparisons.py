from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.session import get_db
from src.db.models import Comparison, Brand, Analysis

router = APIRouter(prefix="/comparisons", tags=["comparisons"])


class ComparisonCreate(BaseModel):
    primary_brand_id: UUID
    competitor_brand_ids: List[UUID] = Field(..., min_items=1, max_items=5)
    analysis_ids: List[UUID] = Field(default_factory=list)


class ComparisonResponse(BaseModel):
    id: UUID
    primary_brand_id: UUID
    primary_brand_name: str
    competitor_brand_ids: List[UUID]
    competitor_brand_names: List[str]
    metrics: dict
    insights: dict
    created_at: str

    class Config:
        from_attributes = True


@router.post("", response_model=ComparisonResponse, status_code=status.HTTP_201_CREATED)
async def create_comparison(
    request: ComparisonCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new brand comparison."""
    # Verify brands exist
    stmt = select(Brand).where(Brand.id.in_([request.primary_brand_id] + request.competitor_brand_ids))
    result = await db.execute(stmt)
    brands = {b.id: b for b in result.scalars().all()}

    if request.primary_brand_id not in brands:
        raise HTTPException(status_code=404, detail="Primary brand not found")

    for cid in request.competitor_brand_ids:
        if cid not in brands:
            raise HTTPException(status_code=404, detail=f"Competitor brand {cid} not found")

    # If analysis_ids provided, aggregate metrics from them
    metrics = {}
    insights = {}

    if request.analysis_ids:
        stmt = select(Analysis).where(Analysis.id.in_(request.analysis_ids))
        result = await db.execute(stmt)
        analyses = result.scalars().all()

        for analysis in analyses:
            if analysis.result:
                # Extract comparison data from analysis results
                if "competitorComparison" in analysis.result:
                    for comp in analysis.result["competitorComparison"]:
                        brand_name = comp.get("brand")
                        if brand_name:
                            if brand_name not in metrics:
                                metrics[brand_name] = {}
                            metrics[brand_name].update(comp.get("metrics", {}))

                if "recommendations" in analysis.result:
                    insights["recommendations"] = analysis.result["recommendations"]

    comparison = Comparison(
        primary_brand_id=request.primary_brand_id,
        competitor_brand_ids=[str(c) for c in request.competitor_brand_ids],
        metrics=metrics,
        insights=insights,
        analysis_ids=[str(a) for a in request.analysis_ids],
    )
    db.add(comparison)
    await db.commit()
    await db.refresh(comparison)

    return ComparisonResponse(
        id=comparison.id,
        primary_brand_id=comparison.primary_brand_id,
        primary_brand_name=brands[request.primary_brand_id].name,
        competitor_brand_ids=[UUID(c) for c in comparison.competitor_brand_ids],
        competitor_brand_names=[brands[UUID(c)].name for c in comparison.competitor_brand_ids],
        metrics=comparison.metrics,
        insights=comparison.insights,
        created_at=comparison.created_at.isoformat(),
    )


@router.get("", response_model=List[ComparisonResponse])
async def list_comparisons(
    user_id: Optional[UUID] = None,
    primary_brand_id: Optional[UUID] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List comparisons."""
    stmt = select(Comparison).order_by(Comparison.created_at.desc()).limit(limit).offset(offset)

    if primary_brand_id:
        stmt = stmt.where(Comparison.primary_brand_id == primary_brand_id)

    result = await db.execute(stmt)
    comparisons = result.scalars().all()

    # Get brand names
    all_brand_ids = set()
    for c in comparisons:
        all_brand_ids.add(c.primary_brand_id)
        all_brand_ids.update(UUID(bid) for bid in c.competitor_brand_ids)

    stmt = select(Brand).where(Brand.id.in_(all_brand_ids))
    result = await db.execute(stmt)
    brands = {b.id: b.name for b in result.scalars().all()}

    return [
        ComparisonResponse(
            id=c.id,
            primary_brand_id=c.primary_brand_id,
            primary_brand_name=brands.get(c.primary_brand_id, "Unknown"),
            competitor_brand_ids=[UUID(bid) for bid in c.competitor_brand_ids],
            competitor_brand_names=[brands.get(UUID(bid), "Unknown") for bid in c.competitor_brand_ids],
            metrics=c.metrics,
            insights=c.insights,
            created_at=c.created_at.isoformat(),
        )
        for c in comparisons
    ]


@router.get("/{comparison_id}", response_model=ComparisonResponse)
async def get_comparison(comparison_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get comparison details."""
    stmt = select(Comparison).where(Comparison.id == comparison_id)
    result = await db.execute(stmt)
    comparison = result.scalar_one_or_none()

    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")

    # Get brand names
    all_brand_ids = {comparison.primary_brand_id}
    all_brand_ids.update(UUID(bid) for bid in comparison.competitor_brand_ids)

    stmt = select(Brand).where(Brand.id.in_(all_brand_ids))
    result = await db.execute(stmt)
    brands = {b.id: b.name for b in result.scalars().all()}

    return ComparisonResponse(
        id=comparison.id,
        primary_brand_id=comparison.primary_brand_id,
        primary_brand_name=brands.get(comparison.primary_brand_id, "Unknown"),
        competitor_brand_ids=[UUID(bid) for bid in comparison.competitor_brand_ids],
        competitor_brand_names=[brands.get(UUID(bid), "Unknown") for bid in comparison.competitor_brand_ids],
        metrics=comparison.metrics,
        insights=comparison.insights,
        created_at=comparison.created_at.isoformat(),
    )


@router.delete("/{comparison_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comparison(comparison_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a comparison."""
    stmt = select(Comparison).where(Comparison.id == comparison_id)
    result = await db.execute(stmt)
    comparison = result.scalar_one_or_none()

    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")

    await db.delete(comparison)
    await db.commit()