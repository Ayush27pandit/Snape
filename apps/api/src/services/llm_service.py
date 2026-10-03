from typing import List, Dict, Any, Optional, Type, TypeVar
from pydantic import BaseModel
import instructor
from openai import AsyncOpenAI
import anthropic

from src.core.config import settings


T = TypeVar("T", bound=BaseModel)


class LLMService:
    """Unified LLM interface with structured output support."""

    def __init__(self):
        self.openai_client = instructor.from_openai(AsyncOpenAI(api_key=settings.OPENAI_API_KEY))
        self.anthropic_client = instructor.from_anthropic(AsyncOpenAI(
            api_key=settings.ANTHROPIC_API_KEY,
            base_url="https://api.anthropic.com/v1/",
        )) if settings.ANTHROPIC_API_KEY else None
        self.default_model = settings.DEFAULT_LLM_MODEL

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4000,
    ) -> str:
        """Simple text completion."""
        model = model or self.default_model
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def structured_complete(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4000,
    ) -> T:
        """Structured output using Instructor."""
        model = model or self.default_model
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            response_model=response_model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
    ):
        """Streaming completion."""
        model = model or self.default_model
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def count_tokens(self, text: str, model: Optional[str] = None) -> int:
        """Approximate token count."""
        # Rough approximation: 1 token ≈ 4 chars
        return len(text) // 4


# Singleton
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service