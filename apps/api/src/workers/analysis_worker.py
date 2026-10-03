import json
import uuid
from datetime import datetime
from typing import Dict, Any
from bullmq import Worker, Queue, Job
import asyncio

from src.core.config import settings
from src.db.session import get_db_context
from src.db.models import Analysis, JobStatus
from src.agents.pipeline import get_pipeline
from src.agents.state import create_initial_state
from src.memory.job_context import JobContextManager, PipelineStage, get_job_context_manager


class AnalysisWorker:
    """BullMQ worker for processing analysis jobs."""

    def __init__(self):
        self.worker: Worker = None
        self.queue: Queue = None
        self.context_manager = get_job_context_manager()

    async def initialize(self):
        """Initialize worker and queue."""
        self.queue = Queue("analysis", {"connection": {"url": settings.REDIS_URL}})
        self.worker = Worker(
            "analysis",
            self.process_job,
            {"connection": {"url": settings.REDIS_URL}, "concurrency": settings.JOB_CONCURRENCY},
        )

        # Event handlers
        self.worker.on("completed", self.on_completed)
        self.worker.on("failed", self.on_failed)
        self.worker.on("error", self.on_error)

    async def process_job(self, job: Job) -> Dict[str, Any]:
        """Process a single analysis job."""
        data = job.data
        analysis_id = data["analysisId"]
        job_id = data.get("jobId", str(uuid.uuid4()))

        # Update job progress
        await job.updateProgress(5)

        async with get_db_context() as db:
            # Get analysis record
            from sqlalchemy import select
            stmt = select(Analysis).where(Analysis.id == analysis_id)
            result = await db.execute(stmt)
            analysis = result.scalar_one_or_none()

            if not analysis:
                raise ValueError(f"Analysis {analysis_id} not found")

            # Update status to RUNNING
            analysis.status = JobStatus.RUNNING
            analysis.job_id = job_id
            analysis.started_at = datetime.utcnow()
            analysis.progress = 5
            analysis.current_stage = "initializing"

            # Get brand info
            from sqlalchemy import select
            from src.db.models import Brand
            stmt = select(Brand).where(Brand.id == analysis.brand_id)
            result = await db.execute(stmt)
            brand = result.scalar_one_or_none()

            if not brand:
                raise ValueError(f"Brand {analysis.brand_id} not found")

            # Create initial pipeline state
            initial_state = create_initial_state(
                job_id=job_id,
                analysis_id=str(analysis_id),
                brand_id=str(brand.id),
                user_id=str(analysis.user_id),
                analysis_type=analysis.type.value,
                config=analysis.input_config,
            )

            # Store initial job context
            from src.memory.job_context import JobContext
            context = JobContext(
                job_id=job_id,
                analysis_id=str(analysis_id),
                brand_id=str(brand.id),
                user_id=str(analysis.user_id),
                analysis_type=analysis.type.value,
                config=analysis.input_config,
            )
            await self.context_manager.create(context)

            # Run pipeline
            pipeline = get_pipeline()

            # Stream updates
            async for state in pipeline.astream(
                initial_state,
                config={"configurable": {"thread_id": job_id}},
            ):
                # Extract the latest state from the stream
                for node_name, node_state in state.items():
                    if isinstance(node_state, dict):
                        # Update progress in DB
                        analysis.progress = node_state.get("overall_progress", 0)
                        analysis.current_stage = node_state.get("current_stage", "unknown")
                        analysis.stage_progress = node_state.get("stage_progress", {})

                        # Update job context
                        context = await self.context_manager.get(job_id)
                        if context:
                            context.overall_progress = node_state.get("overall_progress", 0)
                            context.current_stage = PipelineStage(node_state.get("current_stage", "planner"))
                            context.stage_progress = node_state.get("stage_progress", {})
                            context.sub_tasks = node_state.get("sub_tasks", [])
                            context.search_results = node_state.get("search_results", [])
                            context.extracted_docs = node_state.get("extracted_docs", [])
                            context.analysis_cache = node_state.get("analysis_cache", {})
                            context.synthesis_draft = node_state.get("synthesis_draft")
                            context.error = node_state.get("error")
                            await self.context_manager.update(context)

                        # Update BullMQ progress
                        await job.updateProgress(analysis.progress)

            # Get final state
            final_state = await pipeline.aget_state({"configurable": {"thread_id": job_id}})
            state_values = final_state.values

            # Save final report
            if state_values.get("final_report"):
                analysis.result = state_values["final_report"]
                analysis.status = JobStatus.COMPLETED
                analysis.completed_at = datetime.utcnow()
                analysis.progress = 100
                analysis.current_stage = "complete"
            else:
                analysis.status = JobStatus.FAILED
                analysis.error = state_values.get("error", "Unknown error")
                analysis.completed_at = datetime.utcnow()

            await db.commit()

            return {"status": analysis.status.value, "analysis_id": str(analysis_id)}

    async def on_completed(self, job: Job, result: Any):
        """Handle job completion."""
        print(f"Job {job.id} completed: {result}")

    async def on_failed(self, job: Job, error: Exception):
        """Handle job failure."""
        print(f"Job {job.id} failed: {error}")
        # Update analysis status in DB
        try:
            async with get_db_context() as db:
                from sqlalchemy import select
                job_data = job.data
                analysis_id = job_data.get("analysisId")
                if analysis_id:
                    stmt = select(Analysis).where(Analysis.id == analysis_id)
                    result = await db.execute(stmt)
                    analysis = result.scalar_one_or_none()
                    if analysis:
                        analysis.status = JobStatus.FAILED
                        analysis.error = str(error)
                        analysis.completed_at = datetime.utcnow()
                        await db.commit()
        except Exception as e:
            print(f"Failed to update analysis status: {e}")

    async def on_error(self, error: Exception):
        """Handle worker errors."""
        print(f"Worker error: {error}")

    async def close(self):
        """Close worker."""
        if self.worker:
            await self.worker.close()
        if self.queue:
            await self.queue.close()
        await self.context_manager.close()


# Singleton
_worker: AnalysisWorker = None


async def get_worker() -> AnalysisWorker:
    global _worker
    if _worker is None:
        _worker = AnalysisWorker()
        await _worker.initialize()
    return _worker


async def start_worker():
    """Start the analysis worker."""
    worker = await get_worker()
    print("Analysis worker started")
    # Keep running
    await asyncio.Event().wait()