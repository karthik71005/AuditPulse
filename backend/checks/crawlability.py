from urllib.parse import urlparse
import httpx


async def check_crawlability(url: str) -> dict:
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    results = {
        "gptbot_blocked": False,
        "perplexity_blocked": False,
        "has_llms_txt": False,
        "llms_txt_valid": False,
        "robots_found": False,
        "details": [],
    }

    async with httpx.AsyncClient(
        timeout=8.0, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}
    ) as client:
        # 1. Inspect robots.txt
        try:
            robots_res = await client.get(f"{base_url}/robots.txt")
            if robots_res.status_code == 200:
                results["robots_found"] = True
                txt = robots_res.text.lower()
                if "user-agent: gptbot" in txt and "disallow: /" in txt:
                    results["gptbot_blocked"] = True
                if "user-agent: perplexitybot" in txt and "disallow: /" in txt:
                    results["perplexity_blocked"] = True
        except Exception:
            results["details"].append("Could not fetch robots.txt")

        # 2. Inspect /llms.txt
        try:
            llms_res = await client.get(f"{base_url}/llms.txt")
            if llms_res.status_code == 200 and len(llms_res.text.strip()) > 20:
                results["has_llms_txt"] = True
                if llms_res.text.strip().startswith("#") or ">" in llms_res.text:
                    results["llms_txt_valid"] = True
        except Exception:
            results["details"].append("Missing or invalid /llms.txt standard file")

    return results 
