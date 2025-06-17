import streamlit as st
import pandas as pd
import json
from data_fetcher import fetch_opportunities, fetch_collaborators
from datetime import datetime

st.set_page_config(page_title="Green Anjou v1.0 - Bill's Grant Opportunity Dashboard", layout="wide")
st.title("Green Anjou v1.0 - Bill's Grant Opportunity Dashboard")

# Load config
with open('config.json') as f:
    config = json.load(f)

# Load or initialize grants.json
if 'grants' not in st.session_state:
    try:
        with open('grants.json', 'r') as f:
            st.session_state.grants = json.load(f)
    except FileNotFoundError:
        st.session_state.grants = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Opportunities", "Collaborators", "Needed Collaborators", "TRL Tracker", "Status Tracking"])

with tab1:
    st.header("Opportunities")
    keywords = st.text_input("Keywords (comma-separated)", config['keywords'])
    if st.button("Refresh Now"):
        with st.spinner("Fetching new grants..."):
            opportunities = fetch_opportunities(keywords.split(','), config['sources'])
            st.session_state.opportunities = opportunities
    if 'opportunities' in st.session_state:
        df = pd.DataFrame(st.session_state.opportunities)
        df['Responding'] = False
        edited_df = st.data_editor(
            df[['title', 'agency', 'fit_score', 'funding_weighted_score', 'deadline', 'specific_aims', 'Responding']],
            use_container_width=True,
            column_config={
                "Responding": st.column_config.CheckboxColumn(default=False),
                "specific_aims": st.column_config.ListColumn()
            }
        )
        for index, row in edited_df.iterrows():
            if row['Responding'] and not any(g['title'] == row['title'] for g in st.session_state.grants):
                st.session_state.grants.append({
                    "title": row['title'],
                    "agency": row['agency'],
                    "status": "In Process",
                    "submission_date": "",
                    "score": "",
                    "resubmission": "No",
                    "funded": False,
                    "amount": row.get('funding_amount', ""),
                    "rejected": False
                })
        with open('grants.json', 'w') as f:
            json.dump(st.session_state.grants, f, indent=2)
    else:
        st.write("Click 'Refresh Now' to fetch opportunities.")

with tab2:
    st.header("Collaborators")
    st.subheader("Current Collaborators")
    current_collaborators = [
        {"name": "Yonatan Lipsitz", "org": "Lilium Therapeutics", "role": "VLP Engineering", "expertise": "VLP synthesis, CNS delivery", "score": 95},
        {"name": "Brent Dixon", "org": "BioCytics", "role": "Animal Studies", "expertise": "In vivo testing", "score": 90},
        {"name": "Burt Sharp", "org": "University of Tennessee", "role": "PDE4B Targeting", "expertise": "Addiction treatment", "score": 85}
    ]
    st.dataframe(pd.DataFrame(current_collaborators), use_container_width=True)
    st.subheader("Potential Collaborators")
    potential_collaborators = [
        {"name": "John Smith", "org": "PhageTech Inc.", "expertise": "Field-deployable biosensors", "contact": "john@phagetech.com"},
        {"name": "Jane Doe", "org": "BioSense Solutions", "expertise": "Clinical trial design", "contact": "jane@biosense.com"},
        {"name": "Emily Chen", "org": "NeuroTech Labs", "expertise": "CNS biomarker", "contact": "emily@neurotechlabs.com"}
    ]
    st.dataframe(pd.DataFrame(potential_collaborators), use_container_width=True)

with tab3:
    st.header("Needed Collaborators")
    opportunity = st.selectbox("Select Opportunity", [op['title'] for op in st.session_state.get('opportunities', [])] if 'opportunities' in st.session_state else ["None"])
    if st.button("Activate"):
        with st.spinner("Finding collaborators..."):
            gaps, suggested = fetch_collaborators(opportunity)
            st.session_state.gaps = gaps
            st.session_state.suggested = suggested
    if 'gaps' in st.session_state:
        st.write(f"Team Gaps: {', '.join(st.session_state.gaps)}")
        st.dataframe(pd.DataFrame(st.session_state.suggested), use_container_width=True)

with tab4:
    st.header("TRL Tracker")
    st.write("Current TRL: 4 (Lab-validated aptamer platform, placeholder)")
    target_trl = st.selectbox("Target TRL", ["", "4", "5", "6"])
    if target_trl:
        st.write(f"Our platform, currently at TRL 4, will advance to TRL {target_trl} through {'in vivo validation' if target_trl == '5' else 'prototype testing'}.")

with tab5:
    st.header("Status Tracking")
    if st.session_state.grants:
        st.subheader("Tracked Grants")
        grants_df = pd.DataFrame(st.session_state.grants)
        edited_grants = st.data_editor(
            grants_df,
            use_container_width=True,
            column_config={
                "status": st.column_config.SelectboxColumn(options=["In Process", "Submitted", "Score Received", "Resubmission", "Rejected", "Funded"]),
                "resubmission": st.column_config.SelectboxColumn(options=["Yes", "No"]),
                "funded": st.column_config.CheckboxColumn(default=False),
                "rejected": st.column_config.CheckboxColumn(default=False)
            }
        )
        st.session_state.grants = edited_grants.to_dict('records')
        with open('grants.json', 'w') as f:
            json.dump(st.session_state.grants, f, indent=2)
        st.subheader("Performance Scorecard")
        total_submitted = len([g for g in st.session_state.grants if g['status'] in ["Submitted", "Score Received", "Resubmission", "Funded", "Rejected"]])
        funded = len([g for g in st.session_state.grants if g['funded']])
        success_rate = (funded / total_submitted * 100) if total_submitted > 0 else 0
        scores = [float(g['score']) for g in st.session_state.grants if g['score'] and g['status'] == "Score Received"]
        avg_score = sum(scores) / len(scores) if scores else "N/A"
        resubmitted = len([g for g in st.session_state.grants if g['resubmission'] == "Yes"])
        resubmission_rate = (resubmitted / total_submitted * 100) if total_submitted > 0 else 0
        total_funding = sum(float(g['amount']) for g in st.session_state.grants if g['amount'] and g['funded'])
        st.metric("Success Rate", f"{success_rate:.1f}% ({funded}/{total_submitted})")
        st.metric("Average Score", avg_score)
        st.metric("Resubmission Rate", f"{resubmission_rate:.1f}%")
        st.metric("Total Funding", f"${total_funding:,.2f}")
        status_counts = grants_df['status'].value_counts().to_dict()
        st.write("Status Breakdown:")
        st.dataframe(pd.DataFrame([{"Status": k, "Count": v} for k, v in sorted(status_counts.items())]), use_container_width=True)
    else:
        st.write("No grants tracked yet. Check 'Responding' in Opportunities tab.")