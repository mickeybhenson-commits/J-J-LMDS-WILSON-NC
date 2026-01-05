import streamlit as st
import json
from datetime import datetime

# 1. SIDEBAR SETUP: The "Project Switcher"
st.sidebar.image("https://www.waynebrothers.com/wp-content/uploads/2021/01/logo.png", width=200) # Professional Branding
st.sidebar.title("Project Selection")
project_choice = st.sidebar.selectbox(
    "Choose Site:", 
    ["Wilson - J&J LMDS", "Charlotte - South Blvd"]
)

# 2. LOGIC: Pick the correct data file based on user choice
if project_choice == "Wilson - J&J LMDS":
    data_path = "data/wilson_site.json"
else:
    data_path = "data/charlotte_site.json"

# 3. LOAD DATA
try:
    with open(data_path) as f:
        site_data = json.load(f)
except FileNotFoundError:
    st.error(f"Error: {data_path} not found. Run updater.py first.")
    st.stop()

# 4. HEADER: Changes automatically based on the site data
st.title(f"🚧 {site_data['project_name']}")
st.markdown(f"**Location:** {site_data['location']} | **System Status:** ✅ Active")
st.markdown(f"**Last Data Sync:** {site_data['last_updated']}")

st.divider()

# 5. METRICS: Rainfall and Safety
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rainfall (24h)", f"{site_data['swppp']['rain_24h']}\"")
    if site_data['swppp']['rain_24h'] >= 0.5:
        st.error("ACTION: SWPPP Inspection Required")
    else:
        st.success("Compliant: No Action Needed")

with col2:
    st.metric("Temperature (Low)", f"{site_data['concrete']['temp_low']}°F")
    if site_data['concrete']['blankets_required']:
        st.warning("Blankets Required Tonight")
    else:
        st.info("No Freeze Protection Needed")

with col3:
    st.metric("Wind Speed", f"{site_data['crane']['wind_speed']} mph")
    st.success(f"Crane Status: {site_data['crane']['status']}")

# 6. FIELD NOTES: Specific details for the CM
st.subheader("Field Operational Directives")
st.info(site_data['swppp']['notes'])
st.write(f"**Concrete Phase Notes:** {site_data['concrete']['notes']}")

# 7. SIDEBAR FOOTER
st.sidebar.markdown("---")
st.sidebar.caption("Data feeds provided by USGS & NOAA.")
st.sidebar.caption("Updates every 30m or on-demand via 'Storm Button'.")
