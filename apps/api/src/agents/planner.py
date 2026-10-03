from typing import Dict, Any, List
from uuid import uuid4
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from src.agents.state import AgentState, create_initial_state
from src.memory.job_context import SubTask
from src.services.llm_service import get_llm_service


class PlannerOutput(BaseModel):
    """Structured output from the planner agent."""
    sub_tasks: List[Dict[str, Any]] = Field(
        description="List of sub-tasks to execute",
        min_items=1,
        max_items=10,
    )
    strategy: str = Field(description="Overall analysis strategy")
    estimated_duration_seconds: int = Field(description="Estimated time to complete")


PLANNER_SYSTEM_PROMPT = """You are a competitive intelligence planner. Your job is to break down a brand analysis request into specific, executable sub-tasks.

Given a brand analysis request, create a plan that covers:
1. What information to search for
2. What sources to prioritize
3. What specific metrics to extract
4. How to structure the final comparison

Analysis Types:
- DEEP_DIVE: Comprehensive single brand analysis
- COMPETITOR_COMPARISON: Side-by-side comparison with rivals
- MARKET_LANDSCAPE: Category-wide view of top players
- CAMPAIGN_TRACKING: Specific event/campaign impact

For each sub-task, specify:
- type: "search", "extract", or "analyze"
- query: The search query or analysis prompt
- params: Additional parameters (source types, depth, etc.)
- priority: 1-5 (1=highest)

Return structured JSON only."""


PLANNER_USER_PROMPT = """Analyze this request and create an execution plan:

Brand: {brand_name}
Analysis Type: {analysis_type}
Competitors: {competitors}
Date Range: {date_range}
Focus Areas: {focus_areas}
Depth: {depth}

Config: {config}"""


async def planner_node(state: AgentState) -> AgentState:
    """Planner agent node - creates execution plan."""
    llm = get_llm_service()

    # Build prompt
    brand_name = state["config"].get("brand_name", "the brand")
    competitors = state["config"].get("competitors", [])
    date_range = state["config"].get("date_range", "LAST_30_DAYS")
    focus_areas = state["config"].get("focus_areas", ["sentiment", "pricing", "product", "marketing"])
    depth = state["config"].get("depth", "deep")

    user_prompt = PLANNER_USER_PROMPT.format(
        brand_name=brand_name,
        analysis_type=state["analysis_type"],
        competitors=", ".join(competitors) if competitors else "auto-discover",
        date_range=date_range,
        focus_areas=", ".join(focus_areas),
        depth=depth,
        config=state["config"],
    )

    # Get structured plan
    plan = await llm.structured_complete(
        prompt=user_prompt,
        response_model=PlannerOutput,
        system_prompt=PLANNER_SYSTEM_PROMPT,
        temperature=0.2,
    )

    # Convert to SubTask objects
    sub_tasks = []
    for i, task in enumerate(plan.sub_tasks):
        sub_tasks.append(SubTask(
            id=f"task_{i}_{uuid4().hex[:8]}",
            type=task.get("type", "search"),
            query=task.get("query", ""),
            params=task.get("params", {}),
            status="pending",
        ))

    # Update state
    new_state = state.copy()
    new_state["sub_tasks"] = sub_tasks
    new_state["current_stage"] = "search"
    new_state["stage_progress"] = {"planner": 100, "search": 0, "extract": 0, "analyze": 0, "synthesize": 0}
    new_state["overall_progress"] = 10
    new_state["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()

    return new_state


def create_planner_graph() -> StateGraph:
    """Create the planner subgraph."""
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", END)
    return graph