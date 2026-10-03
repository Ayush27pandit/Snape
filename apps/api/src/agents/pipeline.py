from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.agents.state import AgentState
from src.agents.planner import planner_node
from src.agents.search import search_node
from src.agents.extract import extract_node
from src.agents.analyze import analyze_node
from src.agents.synthesize import synthesize_node


def should_continue(state: AgentState) -> str:
    """Determine next stage based on current state."""
    stage = state["current_stage"]

    if stage == "planner":
        return "search"
    elif stage == "search":
        # Check if search tasks completed
        pending = [t for t in state["sub_tasks"] if t.type == "search" and t.status == "pending"]
        if pending:
            return "search"
        return "extract"
    elif stage == "extract":
        pending = [t for t in state["sub_tasks"] if t.type == "extract" and t.status == "pending"]
        if pending:
            return "extract"
        return "analyze"
    elif stage == "analyze":
        pending = [t for t in state["sub_tasks"] if t.type == "analyze" and t.status == "pending"]
        if pending:
            return "analyze"
        return "synthesize"
    elif stage == "synthesize":
        return "complete"
    elif stage in ("complete", "failed"):
        return END
    return END


def create_analysis_pipeline() -> StateGraph:
    """Create the complete multi-agent analysis pipeline."""
    graph = StateGraph(AgentState)

    # Add all agent nodes
    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("extract", extract_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("synthesize", synthesize_node)

    # Set entry point
    graph.set_entry_point("planner")

    # Add conditional edges
    graph.add_conditional_edges(
        "planner",
        should_continue,
        {
            "search": "search",
            END: END,
        },
    )
    graph.add_conditional_edges(
        "search",
        should_continue,
        {
            "search": "search",
            "extract": "extract",
            END: END,
        },
    )
    graph.add_conditional_edges(
        "extract",
        should_continue,
        {
            "extract": "extract",
            "analyze": "analyze",
            END: END,
        },
    )
    graph.add_conditional_edges(
        "analyze",
        should_continue,
        {
            "analyze": "analyze",
            "synthesize": "synthesize",
            END: END,
        },
    )
    graph.add_conditional_edges(
        "synthesize",
        should_continue,
        {
            "complete": END,
            END: END,
        },
    )

    # Compile with checkpointing for resilience
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


# Global pipeline instance
_pipeline = None


def get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = create_analysis_pipeline()
    return _pipeline