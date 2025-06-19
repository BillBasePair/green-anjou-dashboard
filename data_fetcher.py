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
            # API call (needs authentication fix for 200 status)
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
            # Web scraping with form submission simulation
            scrape_url = "https://www.grants.gov/search-grants"
            payload = {
                'inp-keywords': keyword,
                'btn-search': 'Search'
            }
            response = requests.post(scrape_url, data=payload, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Look for the results table (adjust selector based on post-search HTML)
                table = soup.find('table', class_='usa-table-container--scrollable')
                if table:
                    rows = table.find_all('tr')[1:]  # Skip header row
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 2:  # Minimum columns for title and agency
                            grants.append({
                                'title': cols[0].get_text(strip=True) if cols[0].get_text(strip=True) else 'N/A',
                                'agency': cols[1].get_text(strip=True) if len(cols) > 1 and cols[1].get_text(strip=True) else 'N/A',
                                'deadline': cols[2].get_text(strip=True) if len(cols) > 2 and cols[2].get_text(strip=True) else 'N/A',
                                'specific_aims': 'N/A',  # Adjust if abstract is available
                                'funding_weighted_score': None,
                                'status': 'In Process'
                            })
                else:
                    print(f"No valid data table found for {keyword} after search")
            else:
                print(f"Scrape request failed with status code: {response.status_code}")

    return pd.DataFrame(grants) if grants else pd.DataFrame()

def fetch_collaborators():
    # Placeholder for collaborator data
    return pd.DataFrame([
        {'name': 'John Doe', 'expertise': 'Data Scientist', 'status': 'Available'},
        {'name': 'Jane Smith', 'expertise': 'Regulatory Expert', 'status': 'Available'}
    ])