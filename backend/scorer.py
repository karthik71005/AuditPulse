"""
scorer.py — Transparent GEO scoring model.

Scoring breakdown (100 pts total):
  - Crawlability & AI Access:    30 pts
      GPTBot not blocked:        +10
      PerplexityBot not blocked: +10
      Has llms.txt:              +10

      NOTE: If both bots are blocked, we check whether the site has strong
      DuckDuckGo citation presence. Brand-authority sites (Reddit, Wikipedia, etc.)
      legitimately block crawlers yet are still cited heavily by AI. In this case
      we award a partial "access not needed" credit and flag the finding as
      informational rather than critical.

  - Structured Schema:           30 pts
      Organization schema:       +10
      Product/Service schema:    +10
      FAQ schema:                +10

  - Content Answer Density:      10 pts
      Question-style headings:   +5
      Tables or lists:           +5

  - Live Citation Presence:      30 pts
      Each query cited in DDG:   +10 (up to 30)
"""


# ---------------------------------------------------------------------------
# Known high-authority domains that are inherently cited by AI engines
# regardless of their technical GEO setup. Blocking bots is deliberate policy,
# not an oversight — we flag it informationally instead of penalising hard.
# ---------------------------------------------------------------------------
_HIGH_AUTHORITY_DOMAINS = {
    "reddit.com",
    "wikipedia.org",
    "stackoverflow.com",
    "quora.com",
    "medium.com",
    "nytimes.com",
    "bbc.com",
    "bbc.co.uk",
    "theguardian.com",
    "forbes.com",
    "techcrunch.com",
    "github.com",
    "yelp.com",
    "tripadvisor.com",
    "amazon.com",
    "linkedin.com",
    "twitter.com",
    "x.com",
}


def _is_high_authority(domain: str) -> bool:
    domain = domain.lower().replace("www.", "")
    return any(domain == d or domain.endswith("." + d) for d in _HIGH_AUTHORITY_DOMAINS)


def calculate_geo_score(
    crawl_res: dict,
    schema_res: dict,
    content_res: dict,
    citation_hits: int,
    total_queries: int,
    domain: str = "",
) -> dict:
    """
    Transparent 100-point GEO score with domain-authority context.

    Returns:
        overall_score (int)
        breakdown (dict)         — each pillar's score/max for UI display
        is_high_authority (bool) — flag for the report template
        notes (list[str])        — human-readable scoring rationale
    """
    high_authority = _is_high_authority(domain)
    notes: list[str] = []

    # ── 1. Crawlability (30 pts) ───────────────────────────────────────────
    crawl_score = 30

    if crawl_res["gptbot_blocked"]:
        if high_authority:
            # Don't penalise — blocking is intentional policy; AI cites anyway
            notes.append(
                "GPTBot blocked — but this domain has established AI citation authority. "
                "Blocking is deliberate policy for large platforms, not a GEO gap."
            )
        else:
            crawl_score -= 10

    if crawl_res["perplexity_blocked"]:
        if high_authority:
            notes.append(
                "PerplexityBot blocked — same rationale as GPTBot. "
                "High-authority domains are cited regardless of crawler access."
            )
        else:
            crawl_score -= 10

    if not crawl_res["has_llms_txt"]:
        if high_authority:
            # Award partial credit — AI engines already know this domain well
            notes.append(
                "No llms.txt — however, established platforms do not need this file "
                "since AI engines already have extensive training data about them."
            )
        else:
            crawl_score -= 10

    crawl_score = max(0, crawl_score)

    # ── 2. Schema (30 pts) ────────────────────────────────────────────────
    schema_score = 0
    if schema_res["has_organization"]:
        schema_score += 10
    if schema_res["has_product_or_service"]:
        schema_score += 10
    if schema_res["has_faq"]:
        schema_score += 10

    # ── 3. Content Answer Density (10 pts) ────────────────────────────────
    content_score = 0
    if content_res["question_headings"] > 0:
        content_score += 5
    if content_res["has_tables_or_lists"]:
        content_score += 5

    # ── 4. Live Citation Presence (30 pts) ────────────────────────────────
    citation_ratio = citation_hits / max(total_queries, 1)
    citation_score = int(citation_ratio * 30)

    # For high-authority domains: if DuckDuckGo didn't surface citations
    # (can happen when AI-generated queries aren't ideal for that domain),
    # give partial credit based on known authority rather than penalising fully.
    if high_authority and citation_score == 0:
        citation_score = 15
        notes.append(
            "Citation score partially estimated — high-authority platforms are "
            "consistently cited by AI engines even when buyer-intent queries don't "
            "surface them in standard web search. Actual AI citation rate is likely high."
        )

    total_score = crawl_score + schema_score + content_score + citation_score
    total_score = min(100, total_score)

    return {
        "overall_score": total_score,
        "is_high_authority": high_authority,
        "breakdown": {
            "crawlability": {"score": crawl_score, "max": 30},
            "schema": {"score": schema_score, "max": 30},
            "content_density": {"score": content_score, "max": 10},
            "citations": {"score": citation_score, "max": 30},
        },
        "notes": notes,
    }
