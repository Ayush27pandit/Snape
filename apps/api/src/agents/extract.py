from typing import Dict, Any, List
from langgraph.graph import StateGraph, END

from src.agents.state import AgentState
from src.memory.job_context import SubTask, SearchResult, ExtractedDoc
from src.services.scrape_service import get_scrape_service


async def extract_node(state: AgentState) -> AgentState:
    """Extract agent node - scrapes full content from search results."""
    scrape_service = get_scrape_service()

    # Get pending extract tasks
    extract_tasks = [t for t in state["sub_tasks"] if t.type == "extract" and t.status == "pending"]

    # Also extract from search results if no explicit extract tasks
    urls_to_scrape = []

    for task in extract_tasks:
        urls_to_scrape.extend(task.params.get("urls", []))

    # If no explicit extract tasks, scrape top search results
    if not urls_to_scrape:
        # Get top 10 unique URLs from search results
        seen = set()
        for r in state["search_results"]:
            if r.url not in seen and r.relevance_score > 0.3:
                urls_to_scrape.append(r.url)
                seen.add(r.url)
                if len(urls_to_scrape) >= 10:
                    break

    all_docs = []

    if urls_to_scrape:
        # Scrape in batches
        scraped_pages = await scrape_service.scrape_batch(urls_to_scrape, max_concurrent=3)

        for page in scraped_pages:
            if page.success and page.content:
                doc = ExtractedDoc(
                    url=page.url,
                    title=page.title,
                    content=page.content[:50000],  # Limit content size
                    metadata=page.metadata,
                    source_type=page.source_type,
                    scraped_at=page.scraped_at,
                )
                all_docs.append(doc)

        # Mark extract tasks as completed
        for task in extract_tasks:
            task.status = "completed"
            task.result = {"scraped_count": len(all_docs), "urls": [d.url for d in all_docs]}

    # Update state
    new_state = state.copy()
    new_state["extracted_docs"] = state["extracted_docs"] + all_docs
    new_state["sub_tasks"] = state["sub_tasks"]

    # Check if all extract tasks done
    pending_extract = [t for t in state["sub_tasks"] if t.type == "extract" and t.status == "pending"]
    if not pending_extract:
        new_state["current_stage"] = "analyze"
        new_state["stage_progress"]["extract"] = 100
        new_state["stage_progress"]["analyze"] = 0
        new_state["overall_progress"] = 55

    new_state["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
    return new_state


def create_extract_graph() -> StateGraph:
    """Create the extract subgraph."""
    graph = StateGraph(AgentState)
    graph.add_node("extract", extract_node)
    graph.set_entry_point("extract")
    graph.add_edge("extract", END)
    return graph