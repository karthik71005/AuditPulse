import re
from bs4 import BeautifulSoup


def check_content_structure(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")

    headings = soup.find_all(["h1", "h2", "h3"])
    question_headings = 0
    answer_density_pass = False

    for h in headings:
        text = h.get_text().strip()
        if text.endswith("?") or re.search(
            r"^(what|how|why|where|who|is|are|can|does)", text, re.IGNORECASE
        ):
            question_headings += 1

            # Check if next sibling is a concise direct answer paragraph (< 200 chars)
            next_p = h.find_next_sibling("p")
            if next_p and len(next_p.get_text().strip()) < 250:
                answer_density_pass = True

    tables = len(soup.find_all("table"))
    lists = len(soup.find_all(["ul", "ol"]))

    return {
        "total_headings": len(headings),
        "question_headings": question_headings,
        "has_tables_or_lists": (tables > 0 or lists > 0),
        "answer_density_pass": answer_density_pass,
    } 
