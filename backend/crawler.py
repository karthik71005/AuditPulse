import asyncio
import random
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Browser-realistic User-Agent pool — rotated per request to avoid simple
# bot-detection filters like Wikipedia's.
# ---------------------------------------------------------------------------
_USER_AGENTS = [
    # Chrome 124 / Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # Chrome 124 / macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # Firefox 125 / Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    # Safari / macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    # Edge / Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
]


def _browser_headers(ua: str) -> dict:
    """Return a realistic browser header set for the given User-Agent."""
    return {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
    }


async def _try_fetch(client: httpx.AsyncClient, url: str, ua: str) -> httpx.Response:
    headers = _browser_headers(ua)
    response = await client.get(url, headers=headers)
    response.raise_for_status()
    return response


async def scrape_target_site(url: str) -> dict:
    """
    Scrape the target URL with browser-realistic headers.

    Strategy:
      1. Try each User-Agent in random order (up to 3 attempts).
      2. On 403/429, wait briefly and retry.
      3. On persistent failure, return partial=True with empty HTML so that
         crawlability and citation checks (which don't need HTML) still run.
    """
    agents = random.sample(_USER_AGENTS, len(_USER_AGENTS))

    async with httpx.AsyncClient(
        timeout=15.0,
        follow_redirects=True,
        # Don't verify aggressively — some sites have cert quirks
    ) as client:
        last_error = None

        for attempt, ua in enumerate(agents[:3]):
            try:
                res = await _try_fetch(client, url, ua)
                html = res.text
                soup = BeautifulSoup(html, "html.parser")

                title = (
                    soup.title.string.strip()
                    if soup.title
                    else urlparse(url).netloc
                )
                meta_desc = ""
                meta_tag = soup.find("meta", attrs={"name": "description"})
                if meta_tag and meta_tag.get("content"):
                    meta_desc = str(meta_tag.get("content")).strip()

                return {
                    "success": True,
                    "partial": False,
                    "url": str(res.url),
                    "title": title,
                    "description": meta_desc,
                    "html": html,
                }

            except httpx.HTTPStatusError as exc:
                last_error = exc
                status = exc.response.status_code

                if status in (403, 429, 503):
                    # Anti-bot wall — wait and try next UA
                    if attempt < 2:
                        await asyncio.sleep(1.5)
                    continue
                else:
                    # Non-retryable HTTP error (404, 500, etc.)
                    break

            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                last_error = exc
                break

            except Exception as exc:
                last_error = exc
                break

        # ── Graceful degradation ────────────────────────────────────────
        # For 403 sites (Wikipedia, paywalled, etc.) we can still run:
        #   - robots.txt / llms.txt checks  (don't need page HTML)
        #   - DuckDuckGo citation check     (don't need page HTML)
        # We skip schema and content checks (return empty results).
        netloc = urlparse(url).netloc
        is_forbidden = (
            isinstance(last_error, httpx.HTTPStatusError)
            and last_error.response.status_code == 403
        )

        if is_forbidden:
            # Infer title from domain for the report
            domain_name = netloc.replace("www.", "").split(".")[0].capitalize()
            return {
                "success": True,          # allow audit to continue
                "partial": True,          # flag: HTML checks will be skipped
                "url": url,
                "title": domain_name,
                "description": "",
                "html": "",              # empty — schema + content checks gracefully return empty
                "warning": (
                    f"The target site returned 403 Forbidden — it actively blocks scrapers. "
                    f"AI bot access, schema, and content checks were skipped. "
                    f"Crawlability and citation checks still ran."
                ),
            }

        return {
            "success": False,
            "partial": False,
            "url": url,
            "title": netloc,
            "description": "",
            "html": "",
            "error": str(last_error),
        }
