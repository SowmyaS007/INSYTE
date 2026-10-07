from datetime import datetime, timezone

from company_profile_service import fetch_company_profile
from financial_service import fetch_company_financials
from news_service import fetch_company_news
from seller_context import SELLER_CONTEXT


def run_research_agent(company: str) -> dict:
    """
    Collect external buyer intelligence for the multi-agent workflow.
    """

    warnings = []

    news = None
    financials = None
    company_profile = None

    try:
        news = fetch_company_news(company)
    except Exception as exc:
        warnings.append(f"News unavailable: {str(exc)}")

    try:
        financials = fetch_company_financials(company)
    except Exception as exc:
        warnings.append(f"Financial data unavailable: {str(exc)}")

    try:
        company_profile = fetch_company_profile(company)
    except Exception as exc:
        warnings.append(f"Company profile unavailable: {str(exc)}")

    return {
        "agent": "research_agent",
        "company": company,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seller_context": SELLER_CONTEXT,
        "research": {
            "news": news,
            "financials": financials,
            "company_profile": company_profile,
        },
        "warnings": warnings,
    }