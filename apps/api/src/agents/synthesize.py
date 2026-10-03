from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from src.agents.state import AgentState
from src.memory.job_context import SubTask, AnalysisResult
from src.services.llm_service import get_llm_service


class SynthesisOutput(BaseModel):
    """Structured final report."""
    executive_summary: str = Field(description="2-3 paragraph executive summary")
    brand_overview: Dict[str, Any] = Field(description="Brand profile summary")
    competitor_comparison: List[Dict[str, Any]] = Field(description="Side-by-side competitor data")
    sentiment_analysis: Dict[str, Any] = Field(description="Sentiment breakdown")
    news_and_articles: List[Dict[str, Any]] = Field(description="Recent news with links")
    public_opinion: Dict[str, Any] = Field(description="Social/review sentiment")
    recommendations: List[str] = Field(description="Actionable recommendations")
    citations: List[Dict[str, Any]] = Field(description="All citations")


SYNTHESIZER_SYSTEM_PROMPT = """You are a competitive intelligence report writer. Synthesize all analysis into a comprehensive, well-structured report.

Create a report with:
1. Executive Summary (2-3 paragraphs)
2. Brand Overview (key facts, positioning)
3. Competitor Comparison (table-ready data for each rival)
4. Sentiment Analysis (overall, by channel, trends)
5. News & Articles (recent, with links, sentiment)
6. Public Opinion (Reddit, Twitter, reviews, forums)
7. Recommendations (prioritized, actionable)
8. Citations (every claim backed by source)

Be specific, use data, cite everything. Return structured JSON."""


SYNTHESIZER_USER_PROMPT = """Synthesize this competitive intelligence analysis:

Brand: {brand_name}
Analysis Type: {analysis_type}
Competitors: {competitors}

Analysis Results:
{analysis_results}

Search Results Count: {search_count}
Extracted Documents: {doc_count}

Generate the complete report."""


async def synthesize_node(state: AgentState) -> AgentState:
    """Synthesize agent node - creates final report."""
    llm = get_llm_service()

    # Collect all analysis results
    analysis_summary = ""
    for task_id, result in state["analysis_cache"].items():
        analysis_summary += f"\n--- Task {task_id} ---\n"
        analysis_summary += f"Insights: {'; '.join(result.insights)}\n"
        analysis_summary += f"Metrics: {result.metrics}\n"
        analysis_summary += f"Confidence: {result.confidence}\n"

    brand_name = state["config"].get("brand_name", "the brand")
    competitors = state["config"].get("competitors", [])

    user_prompt = SYNTHESIZER_USER_PROMPT.format(
        brand_name=brand_name,
        analysis_type=state["analysis_type"],
        competitors=", ".join(competitors) if competitors else "N/A",
        analysis_results=analysis_summary,
        search_count=len(state["search_results"]),
        doc_count=len(state["extracted_docs"]),
    )

    try:
        result = await llm.structured_complete(
            prompt=user_prompt,
            response_model=SynthesisOutput,
            system_prompt=SYNTHESIZER_SYSTEM_PROMPT,
            temperature=0.2,
        )

        # Build final report
        final_report = {
            "executiveSummary": result.executive_summary,
            "brandOverview": result.brand_overview,
            "competitorComparison": result.competitor_comparison,
            "sentimentAnalysis": result.sentiment_analysis,
            "newsAndArticles": result.news_and_articles,
            "publicOpinion": result.public_opinion,
            "recommendations": result.recommendations,
            "citations": result.citations,
            "metadata": {
                "analysisId": state["analysis_id"],
                "brandId": state["brand_id"],
                "analysisType": state["analysis_type"],
                "searchResultsCount": len(state["search_results"]),
                "documentsAnalyzed": len(state["extracted_docs"]),
                "analysisTasksCompleted": len([t for t in state["sub_tasks"] if t.status == "completed"]),
            },
        }

        new_state = state.copy()
        new_state["final_report"] = final_report
        new_state["current_stage"] = "complete"
        new_state["stage_progress"]["synthesize"] = 100
        new_state["overall_progress"] = 100

        # Mark any synthesis tasks as completed
        for task in new_state["sub_tasks"]:
            if task.type == "synthesize" and task.status == "pending":
                task.status = "completed"
                task.result = {"report_generated": True}

    except Exception as e:
        new_state = state.copy()
        new_state["error"] = f"Synthesis failed: {str(e)}"
        new_state["current_stage"] = "failed"

    new_state["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
    new_state["completed_at"] = __import__("datetime").datetime.utcnow().isoformat()
    return new_state


def create_synthesize_graph() -> StateGraph:
    """Create the synthesize subgraph."""
    graph = StateGraph(AgentState)
    graph.add_node("synthesize", synthesize_node)
    graph.set_entry_point("synthesize")
    graph.add_edge("synthesize", END)
    return graph