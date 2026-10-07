from datetime import datetime, timezone

from ai_service import generate_meeting_brief
from company_profile_service import fetch_company_profile
from financial_service import fetch_company_financials
from news_service import fetch_company_news
from seller_context import SELLER_CONTEXT


def build_company_intelligence(company: str) -> dict:
    """
    Build a unified company intelligence object.
    """

    warnings = []

    news = None
    financials = None
    profile = None
    meeting_brief = None

    # -------- News --------
    try:
        news = fetch_company_news(company)
    except Exception as e:
        warnings.append(f"News unavailable: {str(e)}")

    # -------- Financials --------
    try:
        financials = fetch_company_financials(company)
    except Exception as e:
        warnings.append(f"Financial data unavailable: {str(e)}")

    # -------- Company Profile --------
    try:
        profile = fetch_company_profile(company)
    except Exception as e:
        warnings.append(f"Company profile unavailable: {str(e)}")

    # -------- AI Meeting Brief --------
    try:
        meeting_brief = generate_meeting_brief(
            seller_context=SELLER_CONTEXT,
            buyer_company=company,
            intelligence={
                "news": news,
                "financials": financials,
                "company_profile": profile,
            },
        )
    except Exception as e:
        warnings.append(f"AI Meeting Brief unavailable: {str(e)}")

    return {
        "company": company,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "meeting_brief": meeting_brief,
        "intelligence": {
            "news": news,
            "financials": financials,
            "company_profile": profile,
            "press_releases": [],
            "social_signals": None,
        },
        "warnings": warnings,
    }