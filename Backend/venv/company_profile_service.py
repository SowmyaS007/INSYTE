import os

import requests
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

FINNHUB_URL = "https://finnhub.io/api/v1/stock/profile2"


# Same company-symbol mapping used elsewhere
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


def fetch_company_profile(company: str) -> dict:
    """
    Fetch company profile from Finnhub.
    """

    if not FINNHUB_API_KEY:
        raise ValueError("FINNHUB_API_KEY is missing from .env")

    symbol = COMPANY_SYMBOLS.get(company.lower())

    if symbol is None:
        raise ValueError(f"No stock symbol mapping found for '{company}'")

    params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY,
    }

    response = requests.get(
        FINNHUB_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise RuntimeError("No company profile returned from Finnhub.")

    return {
        "symbol": data.get("ticker"),
        "company_name": data.get("name"),
        "country": data.get("country"),
        "currency": data.get("currency"),
        "exchange": data.get("exchange"),
        "industry": data.get("finnhubIndustry"),
        "ipo_date": data.get("ipo"),
        "market_cap_million_usd": data.get("marketCapitalization"),
        "website": data.get("weburl"),
        "logo": data.get("logo"),
    }