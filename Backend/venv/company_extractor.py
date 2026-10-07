import re

KNOWN_COMPANIES = [
    "Microsoft",
    "Google",
    "Alphabet",
    "Amazon",
    "Apple",
    "Meta",
    "Oracle",
    "Salesforce",
    "IBM",
    "NVIDIA",
    "Intel",
    "Adobe",
    "SAP",
    "ServiceNow",
    "Tesla",
    "Netflix",
]


def extract_company(summary: str):
    """
    Extract a known company name from a meeting title.
    Returns None if no company is detected.
    """

    if not summary:
        return None

    summary = summary.strip()

    # Pattern-based extraction
    patterns = [
        r"Meeting with (.+)",
        r"Call with (.+)",
        r"Discussion with (.+)",
        r"Demo with (.+)",
        r"Intro to (.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, summary, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()

            for company in KNOWN_COMPANIES:
                if company.lower() in candidate.lower():
                    return company

    # Direct company name search
    for company in KNOWN_COMPANIES:
        if company.lower() in summary.lower():
            return company

    return None