from typing import List, Optional
import openai
from openai import AsyncOpenAI

from src.core.config import settings


class Embedder:
    """Wrapper for OpenAI embeddings with caching and batching."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"
        self.dimensions = settings.VECTOR_DIMENSIONS

    async def embed(self, text: str) -> List[float]:
        """Embed a single text."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
            dimensions=self.dimensions,
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Embed multiple texts in batches."""
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = await self.client.embeddings.create(
                model=self.model,
                input=batch,
                dimensions=self.dimensions,
            )
            embeddings = [d.embedding for d in response.data]
            all_embeddings.extend(embeddings)
        return all_embeddings

    async def embed_query(self, query: str) -> List[float]:
        """Embed a search query (same as embed for this model)."""
        return await self.embed(query)


# Singleton
_embedder: Optional[Embedder] = None


def get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder