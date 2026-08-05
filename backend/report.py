from urllib.parse import urlparse

from backend.scorer import _is_high_authority


def generate_actionable_report(
    url: str,
    title: str,
    crawl_res: dict,
    schema_res: dict,
    content_res: dict,
    queries_tested: list[str],
    citation_hits: int,
) -> list[dict]:
    findings = []
    raw_domain = urlparse(url).netloc
    domain = raw_domain.replace("www.", "")
    high_authority = _is_high_authority(domain)

    # ── Finding 1: Blocked AI Bots ──────────────────────────────────────
    if crawl_res["gptbot_blocked"] or crawl_res["perplexity_blocked"]:
        blocked_bots = []
        if crawl_res["gptbot_blocked"]:
            blocked_bots.append("GPTBot")
        if crawl_res["perplexity_blocked"]:
            blocked_bots.append("PerplexityBot")

        if high_authority:
            # Informational — not a critical issue for brand-authority platforms
            findings.append(
                {
                    "check_id": "crawlability_blocked",
                    "status": "INFO",
                    "title": f"AI Crawlers Blocked ({', '.join(blocked_bots)}) — Intentional Policy",
                    "impact": "LOW",
                    "effort": "LOW",
                    "evidence": (
                        f"robots.txt restricts {', '.join(blocked_bots)}. "
                        f"However, {domain} is a high-authority platform already embedded in AI training data. "
                        "AI engines cite it extensively without needing live crawler access."
                    ),
                    "description": (
                        "For established platforms, blocking AI crawlers is a deliberate content-control decision — "
                        "not a GEO gap. If you ever want to expand AI crawlability, you can selectively open "
                        "read-only paths while keeping user-generated content gated."
                    ),
                    "copy_paste_code": (
                        "# Optional — open only curated paths to AI bots:\n"
                        "User-agent: GPTBot\n"
                        "Allow: /about\n"
                        "Allow: /help\n"
                        "Disallow: /\n\n"
                        "User-agent: PerplexityBot\n"
                        "Allow: /about\n"
                        "Allow: /help\n"
                        "Disallow: /"
                    ),
                }
            )
        else:
            findings.append(
                {
                    "check_id": "crawlability_blocked",
                    "status": "FAIL",
                    "title": f"AI Scrapers Blocked ({', '.join(blocked_bots)})",
                    "impact": "HIGH",
                    "effort": "LOW",
                    "evidence": f"Your robots.txt explicitly restricts access to {', '.join(blocked_bots)}.",
                    "description": (
                        "Unblock AI bots so ChatGPT and Perplexity can crawl and reference your domain. "
                        "If these bots can't read your site, AI engines will cite your competitors instead."
                    ),
                    "copy_paste_code": (
                        "User-agent: GPTBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /"
                    ),
                }
            )

    # ── Finding 2: Missing llms.txt ─────────────────────────────────────
    if not crawl_res["has_llms_txt"]:
        llms_content = f"""# {title}
> Official AI Context File for {raw_domain}

## Overview
{title} provides industry-leading products and services.

## Core Resources
- [{title} Homepage]({url})
- [Pricing]({url}#pricing)
- [Contact]({url}#contact)
"""
        if high_authority:
            findings.append(
                {
                    "check_id": "missing_llms_txt",
                    "status": "INFO",
                    "title": "No /llms.txt — Optional Optimisation for Platforms",
                    "impact": "LOW",
                    "effort": "LOW",
                    "evidence": f"No /llms.txt file found at https://{raw_domain}/llms.txt.",
                    "description": (
                        "For high-authority platforms, llms.txt is an optional enhancement. "
                        "It lets you control exactly what narrative AI engines use when describing you — "
                        "useful if you want to correct or supplement what LLMs say about your platform."
                    ),
                    "copy_paste_code": llms_content,
                }
            )
        else:
            findings.append(
                {
                    "check_id": "missing_llms_txt",
                    "status": "FAIL",
                    "title": "Missing /llms.txt AI Context File",
                    "impact": "HIGH",
                    "effort": "LOW",
                    "evidence": f"HTTP request to https://{raw_domain}/llms.txt returned 404 Not Found.",
                    "description": (
                        "Add an llms.txt standard markdown summary file to your root web folder "
                        "so AI crawlers parse key site information efficiently."
                    ),
                    "copy_paste_code": llms_content,
                }
            )

    # ── Finding 3: Schema Gaps ──────────────────────────────────────────
    if not schema_res["has_organization"]:
        schema_code = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{title}",
  "url": "{url}"
}}
</script>"""
        findings.append(
            {
                "check_id": "missing_org_schema",
                "status": "FAIL",
                "title": "Missing Organization JSON-LD Schema",
                "impact": "MEDIUM" if high_authority else "HIGH",
                "effort": "LOW",
                "evidence": "No <script type='application/ld+json'> with @type 'Organization' was detected.",
                "description": (
                    "Inject this JSON-LD schema into your page head so LLMs can verify your brand identity, "
                    "name, and URL with certainty. Even well-known brands benefit from explicit schema — "
                    "it removes any ambiguity when AI engines attribute information."
                ),
                "copy_paste_code": schema_code,
            }
        )

    # ── Finding 4: Citation Visibility Gap ──────────────────────────────
    # For high-authority sites that scored 0 DDG hits, the scorer already
    # awarded partial credit. Don't add a FAIL finding — just skip it.
    if citation_hits == 0 and not high_authority:
        findings.append(
            {
                "check_id": "citation_gap",
                "status": "WARN",
                "title": "Zero Citation Share in AI-Related Web Search",
                "impact": "HIGH",
                "effort": "MEDIUM",
                "evidence": (
                    f"Domain appeared in 0 out of {len(queries_tested)} buyer-intent queries tested via web search."
                ),
                "description": (
                    "Publish Q&A structured FAQ content and claim brand listings on third-party aggregators "
                    "(G2, Reddit, ProductHunt). AI engines heavily weight sources that appear in web search."
                ),
                "copy_paste_code": (
                    "<!-- Priority Buyer Queries to Target -->\n"
                    + "\n".join([f"<!-- {q} -->" for q in queries_tested])
                ),
            }
        )

    return findings
