import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from duckduckgo_search import DDGS
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from backend.ai_analyst import (
        enrich_findings_with_ai,
        generate_buyer_queries,
        generate_geo_narrative,
    )
    from backend.checks import (
        check_content_structure,
        check_crawlability,
        check_structured_schema,
    )
    from backend.crawler import scrape_target_site
    from backend.report import generate_actionable_report
    from backend.scorer import calculate_geo_score
except ModuleNotFoundError:
    from ai_analyst import (
        enrich_findings_with_ai,
        generate_buyer_queries,
        generate_geo_narrative,
    )
    from checks import (
        check_content_structure,
        check_crawlability,
        check_structured_schema,
    )
    from crawler import scrape_target_site
    from report import generate_actionable_report
    from scorer import calculate_geo_score

load_dotenv()

app = FastAPI(title="GEO Auditor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuditRequest(BaseModel):
    url: str


def run_ddg_search(query: str, target_domain: str) -> bool:
    """Zero-cost live web search check using duckduckgo-search"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            for r in results:
                href = r.get("href", "")
                if target_domain in href:
                    return True
    except Exception:
        pass
    return False


@app.post("/api/audit")
async def perform_audit(req: AuditRequest):
    target_url = req.url
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    # 1. Scrape target
    scrape_res = await scrape_target_site(target_url)
    if not scrape_res["success"]:
        raise HTTPException(
            status_code=400,
            detail=f"Could not reach target URL: {scrape_res.get('error')}",
        )

    is_partial = scrape_res.get("partial", False)
    scrape_warning = scrape_res.get("warning", "") if is_partial else ""

    domain = urlparse(scrape_res["url"]).netloc.replace("www.", "")
    title = scrape_res["title"]
    description = scrape_res.get("description", "")

    # 2. Run modular deterministic checks
    crawl_res = await check_crawlability(scrape_res["url"])
    schema_res = check_structured_schema(scrape_res["html"])
    content_res = check_content_structure(scrape_res["html"])

    # 3. AI-generated buyer queries (replaces hardcoded templates)
    queries_tested = generate_buyer_queries(title, description, domain)

    # 4. Live DuckDuckGo citation check
    citation_hits = 0
    citation_details = []
    for q in queries_tested:
        found = run_ddg_search(q, domain)
        citation_hits += int(found)
        citation_details.append({"query": q, "cited": found})

    # 5. Transparent score calculation
    scoring = calculate_geo_score(
        crawl_res, schema_res, content_res, citation_hits, len(queries_tested),
        domain=domain,
    )

    # 6. Rule-based actionable findings
    findings = generate_actionable_report(
        scrape_res["url"],
        title,
        crawl_res,
        schema_res,
        content_res,
        queries_tested,
        citation_hits,
    )

    # 7. AI: enrich each finding with site-specific insight
    findings = enrich_findings_with_ai(findings, title, description)

    # 8. AI: generate executive narrative summary
    ai_narrative = generate_geo_narrative(
        title=title,
        url=scrape_res["url"],
        description=description,
        overall_score=scoring["overall_score"],
        breakdown=scoring["breakdown"],
        crawl_res=crawl_res,
        schema_res=schema_res,
        content_res=content_res,
        citation_hits=citation_hits,
        total_queries=len(queries_tested),
    )

    return {
        "url": scrape_res["url"],
        "title": title,
        "description": description,
        "overall_score": scoring["overall_score"],
        "is_high_authority": scoring.get("is_high_authority", False),
        "scoring_notes": scoring.get("notes", []),
        "breakdown": scoring["breakdown"],
        "buyer_queries_tested": citation_details,
        "citation_hits": citation_hits,
        "findings": findings,
        "ai_narrative": ai_narrative,
        "scrape_warning": scrape_warning,
        "checks": {
            "crawlability": crawl_res,
            "schema": schema_res,
            "content": content_res,
        },
    }