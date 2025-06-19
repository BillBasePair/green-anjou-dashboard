import streamlit as st
import requests
from bs4 import BeautifulSoup
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
    # Original scraping logic here (e.g., foundation, grants.gov, NIH)
    st.write("Scraping and processing data...")
except Exception as e:
    st.error(f"Error loading spaCy or scraping: {e}. Using static data as fallback.")
    foundation_data = [{"Source": "Test", "Title": "Sample Grant", "Fit Score": "50%", "Link": "https://example.com", "Description": "Test description"}]
    st.write("**Foundation Opportunities (Fallback):**")
    for opp in foundation_data:
        st.write(f"**Source:** {opp['Source']}")
        st.write(f"**Title:** {opp['Title']}")
        st.write(f"**Fit Score:** {opp['Fit Score']}")
        st.write(f"**Link:** [{opp['Link']}]")
        st.write(f"**Description:** {opp['Description']}")
        st.write("---")