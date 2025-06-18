import pandas as pd
import json
import requests
import os
from datetime import datetime

def fetch_opportunities(keywords=None, sources=None):
    keywords = keywords or []
    sources = sources or []
    grants_data = []

    for source in sources:
        if source == "NIH":
            url = "https://api.reporter.nih.gov/v2/projects/search"
            payload = {
                "criteria": {
                    "search_terms": " ".join(keywords),
                    "fiscal_years": ["2023", "2024", "2025"],
                    "activity_codes": ["R41", "R42", "R43", "R44", "R01", "R21", "U01"]
                },
                "limit": 50
            }
            api_key = os.getenv("API_KEY", "e61dd522d8109420aeef9afaf905b245b308")
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "GreenAnjouDashboard/1.0 (bill.jackson@basepairbio.com)",
                "api_key": api_key
            }
            try:
                print(f"Attempting POST to {url} with keywords: {keywords}")
                print(f"Payload: {payload}")
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                print(f"Response status code: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"Received data: {data}")
                    for item in data.get("items", []):
                        abstract = item.get("abstract_text", "").lower()
                        fit_score = sum(1 for keyword in keywords if keyword.lower() in abstract) * (100 / len(keywords)) if keywords else 0
                        if fit_score > 0:
                            grants_data.append({
                                "title": item.get("project_title", "NIH Opportunity"),
                                "agency": "NIH",
                                "fit_score": min(100, max(0, fit_score)),
                                "funding_weighted_score": item.get("total_cost", 0) * (fit_score / 100),
                                "deadline": item.get("project_end_date", ""),
                                "specific_aims": item.get("abstract_text", "No specific aims"),
                                "responding": False,
                                "status": "In Process"
                            })
                else:
                    print(f"NIH API request failed with status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to NIH API: {e}")
        elif source == "Grants.gov":
            pass
        elif source == "Gates Foundation":
            pass

    # Add mock data if no results and "melanoma" is a keyword, for deployed fallback
    if not grants_data and "melanoma" in [kw.lower() for kw in keywords]:
        print("Adding mock data due to no results")
        grants_data.append({
            "title": "Mock NIH Opportunity - Melanoma",
            "agency": "NIH",
            "fit_score": 50,
            "funding_weighted_score": 1000000,
            "deadline": "2025-12-31",
            "specific_aims": "Mock research aims including melanoma",
            "responding": False,
            "status": "In Process"
        })

    df = pd.DataFrame(grants_data) if grants_data else pd.DataFrame(columns=["title", "agency", "fit_score", "funding_weighted_score", "deadline", "specific_aims", "responding", "status"])
    with open('grants.json', 'w') as f:
        json.dump(grants_data, f)
    return df

def fetch_collaborators():
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