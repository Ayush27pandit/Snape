from typing import Dict, Any, List
from langgraph.graph import StateGraph, END

from src.agents.state import AgentState
from src.memory.job_context import SubTask, SearchResult
from src.services.search_service import get_search_service


async def search_node(state: AgentState) -> AgentState:
    """Search agent node - executes search sub-tasks."""
    search_service = get_search_service()

    # Get pending search tasks
    search_tasks = [t for t in state["sub_tasks"] if t.type == "search" and t.status == "pending"]

    all_results = []

    for task in search_tasks:
        # Update task status
        task.status = "running"

        try:
            # Execute search
            results = await search_service.search(
                query=task.query,
                max_results=task.params.get("max_results", 10),
                search_depth=task.params.get("depth", "basic"),
                topic=task.params.get("topic", "general"),
                days_back=task.params.get("days_back", 30),
                include_domains=task.params.get("include_domains"),
                exclude_domains=task.params.get("exclude_domains"),
            )

            # Convert to SearchResult objects
            search_results = [
                SearchResult(
                    url=r.url,
                    title=r.title,
                    snippet=r.snippet,
                    source=r.source,
                    relevance_score=r.relevance_score,
                    published_at=r.published_at,
                    raw_content=r.raw_content,
                )
                for r in results
            ]

            all_results.extend(search_results)
            task.status = "completed"
            task.result = {"count": len(search_results), "urls": [r.url for r in search_results]}

        except Exception as e:
            task.status = "failed"
            task.error = str(e)

    # Update state
    new_state = state.copy()
    new_state["search_results"] = state["search_results"] + all_results
    new_state["sub_tasks"] = state["sub_tasks"]

    # Check if all search tasks done
    pending_search = [t for t in state["sub_tasks"] if t.type == "search" and t.status == "pending"]
    if not pending_search:
        new_state["current_stage"] = "extract"
        new_state["stage_progress"]["search"] = 100
        new_state["stage_progress"]["extract"] = 0
        new_state["overall_progress"] = 30

    new_state["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
    return new_state


def create_search_graph() -> StateGraph:
    """Create the search subgraph."""
    graph = StateGraph(AgentState)
    graph.add_node("search", search_node)
    graph.set_entry_point("search")
    graph.add_edge("search", END)
    return graph