import streamlit as st

# Simulated data for all tabs
foundation_data = [{"Source": "Test", "Title": "Sample Grant", "Fit Score": "50%", "Link": "https://example.com", "Description": "Test description"}]
grantsgov_data = [{"Opportunity": "Health Equity Research", "Agency": "HHS", "Deadline": "2025-07-15", "Status": "Open"}]
nih_data = [{"Grant": "Aptamer engineering of lentiviral vectors", "Agency": "NIH", "Status": "Active", "Amount": "$500,000"}]

# Streamlit app
st.set_page_config(page_title="GreenAnjou Grant Dashboard", layout="wide")
st.title("GreenAnjou Grant Intelligence Dashboard")

tabs = st.tabs(["Foundation", "Grants.gov", "NIH RePORTER"])

with tabs[0]:  # Foundation Tab
    st.header("Foundation Opportunities")
    for opp in foundation_data:
        st.write(f"**Source:** {opp['Source']}")
        st.write(f"**Title:** {opp['Title']}")
        st.write(f"**Fit Score:** {opp['Fit Score']}")
        st.write(f"**Link:** [{opp['Link']}]")
        st.write(f"**Description:** {opp['Description']}")
        st.write("---")

with tabs[1]:  # Grants.gov Tab
    st.header("Grants.gov Opportunities")
    st.write("Note: Simulated data until API key is received.")
    for grant in grantsgov_data:
        st.write(f"**Opportunity:** {grant['Opportunity']}")
        st.write(f"**Agency:** {grant['Agency']}")
        st.write(f"**Deadline:** {grant['Deadline']}")
        st.write(f"**Status:** {grant['Status']}")
        st.write("---")

with tabs[2]:  # NIH RePORTER Tab
    st.header("NIH RePORTER Grants")
    st.write("Note: Simulated data until API key is received.")
    total_applications = 5
    awarded = len(nih_data)
    success_rate = (awarded / total_applications) * 100
    st.write(f"**Success Rate:** {success_rate:.1f}% ({awarded}/{total_applications} grants)")
    for grant in nih_data:
        st.write(f"**Grant:** {grant['Grant']}")
        st.write(f"**Agency:** {grant['Agency']}")
        st.write(f"**Status:** {grant['Status']}")
        st.write(f"**Amount:** {grant['Amount']}")
        st.write("---")