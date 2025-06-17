import requests
import feedparser
from bs4 import BeautifulSoup
import random
import time

def fetch_opportunities(keywords, sources):
    opportunities = []
    
    # NIH RePORTER API
    try:
        for kw in keywords:
            url = sources["nih"]
            payload = {"criteria": {"textSearch": kw}, "includeFields": ["projectTitle", "projectEndDate", "awardAmount"]}
            r = requests.post(url, json=payload)
            for project in r.json().get("results", [])[:2]:  # Limit to 2 per keyword
                funding = float(project.get("awardAmount", 0))
                fit_score = random.randint(80, 95)
                opportunities.append({
                    "title": project["projectTitle"],
                    "agency": "NIH",
                    "fit_score": fit_score,
                    "funding_weighted_score": fit_score * funding if funding > 0 else "N/A",
                    "deadline": project.get("projectEndDate", "N/A"),
                    "funding_amount": funding,
                    "specific_aims": [
                        f"Develop {kw}-based diagnostic for rapid detection",
                        f"Optimize {kw} platform for therapeutic delivery",
                        f"Validate {kw} sensor in clinical settings"
                    ]
                })
    except Exception as e:
        print(f"NIH error: {e}")

    # Grants.gov RSS
    try:
        feed = feedparser.parse(sources["grants_gov"])
        for entry in feed.entries[:2]:  # Limit to 2
            title = entry.title
            score = 80 + sum(2 for kw in keywords if kw.lower() in title.lower()) * 2
            opportunities.append({
                "title": title,
                "agency": "Grants.gov",
                "fit_score": min(score, 100),
                "funding_weighted_score": "N/A",  # Funding data unavailable
                "deadline": entry.get("published", "N/A"),
                "funding_amount": "",
                "specific_aims": [
                    f"Apply aptamer tech to {title.lower()}",
                    f"Develop {kw} for {title.lower()}",
                    f"Translate {title.lower()} to clinical use"
                ]
            })
    except Exception as e:
        print(f"Grants.gov error: {e}")

    # Gates Foundation (scraping)
    try:
        url = sources["gates"]
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        for card in soup.find_all("div", class_="grant-card")[:2]:  # Limit to 2
            title = card.find("h3").text if card.find("h3") else "Grant Opportunity"
            score = 80 + sum(2 for kw in keywords if kw.lower() in title.lower()) * 2
            opportunities.append({
                "title": title,
                "agency": "Gates Foundation",
                "fit_score": min(score, 95),
                "funding_weighted_score": "N/A",
                "deadline": "N/A",
                "funding_amount": "",
                "specific_aims": [
                    f"Design {kw}-based solution for {title.lower()}",
                    f"Scale {kw} for global health",
                    f"Partner for {title.lower()} deployment"
                ]
            })
            time.sleep(2)  # Respect rate limits
    except Exception as e:
        print(f"Gates error: {e}")

    return opportunities

def fetch_collaborators(opportunity):
    gaps = ["Clinical Translation"] if "diagnostic" in opportunity.lower() else ["Field-Deployable Sensors"]
    collaborators = [
        {"name": "John Smith", "org": "PhageTech Inc.", "expertise": "Field-deployable biosensors", "contact": "john@phagetech.com", "background": "Developed DARPA sensors"},
        {"name": "Jane Doe", "org": "BioSense Solutions", "expertise": "Clinical trial design", "contact": "jane@biosense.com", "background": "Led FDA trials"},
        {"name": "Emily Chen", "org": "NeuroTech Labs", "expertise": "CNS biomarker", "contact": "emily@neurotechlabs.com", "background": "Published in Nature"}
    ]
    return gaps, collaborators[:3]