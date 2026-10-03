from typing import Dict, Any, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from src.db.session import get_db
from src.db.models import Analysis, Brand, User, JobStatus, AnalysisType
from src.workers.analysis_worker import get_worker
from src.memory.job_context import get_job_context_manager
from bullmq import Queue

router = APIRouter(prefix="/analyze", tags=["analyze"])


class AnalysisStartRequest(BaseModel):
    brand_id: UUID
    type: AnalysisType
    competitors: List[UUID] = Field(default_factory=list)
    date_range: str = "LAST_30_DAYS"
    focus_areas: List[str] = Field(default_factory=lambda: ["sentiment", "pricing", "product", "marketing"])
    depth: str = "deep"  # quick, deep, comprehensive
    max_sources: int = 20


class AnalysisStartResponse(BaseModel):
    job_id: str
    analysis_id: UUID
    status: JobStatus
    estimated_duration_seconds: int


class AnalysisStatusResponse(BaseModel):
    job_id: str
    analysis_id: UUID
    status: JobStatus
    progress: int
    current_stage: str
    stage_progress: Dict[str, int]
    error: Optional[str] = None


class AnalysisResultResponse(BaseModel):
    analysis_id: UUID
    report: Dict[str, Any]


@router.post("/start", response_model=AnalysisStartResponse, status_code=status.HTTP_202_ACCEPTED)
async def start_analysis(
    request: AnalysisStartRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Start a new analysis job."""
    # Verify brand exists and belongs to user (TODO: add auth)
    stmt = select(Brand).where(Brand.id == request.brand_id)
    result = await db.execute(stmt)
    brand = result.scalar_one_or_none()

    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Create analysis record
    competitor_ids = [str(c) for c in request.competitors]
    if not competitor_ids and brand.competitors:
        competitor_ids = brand.competitors

    analysis = Analysis(
        brand_id=request.brand_id,
        user_id=brand.user_id,
        type=request.type,
        status=JobStatus.PENDING,
        input_config={
            "brand_name": brand.name,
            "competitors": competitor_ids,
            "date_range": request.date_range,
            "focus_areas": request.focus_areas,
            "depth": request.depth,
            "max_sources": request.max_sources,
        },
    )
    db.add(analysis)
    await db.flush()

    # Update brand stats
    brand.analyses_count = (brand.analyses_count or 0) + 1

    await db.commit()

    # Queue job
    worker = await get_worker()
    job_id = str(uuid.uuid4())

    await worker.queue.add(
        "analysis",
        {
            "analysisId": str(analysis.id),
            "jobId": job_id,
        },
        {
            "jobId": job_id,
            "priority": 1,
            "attempts": settings.JOB_MAX_RETRIES + 1,
            "timeout": settings.JOB_TIMEOUT_SECONDS * 1000,
        },
    )

    return AnalysisStartResponse(
        job_id=job_id,
        analysis_id=analysis.id,
        status=JobStatus.PENDING,
        estimated_duration_seconds=120 if request.depth == "quick" else 300,
    )


@router.get("/status/{job_id}", response_model=AnalysisStatusResponse)
async def get_analysis_status(job_id: str):
    """Get real-time analysis status."""
    context_manager = get_job_context_manager()
    context = await context_manager.get(job_id)

    if not context:
        # Fallback to DB
        async with get_db_context() as db:
            stmt = select(Analysis).where(Analysis.job_id == job_id)
            result = await db.execute(stmt)
            analysis = result.scalar_one_or_none()
            if not analysis:
                raise HTTPException(status_code=404, detail="Analysis not found")

            return AnalysisStatusResponse(
                job_id=job_id,
                analysis_id=analysis.id,
                status=analysis.status,
                progress=analysis.progress,
                current_stage=analysis.current_stage,
                stage_progress=analysis.stage_progress,
                error=analysis.error,
            )

    return AnalysisStatusResponse(
        job_id=job_id,
        analysis_id=UUID(context.analysis_id),
        status=JobStatus.COMPLETED if context.current_stage.value == "complete" else JobStatus.RUNNING,
        progress=context.overall_progress,
        current_stage=context.current_stage.value,
        stage_progress=context.stage_progress,
        error=context.error,
    )


@router.get("/result/{job_id}", response_model=AnalysisResultResponse)
async def get_analysis_result(job_id: str):
    """Get completed analysis result."""
    context_manager = get_job_context_manager()
    context = await context_manager.get(job_id)

    if not context or not context.synthesis_draft:
        # Fallback to DB
        async with get_db_context() as db:
            stmt = select(Analysis).where(Analysis.job_id == job_id)
            result = await db.execute(stmt)
            analysis = result.scalar_one_or_none()
            if not analysis:
                raise HTTPException(status_code=404, detail="Analysis not found")

            if analysis.status != JobStatus.COMPLETED:
                raise HTTPException(status_code=400, detail="Analysis not completed")

            return AnalysisResultResponse(
                analysis_id=analysis.id,
                report=analysis.result or {},
            )

    return AnalysisResultResponse(
        analysis_id=UUID(context.analysis_id),
        report=context.synthesis_draft,
    )


@router.get("/list", response_model=List[Dict[str, Any]])
async def list_analyses(
    brand_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
    status: Optional[JobStatus] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List analyses with filters."""
    stmt = select(Analysis).order_by(Analysis.created_at.desc()).limit(limit).offset(offset)

    if brand_id:
        stmt = stmt.where(Analysis.brand_id == brand_id)
    if user_id:
        stmt = stmt.where(Analysis.user_id == user_id)
    if status:
        stmt = stmt.where(Analysis.status == status)

    result = await db.execute(stmt)
    analyses = result.scalars().all()

    return [
        {
            "id": str(a.id),
            "brand_id": str(a.brand_id),
            "type": a.type.value,
            "status": a.status.value,
            "progress": a.progress,
            "created_at": a.created_at.isoformat(),
            "completed_at": a.completed_at.isoformat() if a.completed_at else None,
        }
        for a in analyses
    ]