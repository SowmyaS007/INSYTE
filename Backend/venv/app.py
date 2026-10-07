from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from company_extractor import extract_company
from intelligence_service import build_company_intelligence
from company_profile_service import fetch_company_profile
from company_profile_service import fetch_company_profile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from research_agent_service import run_research_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://insyte-context-ai.lovable.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI(
    title="INSYTE API",
    description="Backend API for generating contextual pre-meeting intelligence.",
    version="0.2.0",
)

@app.get("/company-profile/{company}")
def company_profile(company: str):
    return fetch_company_profile(company)
@app.get("/agents/research/{company}")
def research_agent(company: str):
    return run_research_agent(company)

class Meeting(BaseModel):
    summary: str


@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "INSYTE Backend",
    }


@app.post("/meeting-context")
def meeting_context(meeting: Meeting):
    company = extract_company(meeting.summary)

    if company is None:
        return {
            "meeting": meeting.summary,
            "company": None,
            "message": "No company detected in the meeting title."
        }

    return {
        "meeting": meeting.summary,
        "company": company,
    }


@app.get("/company-intelligence/{company}")
def company_intelligence(company: str):
    try:
        intelligence = build_company_intelligence(company)
        return intelligence

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc