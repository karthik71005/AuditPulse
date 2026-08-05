import json
from bs4 import BeautifulSoup


def check_structured_schema(html_content: str) -> dict:
    soup = BeautifulSoup(html_content, "html.parser")
    json_ld_scripts = soup.find_all("script", type="application/ld+json")

    found_schemas = []
    has_organization = False
    has_product_or_service = False
    has_faq = False

    for script in json_ld_scripts:
        if not script.string:
            continue
        try:
            data = json.loads(script.string)
            items = (
                data.get("@graph", [data]) if isinstance(data, dict) else [data]
            )

            for item in items:
                if not isinstance(item, dict):
                    continue
                schema_type = str(item.get("@type", ""))
                found_schemas.append(schema_type)

                if any(
                    k in schema_type for k in ["Organization", "Corporation", "Brand"]
                ):
                    has_organization = True
                if any(
                    k in schema_type
                    for k in ["Product", "SoftwareApplication", "Service"]
                ):
                    has_product_or_service = True
                if "FAQPage" in schema_type:
                    has_faq = True
        except json.JSONDecodeError:
            continue

    return {
        "total_schemas": len(json_ld_scripts),
        "detected_types": found_schemas,
        "has_organization": has_organization,
        "has_product_or_service": has_product_or_service,
        "has_faq": has_faq,
    }  
