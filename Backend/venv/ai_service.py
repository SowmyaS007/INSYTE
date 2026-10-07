import json
import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from the .env file.")

client = genai.Client(api_key=api_key)


class FinancialSnapshot(BaseModel):
    revenue: str = Field(
        description="Revenue formatted for business users, such as $318.27B."
    )

    market_cap: str = Field(
        description=(
            "Market capitalization formatted as millions, "
            "billions, or trillions."
        )
    )

    profit_margin: str = Field(
        description="Profit margin formatted as a percentage."
    )

    eps: str = Field(
        description="Earnings per share formatted as a currency value."
    )


class RecommendedPitch(BaseModel):
    headline: str = Field(
        description="A short sales pitch headline of no more than 10 words."
    )

    value_proposition: str = Field(
        description=(
            "A concise value proposition explaining how INSYTE "
            "could help the buyer."
        )
    )

    supporting_points: list[str] = Field(
        description="Exactly three short supporting sales points."
    )


class NewsInsight(BaseModel):
    headline: str = Field(
        description="A concise version of the news headline."
    )

    source: str = Field(
        description="The publisher or news source."
    )

    date: str = Field(
        description="The publication date in DD MMM YYYY format."
    )

    relevance: str = Field(
        description=(
            "One sentence explaining why the news matters "
            "for the sales meeting."
        )
    )


class MeetingBrief(BaseModel):
    executive_summary: list[str] = Field(
        description="Exactly three concise and actionable buyer insights."
    )

    why_this_meeting_matters: list[str] = Field(
        description="Exactly two reasons why this meeting matters now."
    )

    meeting_priority: Literal["High", "Medium", "Low"] = Field(
        description=(
            "Meeting priority based only on the supplied buyer intelligence."
        )
    )

    account_health: Literal[
        "Strong",
        "Stable",
        "Watch",
        "Unknown",
    ] = Field(
        description=(
            "Overall buyer condition based on available financial "
            "and business signals."
        )
    )

    customer_focus: list[str] = Field(
        description=(
            "Three to five strategic buyer focus areas such as AI, "
            "cloud, security, growth, or efficiency."
        )
    )

    business_drivers: list[str] = Field(
        description=(
            "Three to five business outcomes the buyer may be prioritizing, "
            "based only on the supplied information."
        )
    )

    latest_news: list[NewsInsight] = Field(
        description="The three most relevant recent news items."
    )

    financial_snapshot: FinancialSnapshot

    sales_opportunities: list[str] = Field(
        description=(
            "Exactly four areas where INSYTE could explore alignment "
            "with the buyer. Do not present them as confirmed needs."
        )
    )

    risks: list[str] = Field(
        description=(
            "Exactly three buyer risks or challenges relevant to the meeting."
        )
    )

    competitive_landscape: list[str] = Field(
        description=(
            "Relevant competitors, alternative providers, or market "
            "pressures supported by the supplied information."
        )
    )

    conversation_starters: list[str] = Field(
        description=(
            "Exactly three natural conversation starters that an "
            "INSYTE salesperson can say aloud."
        )
    )

    discovery_questions: list[str] = Field(
        description=(
            "Exactly five thoughtful, open-ended questions that validate "
            "potential needs without assuming them."
        )
    )

    recommended_pitch: RecommendedPitch

    recommended_modules: list[str] = Field(
        description=(
            "Exactly three modules from the supplied INSYTE seller context "
            "that are most relevant to the buyer."
        )
    )

    tailored_value_proposition: str = Field(
        description=(
            "A concise, buyer-specific explanation of how INSYTE could help. "
            "Do not claim that the buyer has confirmed a need."
        )
    )

    likely_objections: list[str] = Field(
        description=(
            "Exactly three realistic objections that the buyer might raise "
            "about adopting INSYTE."
        )
    )

    recommended_next_steps: list[str] = Field(
        description=(
            "Exactly three practical next actions for the INSYTE salesperson."
        )
    )

    meeting_readiness_score: int = Field(
        ge=0,
        le=100,
        description=(
            "How well prepared the salesperson can be using "
            "the supplied intelligence."
        ),
    )

    confidence_score: int = Field(
        ge=0,
        le=100,
        description=(
            "Confidence based on the completeness, relevance, recency, "
            "quality, and consistency of the supplied intelligence."
        ),
    )

    confidence_explanation: str = Field(
        description="A brief explanation of the confidence score."
    )


def generate_meeting_brief(
    seller_context: dict,
    buyer_company: str,
    intelligence: dict,
) -> dict:
    """
    Generate a structured, sales-focused meeting brief for selling INSYTE.
    """

    prompt = f"""
You are INSYTE, an AI-powered Chief of Staff for enterprise sales representatives.

Prepare a concise and actionable pre-meeting brief that helps an INSYTE
sales representative position INSYTE appropriately to the buyer.

SELLER CONTEXT:
{json.dumps(seller_context, indent=2, default=str)}

BUYER COMPANY:
{buyer_company}

BUYER INTELLIGENCE:
{json.dumps(intelligence, indent=2, default=str)}

RULES:

1. Use only the supplied seller and buyer information.
2. Do not invent buyer needs, budgets, existing systems, relationships,
   initiatives, people, products, financial values, or events.
3. Clearly distinguish verified buyer facts from sales inferences.
4. Treat potential needs as hypotheses that must be validated during discovery.
5. Keep all insights concise and suitable for a one-minute scan.
6. Do not repeat the same information across sections.
7. Recommend only modules listed in SELLER CONTEXT.
8. Return exactly three recommended INSYTE modules.
9. Explain their relevance using the available buyer signals.
10. The tailored value proposition must be specific to the buyer.
11. Return exactly three realistic likely objections.
12. Sales opportunities must be areas to explore, not confirmed buyer needs.
13. Conversation starters must sound natural when spoken.
14. Discovery questions must be open-ended and must not assume a problem.
15. If information is unavailable, use "Unavailable" or an empty list.
16. Format financial values clearly:
    - 1,000,000,000 as $1.00B
    - 1,000,000,000,000 as $1.00T
    - profit margin 0.393 as 39.3%
17. Do not recommend products or capabilities that are absent from SELLER CONTEXT.
18. The recommended pitch must position INSYTE, not a generic technology company.

SCORING GUIDANCE:

Meeting readiness score:
- 90–100: Strong profile, financial information, and relevant recent news
- 70–89: Useful information, but one area is limited
- 40–69: Major information gaps
- 0–39: Very little reliable intelligence

Confidence score:
- Base the score on data completeness, recency, source quality, and consistency.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MeetingBrief,
        ),
    )

    # The SDK normally returns a parsed Pydantic object
    # when response_schema is a Pydantic model.
    if response.parsed:
        parsed_brief = response.parsed

        if isinstance(parsed_brief, MeetingBrief):
            return parsed_brief.model_dump()

        return MeetingBrief.model_validate(parsed_brief).model_dump()

    # Fallback in case the SDK returns only JSON text.
    if not response.text:
        raise ValueError("Gemini returned an empty meeting brief.")

    brief = MeetingBrief.model_validate_json(response.text)

    return brief.model_dump()