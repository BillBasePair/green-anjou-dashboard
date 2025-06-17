import pandas as pd
import json
from datetime import datetime

def fetch_opportunities(keywords=None, sources=None):
    # Use default values if None
    keywords = keywords if keywords is not None else []
    sources = sources if sources is not None else []

    # Load configuration as fallback
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        keywords = keywords or config.get('keywords', [])
        sources = sources or config.get('sources', [])
    except FileNotFoundError:
        pass

    # Mock data (no API calls)
    grants_data = []
    mock_data = {
        "NIH": [{"title": "Aptamer-Based Cardiac Therapy", "description": "aptamer diagnostics", "funding": 5000000, "deadline": "2025-12-31", "aims": "Develop aptamer diagnostic tool"}],
        "Grants.gov": [{"title": "Opioid Diagnostic Grant", "description": "opioid diagnostics CNS", "closeDate": "2025-06-30", "objectives": "Improve opioid detection"}],
        "Gates Foundation": [{"title": "Fentanyl Biosensor Grant", "description": "fentanyl biosensor", "goals": "Create fentanyl detection system"}]
    }

    for source in sources:
        if source in mock_data:
            for item in mock_data[source]:
                grants_data.append({
                    "title": item.get("title", f"{source} Grant"),
                    "agency": source,
                    "fit_score": calculate_fit_score(item.get("description", ""), keywords),
                    "funding_weighted_score": item.get("funding", 0) * (calculate_fit_score(item.get("description", ""), keywords) / 100) if item.get("funding") else None,
                    "deadline": item.get("deadline", item.get("closeDate", datetime.now().strftime("%Y-%m-%d"))),
                    "specific_aims": item.get("aims", item.get("objectives", item.get("goals", "No specific aims provided"))),
                    "responding": False,
                    "status": "In Process"
                })

    df = pd.DataFrame(grants_data) if grants_data else pd.DataFrame(columns=["title", "agency", "fit_score", "funding_weighted_score", "deadline", "specific_aims", "responding", "status"])
    with open('grants.json', 'w') as f:
        json.dump(grants_data, f)
    return df

def fetch_collaborators():
    # Mock collaborator data
    collaborators_data = [
        {"name": "Yonatan Lipsitz", "expertise": "Aptamer Design", "fit_score": 95, "status": "Current"},
        {"name": "John Smith", "expertise": "Data Analysis", "fit_score": 85, "status": "Potential"}
    ]
    df = pd.DataFrame(collaborators_data)
    with open('collaborators.json', 'w') as f:
        json.dump(collaborators_data, f)
    return df

def calculate_fit_score(description, keywords):
    if not description or not keywords:
        return 0
    score = sum(1 for keyword in keywords if keyword.lower() in description.lower()) * (100 / len(keywords)) if keywords else 0
    return min(100, max(0, score))

if __name__ == "__main__":
    df_opp = fetch_opportunities()
    df_collab = fetch_collaborators()
    print("Opportunities:\n", df_opp)
    print("Collaborators:\n", df_collab)