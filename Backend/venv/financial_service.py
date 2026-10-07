import os

import requests
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"


def _check_api_response(data: dict) -> None:
    """
    Detect common Alpha Vantage API errors.
    """

    if "Error Message" in data:
        raise RuntimeError(data["Error Message"])

    if "Information" in data:
        raise RuntimeError(data["Information"])

    if "Note" in data:
        raise RuntimeError(data["Note"])


# Local mapping of company names to stock symbols
COMPANY_SYMBOLS = {
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "apple": "AAPL",
    "meta": "META",
    "facebook": "META",
    "oracle": "ORCL",
    "salesforce": "CRM",
    "ibm": "IBM",
    "nvidia": "NVDA",
    "intel": "INTC",
    "adobe": "ADBE",
    "sap": "SAP",
    "servicenow": "NOW",
    "zoom": "ZM",
    "netflix": "NFLX",
    "tesla": "TSLA",
}


def fetch_company_financials(company: str) -> dict:
    """
    Fetch a concise financial snapshot for a public company.
    """

    if not ALPHA_VANTAGE_API_KEY:
        raise ValueError(
            "ALPHA_VANTAGE_API_KEY is missing from the .env file."
        )

    symbol = COMPANY_SYMBOLS.get(company.lower())

    if not symbol:
        raise RuntimeError(
            f"No stock symbol mapping found for '{company}'."
        )

    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    try:
        response = requests.get(
            ALPHA_VANTAGE_URL,
            params=params,
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Unable to retrieve financial data: {exc}"
        ) from exc

    data = response.json()

    _check_api_response(data)

    if not data or not data.get("Symbol"):
        raise RuntimeError(
            f"No financial overview returned for '{symbol}'."
        )

    return {
        "symbol": data.get("Symbol"),
        "company_name": data.get("Name"),
        "description": data.get("Description"),
        "exchange": data.get("Exchange"),
        "currency": data.get("Currency"),
        "country": data.get("Country"),
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "market_cap": data.get("MarketCapitalization"),
        "revenue_ttm": data.get("RevenueTTM"),
        "gross_profit_ttm": data.get("GrossProfitTTM"),
        "ebitda": data.get("EBITDA"),
        "profit_margin": data.get("ProfitMargin"),
        "pe_ratio": data.get("PERatio"),
        "eps": data.get("EPS"),
        "dividend_yield": data.get("DividendYield"),
        "52_week_high": data.get("52WeekHigh"),
        "52_week_low": data.get("52WeekLow"),
        "latest_quarter": data.get("LatestQuarter"),
    }