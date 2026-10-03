import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from enum import Enum
import redis.asyncio as redis
from contextlib import asynccontextmanager

from src.core.config import settings


class PipelineStage(str, Enum):
    PLANNER = "planner"
    SEARCH = "search"
    EXTRACT = "extract"
    ANALYZE = "analyze"
    SYNTHESIZE = "synthesize"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class SubTask:
    id: str
    type: str  # search, extract, analyze
    query: str
    params: Dict[str, Any]
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0


@dataclass
class SearchResult:
    url: str
    title: str
    snippet: str
    source: str  # web, news, social, review
    relevance_score: float
    published_at: Optional[datetime] = None


@dataclass
class ExtractedDoc:
    url: str
    title: str
    content: str  # markdown
    metadata: Dict[str, Any]
    source_type: str
    extracted_at: datetime


@dataclass
class AnalysisResult:
    task_id: str
    insights: List[str]
    metrics: Dict[str, Any]
    citations: List[Dict[str, Any]]
    confidence: float


@dataclass
class JobContext:
    """Working memory for a single analysis job. Stored in Redis."""
    job_id: str
    analysis_id: str
    brand_id: str
    user_id: str
    analysis_type: str
    config: Dict[str, Any]

    # Planner output
    sub_tasks: List[SubTask] = field(default_factory=list)

    # Search results
    search_results: List[SearchResult] = field(default_factory=list)

    # Extracted documents
    extracted_docs: List[ExtractedDoc] = field(default_factory=list)

    # Analysis cache
    analysis_cache: Dict[str, AnalysisResult] = field(default_factory=dict)

    # Synthesis draft
    synthesis_draft: Optional[Dict[str, Any]] = None

    # Progress tracking
    current_stage: PipelineStage = PipelineStage.PLANNER
    stage_progress: Dict[str, int] = field(default_factory=dict)
    overall_progress: int = 0

    # Token budget
    token_budget: int = 100000
    tokens_used: int = 0

    # Timing
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Error handling
    error: Optional[str] = None
    retry_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # Convert datetime to ISO string
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        if self.started_at:
            data["started_at"] = self.started_at.isoformat()
        if self.completed_at:
            data["completed_at"] = self.completed_at.isoformat()
        # Convert enums
        data["current_stage"] = self.current_stage.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobContext":
        # Convert ISO strings back to datetime
        for key in ["created_at", "updated_at", "started_at", "completed_at"]:
            if data.get(key):
                data[key] = datetime.fromisoformat(data[key])
        # Convert sub_tasks
        data["sub_tasks"] = [SubTask(**st) for st in data.get("sub_tasks", [])]
        data["search_results"] = [SearchResult(**sr) for sr in data.get("search_results", [])]
        data["extracted_docs"] = [ExtractedDoc(**ed) for ed in data.get("extracted_docs", [])]
        data["analysis_cache"] = {k: AnalysisResult(**v) for k, v in data.get("analysis_cache", {}).items()}
        data["current_stage"] = PipelineStage(data["current_stage"])
        return cls(**data)


class JobContextManager:
    """Manages job context in Redis with TTL."""

    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.ttl_seconds = settings.JOB_TIMEOUT_SECONDS + 3600  # Job timeout + 1 hour buffer

    async def create(self, context: JobContext) -> None:
        key = f"job:{context.job_id}"
        await self.redis.set(key, json.dumps(context.to_dict()), ex=self.ttl_seconds)

    async def get(self, job_id: str) -> Optional[JobContext]:
        key = f"job:{job_id}"
        data = await self.redis.get(key)
        if data:
            return JobContext.from_dict(json.loads(data))
        return None

    async def update(self, context: JobContext) -> None:
        context.updated_at = datetime.utcnow()
        key = f"job:{context.job_id}"
        await self.redis.set(key, json.dumps(context.to_dict()), ex=self.ttl_seconds)

    async def delete(self, job_id: str) -> None:
        key = f"job:{job_id}"
        await self.redis.delete(key)

    async def exists(self, job_id: str) -> bool:
        key = f"job:{job_id}"
        return await self.redis.exists(key) > 0

    @asynccontextmanager
    async def transaction(self, job_id: str):
        """Context manager for atomic read-modify-write."""
        context = await self.get(job_id)
        if not context:
            raise ValueError(f"Job {job_id} not found")
        try:
            yield context
            await self.update(context)
        except Exception:
            # Don't update on error
            raise

    async def update_progress(
        self,
        job_id: str,
        stage: PipelineStage,
        progress: int,
        stage_progress: Optional[Dict[str, int]] = None,
    ) -> None:
        context = await self.get(job_id)
        if context:
            context.current_stage = stage
            context.overall_progress = progress
            if stage_progress:
                context.stage_progress.update(stage_progress)
            context.updated_at = datetime.utcnow()
            await self.update(context)

    async def add_sub_task(self, job_id: str, task: SubTask) -> None:
        context = await self.get(job_id)
        if context:
            context.sub_tasks.append(task)
            await self.update(context)

    async def update_sub_task(
        self,
        job_id: str,
        task_id: str,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        context = await self.get(job_id)
        if context:
            for task in context.sub_tasks:
                if task.id == task_id:
                    task.status = status
                    if result:
                        task.result = result
                    if error:
                        task.error = error
                    if status == "running":
                        task.started_at = datetime.utcnow()
                    elif status in ("completed", "failed"):
                        task.completed_at = datetime.utcnow()
                    break
            await self.update(context)

    async def add_search_results(self, job_id: str, results: List[SearchResult]) -> None:
        context = await self.get(job_id)
        if context:
            context.search_results.extend(results)
            await self.update(context)

    async def add_extracted_docs(self, job_id: str, docs: List[ExtractedDoc]) -> None:
        context = await self.get(job_id)
        if context:
            context.extracted_docs.extend(docs)
            await self.update(context)

    async def set_analysis_result(self, job_id: str, task_id: str, result: AnalysisResult) -> None:
        context = await self.get(job_id)
        if context:
            context.analysis_cache[task_id] = result
            await self.update(context)

    async def set_synthesis_draft(self, job_id: str, draft: Dict[str, Any]) -> None:
        context = await self.get(job_id)
        if context:
            context.synthesis_draft = draft
            await self.update(context)

    async def set_error(self, job_id: str, error: str) -> None:
        context = await self.get(job_id)
        if context:
            context.error = error
            context.current_stage = PipelineStage.FAILED
            await self.update(context)

    async def close(self) -> None:
        await self.redis.close()


# Singleton instance
_job_context_manager: Optional[JobContextManager] = None


def get_job_context_manager() -> JobContextManager:
    global _job_context_manager
    if _job_context_manager is None:
        _job_context_manager = JobContextManager()
    return _job_context_manager