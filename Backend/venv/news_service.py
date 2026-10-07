import os
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Initial trusted-source list for the MVP.
TRUSTED_DOMAINS = [
    "reuters.com",
    "bbc.com",
    "cnbc.com",
    "techcrunch.com",
    "theverge.com",
]

def fetch_company_news(company: str, limit: int = 5) -> list[dict]:
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is missing from the .env file.")

    if not company or not company.strip():
        return []

    from_date = (
        datetime.now(timezone.utc) - timedelta(days=30)
    ).date().isoformat()

    params = {
        "q": f'"{company.strip()}"',
        "searchIn": "title,description",
        "language": "en",
        "sortBy": "publishedAt",
        "from": from_date,
        "pageSize": limit,
        "domains": ",".join(TRUSTED_DOMAINS),
    }

    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    try:
        response = requests.get(
            NEWS_API_URL,
            params=params,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Unable to retrieve company news: {exc}") from exc

    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError(
            data.get("message", "NewsAPI returned an unknown error.")
        )

    articles = []

    for article in data.get("articles", []):
        articles.append(
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "source": article.get("source", {}).get("name"),
                "published_at": article.get("publishedAt"),
                "url": article.get("url"),
            }
        )

    return articles