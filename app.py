import streamlit as st
import requests
from bs4 import BeautifulSoup
import spacy
from datetime import datetime

# Load spaCy model (using a small English model for NLP)
nlp = spacy.load("en_core_web_sm")

# Simulated user keywords based on your expertise
USER_KEYWORDS = {
    "Aptamers": ["aptamer", "SELEX", "biosensor", "diagnostics", "gene therapy", "VLP", "RNA"],
    "Neuro & Immunology": ["neuroinflammation", "Parkinson's", "Alzheimer's", "MS", "cytokines", "autoimmune"],
    "Opioids & Detection": ["opioids", "fentanyl", "refractive index", "interferometry"]
}

# Function to calculate fit_score using NLP
def calculate_fit_score(text, keywords):
    if not text or not keywords:
        return 0
    doc = nlp(text.lower())
    keyword_set = set(keywords)
    matches = sum(1 for token in doc if token.text in keyword_set)
    return min((matches / len(keywords)) * 100, 100) if keywords else 0

# Foundation scraping function
def scrape_foundations():
    foundations = {
        "Gates Foundation": "https://www.gatesfoundation.org/what-we-do/global-health/grand-challenges",
        "Wellcome Trust": "https://wellcome.org/grants-funding/funding-schemes"
    }
    opportunities = []
    for name, url in foundations.items():
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        # Simplified scraping - adjust selectors based on actual site structure
        grants = soup.find_all("div", class_=["grant-card", "funding-opportunity"])
        for grant in grants[:5]:  # Limit to 5 for demo
            title = grant.find("h3") or grant.find("a")
            title_text = title.text.strip() if title else "Untitled Opportunity"
            desc = grant.find("p")
            desc_text = desc.text.strip() if desc else "No description available"
            fit_score = calculate_fit_score(title_text + " " + desc_text, 
                                          USER_KEYWORDS["Aptamers"] + USER_KEYWORDS["Neuro & Immunology"] + USER_KEYWORDS["Opioids & Detection"])
            opportunities.append({
                "Source": name,
                "Title": title_text,
                "Fit Score": f"{fit_score:.1f}%",
                "Link": url if title and title.get("href") else url,
                "Description": desc_text
            })
    return opportunities

# Simulated Grants.gov data (pending API key)
def get_grantsgov_data():
    return [
        {"Opportunity": "Health Equity Research", "Agency": "HHS", "Deadline": "2025-07-15", "Status": "Open"},
        {"Opportunity": "Substance Abuse Prevention", "Agency": "SAMHSA", "Deadline": "2025-08-01", "Status": "Open"}
    ]

# Simulated NIH RePORTER data (pending API key)
def get_nih_reporter_data():
    return [
        {"Grant": "Aptamer engineering of lentiviral vectors", "Agency": "NIH", "Status": "Active", "Amount": "$500,000"},
        {"Grant": "Bench-top Reader and Aptamer-based Assay", "Agency": "NIH", "Status": "Active", "Amount": "$300,000"}
    ]

# Streamlit app
st.set_page_config(page_title="GreenAnjou Grant Dashboard", layout="wide")
st.title("GreenAnjou Grant Intelligence Dashboard")

tabs = st.tabs(["Foundation", "Grants.gov", "NIH RePORTER"])

with tabs[0]:  # Foundation Tab
    st.header("Foundation Opportunities")
    opportunities = scrape_foundations()
    if opportunities:
        for opp in opportunities:
            st.write(f"**Source:** {opp['Source']}")
            st.write(f"**Title:** {opp['Title']}")
            st.write(f"**Fit Score:** {opp['Fit Score']}")
            st.write(f"**Link:** [{opp['Link']}]")
            st.write(f"**Description:** {opp['Description']}")
            st.write("---")
    else:
        st.write("No foundation opportunities found. Check site accessibility.")

with tabs[1]:  # Grants.gov Tab
    st.header("Grants.gov Opportunities")
    st.write("Note: Simulated data until API key is received. Request in progress.")
    grantsgov_data = get_grantsgov_data()
    for grant in grantsgov_data:
        st.write(f"**Opportunity:** {grant['Opportunity']}")
        st.write(f"**Agency:** {grant['Agency']}")
        st.write(f"**Deadline:** {grant['Deadline']}")
        st.write(f"**Status:** {grant['Status']}")
        st.write("---")

with tabs[2]:  # NIH RePORTER Tab
    st.header("NIH RePORTER Grants")
    st.write("Note: Simulated data until API key is received. Request in progress.")
    nih_data = get_nih_reporter_data()
    total_applications = 5  # Simulated total applications for success rate
    awarded = len([g for g in nih_data if g["Status"] == "Active"])
    success_rate = (awarded / total_applications) * 100
    st.write(f"**Success Rate:** {success_rate:.1f}% ({awarded}/{total_applications} grants)")
    for grant in nih_data:
        st.write(f"**Grant:** {grant['Grant']}")
        st.write(f"**Agency:** {grant['Agency']}")
        st.write(f"**Status:** {grant['Status']}")
        st.write(f"**Amount:** {grant['Amount']}")
        st.write("---")