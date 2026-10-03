from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid

from src.db.session import get_db
from src.db.models import Brand, User, UserRole, Plan
from src.services.search_service import get_search_service
from src.memory.brand_memory import BrandProfileManager


router = APIRouter(prefix="/brands", tags=["brands"])


class BrandCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    domain: Optional[HttpUrl] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    competitors: List[str] = Field(default_factory=list)
    focus_keywords: List[str] = Field(default_factory=list)


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[HttpUrl] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    competitors: Optional[List[str]] = None
    focus_keywords: Optional[List[str]] = None


class BrandResponse(BaseModel):
    id: UUID
    name: str
    domain: Optional[str]
    industry: Optional[str]
    description: Optional[str]
    competitors: List[str]
    focus_keywords: List[str]
    auto_discovered: bool
    last_analyzed_at: Optional[str]
    created_at: str
    updated_at: str
    analyses_count: int = 0

    class Config:
        from_attributes = True


class BrandDiscoverRequest(BaseModel):
    name: str


class BrandDiscoverResponse(BaseModel):
    name: str
    domain: Optional[str]
    industry: Optional[str]
    description: Optional[str]
    logo_url: Optional[str]
    colors: List[str]
    social_handles: Dict[str, str]
    confidence: float


@router.post("", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(
    request: BrandCreate,
    db: AsyncSession = Depends(get_db),
    # TODO: Add user authentication
    # current_user: User = Depends(get_current_user),
):
    """Create a new brand to track."""
    # TODO: Get user from auth
    # For now, create a demo user or require user_id
    stmt = select(User).limit(1)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # Create demo user
        user = User(email="demo@snape.ai", name="Demo User", role=UserRole.FOUNDER, plan=Plan.PRO)
        db.add(user)
        await db.flush()

    # Check limit based on plan
    if user.plan == Plan.FREE:
        stmt = select(func.count(Brand.id)).where(Brand.user_id == user.id)
        result = await db.execute(stmt)
        count = result.scalar() or 0
        if count >= 1:
            raise HTTPException(status_code=403, detail="Free plan allows only 1 brand")

    brand = Brand(
        user_id=user.id,
        name=request.name,
        domain=str(request.domain) if request.domain else None,
        industry=request.industry,
        description=request.description,
        competitors=request.competitors,
        focus_keywords=request.focus_keywords,
    )
    db.add(brand)

    user.brands_count = (user.brands_count or 0) + 1

    await db.commit()
    await db.refresh(brand)

    return BrandResponse.from_orm(brand)


@router.post("/discover", response_model=BrandDiscoverResponse)
async def discover_brand(request: BrandDiscoverRequest):
    """Auto-discover brand information from name."""
    search_service = get_search_service()
    brand_data = await search_service.search_brand(request.name)

    if not brand_data:
        # Fallback: basic discovery
        return BrandDiscoverResponse(
            name=request.name,
            domain=None,
            industry=None,
            description=None,
            logo_url=None,
            colors=[],
            social_handles={},
            confidence=0.1,
        )

    return BrandDiscoverResponse(
        name=brand_data.get("name", request.name),
        domain=brand_data.get("domain"),
        industry=brand_data.get("industry"),
        description=brand_data.get("description"),
        logo_url=brand_data.get("logo"),
        colors=brand_data.get("colors", []),
        social_handles=brand_data.get("social", {}),
        confidence=brand_data.get("confidence", 0.8),
    )


@router.get("", response_model=List[BrandResponse])
async def list_brands(
    user_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    """List brands for a user."""
    # TODO: Get user from auth
    stmt = select(User).limit(1)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return []

    stmt = select(Brand).where(Brand.user_id == user.id).order_by(Brand.created_at.desc())
    result = await db.execute(stmt)
    brands = result.scalars().all()

    return [BrandResponse.from_orm(b) for b in brands]


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get brand details."""
    stmt = select(Brand).where(Brand.id == brand_id)
    result = await db.execute(stmt)
    brand = result.scalar_one_or_none()

    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Get analyses count
    from src.db.models import Analysis
    stmt = select(func.count(Analysis.id)).where(Analysis.brand_id == brand_id)
    result = await db.execute(stmt)
    analyses_count = result.scalar() or 0

    response = BrandResponse.from_orm(brand)
    response.analyses_count = analyses_count
    return response


@router.patch("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: UUID,
    request: BrandUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update brand details."""
    stmt = select(Brand).where(Brand.id == brand_id)
    result = await db.execute(stmt)
    brand = result.scalar_one_or_none()

    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "domain" and value:
            value = str(value)
        setattr(brand, field, value)

    await db.commit()
    await db.refresh(brand)

    return BrandResponse.from_orm(brand)


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(brand_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a brand."""
    stmt = select(Brand).where(Brand.id == brand_id)
    result = await db.execute(stmt)
    brand = result.scalar_one_or_none()

    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    await db.delete(brand)

    # Update user count
    stmt = select(User).where(User.id == brand.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        user.brands_count = max(0, (user.brands_count or 1) - 1)

    await db.commit()


@router.get("/{brand_id}/similar", response_model=List[Dict[str, Any]])
async def get_similar_brands(brand_id: UUID, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Find brands with similar profiles."""
    manager = BrandProfileManager(db)
    similar = await manager.get_similar_brands(brand_id, limit=limit)
    return similar