import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

def fetch_opportunities(keywords, sources):
    grants = []
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'GreenAnjouDashboard/1.0 (bill.jackson@basepairbio.com)'
    }

    for keyword in keywords:
        if "Grants.gov" in sources:
            # API call (currently returning 0 items, needs auth fix)
            api_url = "https://api.grants.gov/v1/api/search2"
            payload = {
                'query': {
                    'search_text': keyword,
                    'posted_date_from': '2023-01-01',
                    'posted_date_to': datetime.now().strftime('%Y-%m-%d'),
                    'sort_by': 'posted_date',
                    'sort_order': 'desc',
                    'rows': 50
                }
            }
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('response', {}).get('docs'):
                    for item in data['response']['docs']:
                        grants.append({
                            'title': item.get('title', 'N/A'),
                            'agency': item.get('agency', 'N/A'),
                            'deadline': item.get('deadline_date', 'N/A'),
                            'specific_aims': item.get('abstract', 'N/A'),
                            'funding_weighted_score': None,
                            'status': 'In Process'
                        })
            else:
                print(f"Grants.gov API request failed with status code: {response.status_code}")

        if "WebScrape" in sources:
            # Web scraping attempt
            scrape_url = f"https://www.grants.gov/search-grants?keywords={keyword}"
            response = requests.get(scrape_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Adjust this selector based on actual HTML structure
                table = soup.find('table', class_='usa-table usa-table--striped')
                if table:
                    rows = table.find_all('tr')
                    for row in rows[1:]:  # Skip header row
                        cols = row.find_all('td')
                        if len(cols) >= 3:  # Ensure enough columns
                            grants.append({
                                'title': cols[0].get_text(strip=True) if cols[0].get_text(strip=True) else 'N/A',
                                'agency': cols[1].get_text(strip=True) if cols[1].get_text(strip=True) else 'N/A',
                                'deadline': cols[2].get_text(strip=True) if cols[2].get_text(strip=True) else 'N/A',
                                'specific_aims': 'N/A',  # Adjust if abstract is available
                                'funding_weighted_score': None,
                                'status': 'In Process'
                            })
                else:
                    print(f"No table with class 'usa-table usa-table--striped' found for {keyword}")
                    # Fallback to mock data if no real data
                    grants.append({
                        'title': f"Mock Grant for {keyword}",
                        'agency': 'N/A',
                        'deadline': 'N/A',
                        'specific_aims': 'N/A',
                        'funding_weighted_score': None,
                        'status': 'In Process'
                    })
            else:
                print(f"Scrape request failed with status code: {response.status_code}")

    return pd.DataFrame(grants) if grants else pd.DataFrame()

def fetch_collaborators():
    # Placeholder for collaborator data
    return pd.DataFrame([
        {'name': 'John Doe', 'expertise': 'Data Scientist', 'status': 'Available'},
        {'name': 'Jane Smith', 'expertise': 'Regulatory Expert', 'status': 'Available'}
    ])

# Remove incomplete calculate_fit function