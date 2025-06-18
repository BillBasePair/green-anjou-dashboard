import streamlit as st
from data_fetcher import fetch_opportunities, fetch_collaborators
import pandas as pd

# Initialize session state
if 'grants' not in st.session_state:
    st.session_state.grants = fetch_opportunities().to_dict('records')
if 'collaborators' not in st.session_state:
    st.session_state.collaborators = fetch_collaborators().to_dict('records')

# Sidebar for keywords and refresh
st.sidebar.header("Grant Search")
keywords_input = st.sidebar.text_input("Keywords (comma-separated)", "aptamer,biosensor,fentanyl,opioid,diagnostics,CNS")
keywords = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]
sources = ["NIH", "Grants.gov", "Gates Foundation"]  # Hardcoded for now, adjust if in config

# Function to refresh data
def refresh_data():
    st.session_state.grants = fetch_opportunities(keywords, sources).to_dict('records')
    st.session_state.collaborators = fetch_collaborators().to_dict('records')

# Trigger data refresh on button click
if st.sidebar.button("Refresh Now", key="sidebar_refresh", on_click=refresh_data):
    st.rerun()  # Use rerun instead of experimental_rerun

# Main content
st.title("Green Anjou - Bill’s Grant Opportunity Dashboard")

# Opportunities Tab
st.header("Opportunities")
st.write(f"Current Keywords: {keywords_input}")  # Display current keywords as text
if st.button("Refresh Now", key="main_refresh", on_click=refresh_data):
    st.rerun()  # Use rerun instead of experimental_rerun

# Display opportunities
if st.session_state.grants:
    for grant in st.session_state.grants:
        with st.expander(f"{grant['title']} - {grant['agency']} (Fit Score: {grant['fit_score']}%)"):
            st.write(f"**Funding Weighted Score:** {grant['funding_weighted_score'] if grant['funding_weighted_score'] is not None else 'N/A'}")
            st.write(f"**Deadline:** {grant['deadline'] if grant['deadline'] else 'N/A'}")
            st.write(f"**Specific Aims:** {grant['specific_aims']}")
            grant['responding'] = st.checkbox("Responding", key=f"responding_{grant['title']}")
else:
    st.write("No opportunities found. Please refine keywords or check data sources.")

# Status Tracking Tab
st.header("Status Tracking")
total_submitted = len([g for g in st.session_state.grants if g['status'] in ["Submitted", "Score Received", "Resubmission", "Funded", "Rejected"]])
st.write(f"Total Submitted: {total_submitted}")
for grant in st.session_state.grants:
    with st.expander(f"{grant['title']} - Status: {grant['status']}"):
        status = st.selectbox("Status", ["In Process", "Submitted", "Score Received", "Resubmission", "Funded", "Rejected"], index=["In Process", "Submitted", "Score Received", "Resubmission", "Funded", "Rejected"].index(grant['status']) if grant['status'] in ["In Process", "Submitted", "Score Received", "Resubmission", "Funded", "Rejected"] else 0, key=f"status_{grant['title']}")
        grant['status'] = status
        if status in ["Score Received", "Funded", "Rejected"]:
            score = st.number_input("Score (0-100)", min_value=0, max_value=100, value=0, key=f"score_{grant['title']}")
            amount = st.number_input("Funding Amount ($)", min_value=0, value=0, key=f"amount_{grant['title']}")
            if st.button("Update Scorecard", key=f"update_{grant['title']}"):
                st.write(f"Scorecard: Success Rate: {score}%, Funding: ${amount:,.2f}")

# Collaborators Tab
st.header("Collaborators")
if st.session_state.collaborators:
    for collab in st.session_state.collaborators:
        with st.expander(f"{collab['name']} (Fit Score: {collab['fit_score']}%, Status: {collab['status']}"):
            st.write(f"**Expertise:** {collab['expertise']}")
else:
    st.write("No collaborators available.")

# Needed Collaborators Tab
st.header("Needed Collaborators")
st.write("Suggestions based on current gaps:")
st.write("- Data Scientist (for advanced analytics)")
st.write("- Regulatory Expert (for compliance)")

# TRL Tracker Tab
st.header("TRL Tracker")
st.write("Current TRL: 4 (Placeholder - Update with project-specific TRL)")
st.text_area("TRL Narrative", "Initial prototype development in progress...", key="trl_narrative")