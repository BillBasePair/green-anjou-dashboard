import streamlit as st
from data_fetcher import fetch_opportunities, fetch_collaborators
import pandas as pd
import os

st.title("Green Anjou v1.0 - Bill's Grant Opportunity Dashboard")

if 'grants' not in st.session_state:
    st.session_state.grants = pd.DataFrame()
if 'collaborators' not in st.session_state:
    st.session_state.collaborators = pd.DataFrame()

# Sidebar for input
st.sidebar.header("Search Grants")
keywords = st.sidebar.text_input("Enter keywords (comma-separated)", "aptamer, GPCR, prostate").split(",")
sources = st.sidebar.multiselect("Select data sources", ["Grants.gov", "WebScrape"], default=["Grants.gov", "WebScrape"])
refresh = st.sidebar.button("Refresh Data")

if refresh or st.session_state.grants.empty:
    with st.spinner("Fetching data..."):
        st.session_state.grants = fetch_opportunities([kw.strip() for kw in keywords], sources)
        st.session_state.collaborators = fetch_collaborators()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Opportunities", "Collaborators", "Needed Collaborators", "TRL Tracker"])

with tab1:
    st.header("Grant Opportunities")
    st.write("Debug: Grants data:", st.session_state.grants)
    if not st.session_state.grants.empty:
        for grant in st.session_state.grants.itertuples():
            with st.expander(f"{grant.title} - {grant.agency}"):
                st.write(f"**Funding Weighted Score:** {grant.funding_weighted_score}")
                st.write(f"**Deadline:** {grant.deadline if grant.deadline != 'N/A' else 'N/A'}")
                st.write(f"**Specific Aims:** {grant.specific_aims}")
    else:
        st.write("No grants found.")

with tab2:
    st.header("Collaborators")
    st.write(st.session_state.collaborators)

with tab3:
    st.header("Needed Collaborators")
    st.write("TBD - Add logic to identify needed collaborators based on grants.")

with tab4:
    st.header("TRL Tracker")
    st.write("TBD - Add TRL tracking logic.")