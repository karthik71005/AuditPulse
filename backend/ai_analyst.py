"""
ai_analyst.py — Groq-powered AI intelligence layer for GEO Auditor.

Three responsibilities:
  1. generate_buyer_queries()  — tailored buyer-intent queries for the specific business
  2. generate_geo_narrative()  — plain-English executive summary for business owners
  3. enrich_findings_with_ai() — site-specific "why this matters" for each finding

All functions degrade gracefully: if Groq is unavailable, fallback values are returned
and the audit continues without error.

Model: llama-3.3-70b-versatile (fast, high-quality, Groq free-tier friendly)
"""

import json
import logging
import os
import re

from groq import Groq

logger = logging.getLogger(__name__)

GROQ_MODEL = "llama-3.3-70b-versatile"


def _get_client() -> Groq | None:
    """Return a Groq client if GROQ_API_KEY is set, else None."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key_here":
        logger.warning("GROQ_API_KEY not set — AI features disabled, using rule-based fallbacks.")
        return None
    return Groq(api_key=api_key)


def _chat(client: Groq, system: str, user: str, max_tokens: int = 512) -> str | None:
    """
    Helper: send a single system+user message to Groq.
    Returns the response text or None on error.
    """
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=0.4,
        )
        return completion.choices[0].message.content.strip()
    except Exception as exc:
        logger.error("Groq API error: %s", exc)
        return None


# ---------------------------------------------------------------------------
# 1. Buyer Query Generation
# ---------------------------------------------------------------------------

def generate_buyer_queries(title: str, description: str, domain: str) -> list[str]:
    """
    Generate 3 buyer-intent search queries tailored to the specific business.

    Without AI: queries are generic templates ("<title> reviews", etc.)
    With AI: queries reflect what a real buyer would type when researching THIS business.

    Falls back to rule-based templates if Groq is unavailable.
    """
    fallback = [
        f"best alternatives to {title}",
        f"top software similar to {title}",
        f"{title} reviews and features",
    ]

    client = _get_client()
    if not client:
        return fallback

    system = (
        "You are an expert in AI search and Generative Engine Optimization (GEO). "
        "Your job is to generate realistic buyer-intent search queries that a potential customer "
        "would type into ChatGPT, Perplexity, or Google AI Overviews when looking for a product or service "
        "like this one. Queries must be specific to this business, not generic.\n\n"
        "Respond with ONLY a JSON array of exactly 3 query strings. No explanation, no markdown, no code fences."
    )

    user = (
        f"Business name / page title: {title}\n"
        f"Domain: {domain}\n"
        f"Meta description: {description or 'Not provided'}\n\n"
        "Generate 3 buyer-intent queries a real potential customer would ask an AI assistant about this business."
    )

    raw = _chat(client, system, user, max_tokens=200)
    if not raw:
        return fallback

    # Extract JSON array from response
    try:
        # Find a JSON array in the response
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            queries = json.loads(match.group())
            if isinstance(queries, list) and len(queries) >= 1:
                return [str(q) for q in queries[:3]]
    except (json.JSONDecodeError, ValueError):
        pass

    logger.warning("Could not parse Groq query response — using fallback queries.")
    return fallback


# ---------------------------------------------------------------------------
# 2. Executive Narrative
# ---------------------------------------------------------------------------

def generate_geo_narrative(
    title: str,
    url: str,
    description: str,
    overall_score: int,
    breakdown: dict,
    crawl_res: dict,
    schema_res: dict,
    content_res: dict,
    citation_hits: int,
    total_queries: int,
) -> str:
    """
    Generate a 2–3 paragraph plain-English executive summary of the site's GEO situation.

    Written for business owners, not SEO consultants. Explains:
    - The current AI visibility score and what it means
    - The most critical gap
    - One concrete priority action

    Falls back to a rule-based summary if Groq is unavailable.
    """
    # Build rule-based fallback
    grade = "strong" if overall_score >= 70 else "moderate" if overall_score >= 45 else "weak"
    fallback = (
        f"{title} has a GEO score of {overall_score}/100, indicating {grade} AI search visibility. "
        f"The audit checked four areas: crawlability for AI bots, structured schema data, "
        f"content format, and live citation presence. "
        f"The highest-priority fix is the one flagged as HIGH impact in the findings below."
    )

    client = _get_client()
    if not client:
        return fallback

    # Summarise results compactly for the prompt (avoid sending full HTML)
    context = {
        "title": title,
        "url": url,
        "description": description or "Not provided",
        "score": overall_score,
        "breakdown": {
            k: f"{v['score']}/{v['max']}" for k, v in breakdown.items()
        },
        "gptbot_blocked": crawl_res.get("gptbot_blocked", False),
        "perplexity_blocked": crawl_res.get("perplexity_blocked", False),
        "has_llms_txt": crawl_res.get("has_llms_txt", False),
        "org_schema": schema_res.get("has_organization", False),
        "product_schema": schema_res.get("has_product_or_service", False),
        "faq_schema": schema_res.get("has_faq", False),
        "question_headings": content_res.get("question_headings", 0),
        "has_lists_or_tables": content_res.get("has_tables_or_lists", False),
        "citation_hits": citation_hits,
        "queries_tested": total_queries,
    }

    system = (
        "You are a senior GEO (Generative Engine Optimization) consultant. "
        "You write audit reports for business owners — not SEO experts. "
        "Your job: read the audit results and write a 2–3 paragraph executive summary that:\n"
        "  1. Tells the business owner plainly what their AI search visibility score means\n"
        "  2. Names the single most critical gap in concrete terms\n"
        "  3. Ends with one specific priority action they should take this week\n\n"
        "Use plain English. No jargon without inline explanation. Be direct and specific to THIS business — "
        "not generic. Maximum 200 words. Do not use bullet points or headings."
    )

    user = f"Audit results for {title} ({url}):\n\n{json.dumps(context, indent=2)}"

    raw = _chat(client, system, user, max_tokens=350)
    return raw if raw else fallback


# ---------------------------------------------------------------------------
# 3. Per-Finding AI Enrichment
# ---------------------------------------------------------------------------

def enrich_findings_with_ai(findings: list[dict], title: str, description: str) -> list[dict]:
    """
    For each finding, add an 'ai_insight' field: a 1–2 sentence site-specific explanation
    of why this specific issue matters for THIS business.

    Without AI: findings use generic template text.
    With AI: each finding is contextualised to the actual business.

    Falls back to empty ai_insight strings if Groq is unavailable.
    """
    if not findings:
        return findings

    client = _get_client()
    if not client:
        # Attach empty ai_insight so the template doesn't break
        for f in findings:
            f["ai_insight"] = ""
        return findings

    system = (
        "You are a GEO consultant writing concise, business-specific insights. "
        "Given a finding from a GEO audit and basic info about the business, write exactly 1–2 sentences "
        "explaining why THIS specific issue matters for THIS specific business. "
        "Be concrete. Name the business. Do not repeat what the finding already says. "
        "Do not use jargon without explanation. Output only the 1–2 sentences — nothing else."
    )

    enriched = []
    for finding in findings:
        user = (
            f"Business: {title}\n"
            f"Description: {description or 'Not provided'}\n\n"
            f"Finding title: {finding.get('title', '')}\n"
            f"Evidence: {finding.get('evidence', '')}\n"
            f"General description: {finding.get('description', '')}\n\n"
            "Write 1–2 sentences explaining why this issue specifically matters for this business."
        )

        insight = _chat(client, system, user, max_tokens=120)
        finding["ai_insight"] = insight if insight else ""
        enriched.append(finding)

    return enriched
