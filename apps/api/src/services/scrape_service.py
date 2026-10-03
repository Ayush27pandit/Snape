from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import httpx
from playwright.async_api import async_playwright, Browser, Page
import asyncio

from src.core.config import settings


@dataclass
class ScrapedPage:
    url: str
    title: str
    content: str  # markdown
    html: str
    metadata: Dict[str, Any]
    source_type: str
    scraped_at: datetime
    success: bool
    error: Optional[str] = None


class ScrapeService:
    """Playwright-based scraping with browser pool."""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context_key = settings.CONTEXT_API_KEY
        self.http_client = httpx.AsyncClient(timeout=60.0)
        self._pool: asyncio.Queue = asyncio.Queue()
        self._pool_size = 5
        self._initialized = False

    async def initialize(self):
        """Initialize browser pool."""
        if self._initialized:
            return

        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ],
        )

        # Pre-create pages
        for _ in range(self._pool_size):
            page = await self.browser.new_page()
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            await self._pool.put(page)

        self._initialized = True

    async def _get_page(self) -> Page:
        return await self._pool.get()

    async def _return_page(self, page: Page):
        await self._pool.put(page)

    async def scrape(
        self,
        url: str,
        wait_for: Optional[str] = None,
        timeout: int = 30000,
    ) -> ScrapedPage:
        """Scrape a single URL using Playwright."""
        if not self._initialized:
            await self.initialize()

        page = await self._get_page()
        try:
            response = await page.goto(url, wait_until="networkidle", timeout=timeout)
            if not response or response.status >= 400:
                return ScrapedPage(
                    url=url,
                    title="",
                    content="",
                    html="",
                    metadata={"status_code": response.status if response else 0},
                    source_type="web",
                    scraped_at=datetime.utcnow(),
                    success=False,
                    error=f"HTTP {response.status if response else 'No response'}",
                )

            if wait_for:
                await page.wait_for_selector(wait_for, timeout=5000)

            # Extract content
            title = await page.title()
            html = await page.content()

            # Get markdown via Context.dev if available, else extract from DOM
            content = await self._extract_markdown(page, url)

            return ScrapedPage(
                url=url,
                title=title,
                content=content,
                html=html,
                metadata={
                    "status_code": response.status,
                    "final_url": page.url,
                },
                source_type="web",
                scraped_at=datetime.utcnow(),
                success=True,
            )
        except Exception as e:
            return ScrapedPage(
                url=url,
                title="",
                content="",
                html="",
                metadata={},
                source_type="web",
                scraped_at=datetime.utcnow(),
                success=False,
                error=str(e),
            )
        finally:
            await self._return_page(page)

    async def _extract_markdown(self, page: Page, url: str) -> str:
        """Extract clean markdown from page."""
        # Try Context.dev first for best extraction
        if self.context_key:
            try:
                response = await self.http_client.post(
                    "https://api.context.dev/v1/extract",
                    headers={"Authorization": f"Bearer {self.context_key}"},
                    json={"url": url, "format": "markdown"},
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("markdown", "")
            except Exception:
                pass

        # Fallback: extract main content via DOM
        return await page.evaluate("""
            () => {
                // Remove scripts, styles, nav, footer, ads
                const remove = document.querySelectorAll('script, style, nav, footer, header, aside, [class*="ad"], [id*="ad"], .advertisement');
                remove.forEach(el => el.remove());

                // Try to find main content
                const main = document.querySelector('main, article, [role="main"], .content, #content, .post, .article');
                const root = main || document.body;

                // Convert to markdown-like text
                function toMarkdown(node) {
                    if (node.nodeType === Node.TEXT_NODE) {
                        return node.textContent.trim();
                    }
                    if (node.nodeType !== Node.ELEMENT_NODE) return '';

                    const tag = node.tagName.toLowerCase();
                    let prefix = '', suffix = '', newline = '';

                    if (['h1','h2','h3','h4','h5','h6'].includes(tag)) {
                        prefix = '#'.repeat(parseInt(tag[1])) + ' ';
                        suffix = '\\n\\n';
                    } else if (tag === 'p') {
                        suffix = '\\n\\n';
                    } else if (tag === 'br') {
                        return '\\n';
                    } else if (tag === 'a') {
                        const href = node.getAttribute('href');
                        const text = node.textContent.trim();
                        if (href && text) return `[${text}](${href})`;
                    } else if (['ul','ol'].includes(tag)) {
                        newline = '\\n';
                    } else if (tag === 'li') {
                        prefix = '- ';
                        suffix = '\\n';
                    }

                    let result = prefix;
                    for (const child of node.childNodes) {
                        result += toMarkdown(child);
                    }
                    return result + suffix + newline;
                }

                return toMarkdown(root).trim();
            }
        """)

    async def scrape_batch(
        self,
        urls: List[str],
        max_concurrent: int = 3,
    ) -> List[ScrapedPage]:
        """Scrape multiple URLs with concurrency control."""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def scrape_one(url: str) -> ScrapedPage:
            async with semaphore:
                return await self.scrape(url)

        tasks = [scrape_one(url) for url in urls]
        return await asyncio.gather(*tasks)

    async def close(self):
        """Clean up browser pool."""
        while not self._pool.empty():
            page = await self._pool.get()
            await page.close()
        if self.browser:
            await self.browser.close()
        await self.http_client.aclose()


# Singleton
_scrape_service: Optional[ScrapeService] = None


def get_scrape_service() -> ScrapeService:
    global _scrape_service
    if _scrape_service is None:
        _scrape_service = ScrapeService()
    return _scrape_service