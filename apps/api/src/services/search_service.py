from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import httpx
from tavily import TavilyClient

from src.core.config import settings


@dataclass
class SearchResult:
    url: str
    title: str
    snippet: str
    source: str  # web, news, social, review
    relevance_score: float
    published_at: Optional[datetime] = None
    raw_content: Optional[str] = None


class SearchService:
    """Unified search interface using Tavily (primary) with Context.dev fallback."""

    def __init__(self):
        self.tavily = TavilyClient(api_key=settings.TAVILY_API_KEY) if settings.TAVILY_API_KEY else None
        self.context_key = settings.CONTEXT_API_KEY
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def search(
        self,
        query: str,
        max_results: int = 10,
        search_depth: str = "basic",  # basic, advanced
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        topic: str = "general",  # general, news
        days_back: int = 30,
    ) -> List[SearchResult]:
        """Search using Tavily."""
        if not self.tavily:
            return await self._search_context_dev(query, max_results, topic, days_back)

        try:
            response = self.tavily.search(
                query=query,
                max_results=max_results,
                search_depth=search_depth,
                include_domains=include_domains,
                exclude_domains=exclude_domains,
                topic=topic,
                days_back=days_back,
                include_raw_content=True,
            )

            results = []
            for r in response.get("results", []):
                results.append(SearchResult(
                    url=r.get("url", ""),
                    title=r.get("title", ""),
                    snippet=r.get("content", ""),
                    source=topic,
                    relevance_score=r.get("score", 0.0),
                    raw_content=r.get("raw_content"),
                ))
            return results
        except Exception as e:
            # Fallback to Context.dev
            return await self._search_context_dev(query, max_results, topic, days_back)

    async def _search_context_dev(
        self,
        query: str,
        max_results: int,
        topic: str,
        days_back: int,
    ) -> List[SearchResult]:
        """Fallback search using Context.dev."""
        if not self.context_key:
            return []

        try:
            response = await self.http_client.post(
                "https://api.context.dev/v1/search",
                headers={"Authorization": f"Bearer {self.context_key}"},
                json={
                    "query": query,
                    "limit": max_results,
                    "recency_days": days_back,
                },
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for r in data.get("results", []):
                results.append(SearchResult(
                    url=r.get("url", ""),
                    title=r.get("title", ""),
                    snippet=r.get("snippet", ""),
                    source=r.get("source_type", topic),
                    relevance_score=r.get("score", 0.0),
                ))
            return results
        except Exception:
            return []

    async def search_brand(self, brand_name: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """Get brand intelligence from Context.dev."""
        if not self.context_key:
            return {}

        try:
            payload = {"name": brand_name}
            if domain:
                payload["domain"] = domain

            response = await self.http_client.post(
                "https://api.context.dev/v1/brand/retrieve",
                headers={"Authorization": f"Bearer {self.context_key}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {}

    async def search_competitors(self, brand_name: str, industry: str, limit: int = 10) -> List[str]:
        """Search for competitor brand names."""
        query = f"{brand_name} competitors {industry} companies"
        results = await self.search(query, max_results=limit, search_depth="advanced")

        # Extract potential competitor names from snippets
        competitors = []
        for r in results:
            # Simple extraction - in practice use NER
            competitors.append(r.title)

        return list(set(competitors))[:limit]

    async def close(self):
        await self.http_client.aclose()


# Singleton
_search_service: Optional[SearchService] = None


def get_search_service() -> SearchService:
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service