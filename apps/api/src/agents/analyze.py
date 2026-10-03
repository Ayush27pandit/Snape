from typing import Dict, Any, List
from uuid import uuid4
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from src.agents.state import AgentState
from src.memory.job_context import SubTask, AnalysisResult, ExtractedDoc
from src.services.llm_service import get_llm_service
from src.memory.retriever import get_embedder, HybridRetriever
from src.db.session import get_db_context


class AnalysisOutput(BaseModel):
    """Structured output from analysis agent."""
    insights: List[str] = Field(description="Key insights discovered")
    metrics: Dict[str, Any] = Field(description="Quantitative metrics")
    citations: List[Dict[str, Any]] = Field(description="Citations supporting insights")
    confidence: float = Field(description="Confidence score 0-1", ge=0, le=1)


ANALYZER_SYSTEM_PROMPT = """You are a competitive intelligence analyst. Analyze the provided documents and extract:

1. Key insights (3-7 bullet points)
2. Quantitative metrics (sentiment scores, mention counts, pricing data, etc.)
3. Citations linking insights to specific documents
4. Overall confidence in your analysis

Focus on the specific focus areas: {focus_areas}

Return structured JSON only. Be specific and cite sources by URL."""


ANALYZER_USER_PROMPT = """Analyze these documents for {brand_name}:

Focus Areas: {focus_areas}
Analysis Type: {analysis_type}
Competitors: {competitors}

Documents:
{documents}

Provide insights, metrics, and citations."""


async def analyze_node(state: AgentState) -> AgentState:
    """Analyze agent node - extracts insights from documents."""
    llm = get_llm_service()
    embedder = get_embedder()

    # Get pending analyze tasks
    analyze_tasks = [t for t in state["sub_tasks"] if t.type == "analyze" and t.status == "pending"]

    # If no explicit tasks, create one per focus area
    if not analyze_tasks:
        focus_areas = state["config"].get("focus_areas", ["sentiment", "pricing", "product", "marketing"])
        for area in focus_areas:
            analyze_tasks.append(SubTask(
                id=f"analyze_{area}_{uuid4().hex[:8]}",
                type="analyze",
                query=f"Analyze {area} for {state['config'].get('brand_name', 'the brand')}",
                params={"focus_area": area},
                status="pending",
            ))

    # Prepare document context
    docs_text = ""
    for i, doc in enumerate(state["extracted_docs"][:20]):  # Limit to top 20 docs
        docs_text += f"\n--- Document {i+1} ---\n"
        docs_text += f"URL: {doc.url}\n"
        docs_text += f"Title: {doc.title}\n"
        docs_text += f"Content: {doc.content[:3000]}\n"

    brand_name = state["config"].get("brand_name", "the brand")
    competitors = state["config"].get("competitors", [])
    focus_areas = state["config"].get("focus_areas", ["sentiment", "pricing", "product", "marketing"])

    new_state = state.copy()

    for task in analyze_tasks:
        task.status = "running"

        try:
            focus_area = task.params.get("focus_area", "general")

            user_prompt = ANALYZER_USER_PROMPT.format(
                brand_name=brand_name,
                focus_areas=focus_area,
                analysis_type=state["analysis_type"],
                competitors=", ".join(competitors) if competitors else "N/A",
                documents=docs_text,
            )

            result = await llm.structured_complete(
                prompt=user_prompt,
                response_model=AnalysisOutput,
                system_prompt=ANALYZER_SYSTEM_PROMPT.format(focus_areas=focus_area),
                temperature=0.1,
            )

            analysis_result = AnalysisResult(
                task_id=task.id,
                insights=result.insights,
                metrics=result.metrics,
                citations=result.citations,
                confidence=result.confidence,
            )

            new_state["analysis_cache"][task.id] = analysis_result
            task.status = "completed"
            task.result = {
                "insights_count": len(result.insights),
                "metrics_keys": list(result.metrics.keys()),
                "confidence": result.confidence,
            }

        except Exception as e:
            task.status = "failed"
            task.error = str(e)

    new_state["sub_tasks"] = new_state["sub_tasks"]

    # Check if all analyze tasks done
    pending_analyze = [t for t in new_state["sub_tasks"] if t.type == "analyze" and t.status == "pending"]
    if not pending_analyze:
        new_state["current_stage"] = "synthesize"
        new_state["stage_progress"]["analyze"] = 100
        new_state["stage_progress"]["synthesize"] = 0
        new_state["overall_progress"] = 80

    new_state["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
    return new_state


def create_analyze_graph() -> StateGraph:
    """Create the analyze subgraph."""
    graph = StateGraph(AgentState)
    graph.add_node("analyze", analyze_node)
    graph.set_entry_point("analyze")
    graph.add_edge("analyze", END)
    return graph