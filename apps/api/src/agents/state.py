from typing import List, Dict, Any, Optional, TypedDict
from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.memory.job_context import PipelineStage, SubTask, SearchResult, ExtractedDoc, AnalysisResult


class AgentState(TypedDict):
    """LangGraph state for the multi-agent pipeline."""
    # Job identifiers
    job_id: str
    analysis_id: str
    brand_id: str
    user_id: str
    analysis_type: str

    # Configuration
    config: Dict[str, Any]

    # Planner output
    sub_tasks: List[SubTask]

    # Search results
    search_results: List[SearchResult]

    # Extracted documents
    extracted_docs: List[ExtractedDoc]

    # Analysis results
    analysis_cache: Dict[str, AnalysisResult]

    # Synthesis
    synthesis_draft: Optional[Dict[str, Any]]
    final_report: Optional[Dict[str, Any]]

    # Progress
    current_stage: PipelineStage
    stage_progress: Dict[str, int]
    overall_progress: int

    # Token budget
    token_budget: int
    tokens_used: int

    # Error handling
    error: Optional[str]
    retry_count: int

    # Timing
    created_at: str
    updated_at: str
    started_at: Optional[str]
    completed_at: Optional[str]


def create_initial_state(
    job_id: str,
    analysis_id: str,
    brand_id: str,
    user_id: str,
    analysis_type: str,
    config: Dict[str, Any],
) -> AgentState:
    """Create initial state for a new analysis job."""
    now = datetime.utcnow().isoformat()
    return AgentState(
        job_id=job_id,
        analysis_id=analysis_id,
        brand_id=brand_id,
        user_id=user_id,
        analysis_type=analysis_type,
        config=config,
        sub_tasks=[],
        search_results=[],
        extracted_docs=[],
        analysis_cache={},
        synthesis_draft=None,
        final_report=None,
        current_stage=PipelineStage.PLANNER,
        stage_progress={},
        overall_progress=0,
        token_budget=100000,
        tokens_used=0,
        error=None,
        retry_count=0,
        created_at=now,
        updated_at=now,
        started_at=None,
        completed_at=None,
    )