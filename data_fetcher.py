import pandas as pd
import json
import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_opportunities(keywords=None, sources=None):
    keywords = keywords or []
    sources = sources or []
    grants_data = []

    print(f"Starting fetch_opportunities with keywords: {keywords}, sources: {sources}")
    for source in sources:
        if source == "Grants.gov":
            url = "https://api.grants.gov/v1/api/search2"  # Correct endpoint
            payload = {
                "query": {
                    "search_text": " ".join(keywords),
                    "posted_date_from": "2023-01-01",
                    "posted_date_to": "2025-06-18",
                    "sort_by": "posted_date",
                    "sort_order": "desc",
                    "rows": 50
                }
            }
            api_key = os.getenv("GRANTS_API_KEY", "")  # Add API key via environment variable
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "GreenAnjouDashboard/1.0 (bill.jackson@basepairbio.com)"
            }
            if api_key:
                headers["X-API-Key"] = api_key
            try:
                print(f"Attempting POST to {url} with keywords: {keywords}")
                print(f"Payload: {payload}")
                print(f"Headers: {headers}")
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                print(f"Response status code: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    item_count = len(data.get("results", []))
                    print(f"Received data: {item_count} items found")
                    if item_count > 0:
                        print(f"Sample item: {json.dumps(data['results'][0], indent=2)}")
                    for item in data.get("results", []):
                        grants_data.append({
                            "title": item.get("title", "Grants.gov Opportunity"),
                            "agency": item.get("agency", "Unknown"),
                            "fit_score": 0,
                            "funding_weighted_score": 0,
                            "deadline": item.get("close_date", ""),
                            "specific_aims": item.get("description", "No description available"),
                            "responding": False,
                            "status": "In Process"
                        })
                else:
                    print(f"Grants.gov API request failed with status code: {response.status_code}, Response: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to Grants.gov API: {e}")
        elif source == "WebScrape":
            url = "https://www.grants.gov/search-results"
            params = {"keywords": " ".join(keywords)}
            headers = {
                "User-Agent": "GreenAnjouDashboard/1.0 (bill.jackson@basepairbio.com)"
            }
            try:
                print(f"Attempting GET to {url} with keywords: {keywords}")
                response = requests.get(url, params=params, headers=headers, timeout=60)
                print(f"Response status code: {response.status_code}")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    # Verify these classes by inspecting https://www.grants.gov/search-results
                    opportunities = soup.find_all("div", class_="search-result")  # Placeholder
                    print(f"Scraped {len(opportunities)} items")
                    for item in opportunities:
                        title_elem = item.find("h2", class_="search-result-title")  # Placeholder
                        agency_elem = item.find("span", class_="agency-name")  # Placeholder
                        deadline_elem = item.find("span", class_="close-date")  # Placeholder
                        title = title_elem.text.strip() if title_elem else "Unnamed Opportunity"
                        agency = agency_elem.text.strip() if agency_elem else "Unknown"
                        deadline = deadline_elem.text.strip() if deadline_elem else ""
                        grants_data.append({
                            "title": title,
                            "agency": agency,
                            "fit_score": 0,
                            "funding_weighted_score": 0,
                            "deadline": deadline,
                            "specific_aims": "Scraped description placeholder",
                            "responding": False,
                            "status": "In Process"
                        })
                else:
                    print(f"Web scrape request failed with status code: {response.status_code}, Response: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to Grants.gov for scraping: {e}")
        elif source == "NIH":
            pass

    # Force mock data if no results
    if not grants_data:
        print("!!! FORCED MOCK DATA ADDED !!!")
        grants_data.append({
            "title": "Mock NIH Opportunity - Test",
            "agency": "NIH",
            "fit_score": 50,
            "funding_weighted_score": 1000000,
            "deadline": "2025-12-31",
            "specific_aims": "Mock research aims for testing",
            "responding": False,
            "status": "In Process"
        })

    print(f"Fetch completed with {len(grants_data)} items")
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