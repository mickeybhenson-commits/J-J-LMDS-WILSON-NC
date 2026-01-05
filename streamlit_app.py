import streamlit as st
import json

# --- Page Config ---
st.set_page_config(page_title="Wayne Brothers | Site Intelligence", layout="wide")

# --- Custom Theme to Match Your Screenshot ---
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 2.5rem !important; }
    [data-testid="stMetricLabel"] { color: #ff4b4b !important; text-transform: uppercase; font-weight: bold; }
    .stAlert { background-color: #111111; border: 1px solid #333333; color: #ffffff; }
    </style>
    """, unsafe_allow_stdio=True)

# --- Sidebar Selector ---
st.sidebar.image("https://www.waynebrothers.com/wp-content/uploads/2021/01/logo.png", width=200)
st.sidebar.title("Site Command")
project_choice = st.sidebar.selectbox("Choose Site:", ["Wilson - J&J LMDS", "Charlotte - South Blvd"])

# --- Routing Data based on Selection ---
data_path = "data/wilson_site.json" if "Wilson" in project_choice else "data/charlotte_site.json"

# Load the file
with open(data_path) as f:
    site = json.load(f)

# --- Header Section (Matched to Screenshot) ---
# We use the 'location' and 'coordinates' from the JSON file
st.write(f"### Wayne Brothers")
st.title(site['project_name'].upper())
st.write(f"📍 {site.get('location', 'N/A')} | {site.get('acreage', 'N/A')} | {site.get('coords', 'N/A')}")
st.markdown(f"<div style='text-align: right; color: #00ff00;'>SYSTEM ACTIVE • UPDATED: {site['last_updated']}</div>", unsafe_allow_stdio=True)

st.divider()

# --- Main Dashboard Layout (Two Columns) ---
col_left, col_right = st.columns([2, 1])

with col_left:
    # 1. Field Operational Directive
    st.caption("FIELD OPERATIONAL DIRECTIVE", help="Current site authorization based on environmental triggers.")
    status = "OPTIMAL" if site['swppp']['rain_24h'] < 0.5 else "ACTION REQUIRED"
    status_color = "#00ff00" if status == "OPTIMAL" else "#ff0000"
    
    st.markdown(f"""
        <div style="border-left: 10px solid {status_color}; padding: 20px; background-color: #111111; border-radius: 5px;">
            <h1 style="color: {status_color}; margin: 0;">{status}</h1>
            <p style="font-size: 1.5rem; color: #ffffff;">{site['swppp']['notes']}</p>
        </div>
    """, unsafe_allow_stdio=True)

    # 2. Executive Advisory
    st.write("")
    st.caption("EXECUTIVE ADVISORY: SAFETY & TACTICAL PRIORITY")
    st.markdown(f"""
        <div style="background-color: #000000; padding: 10px;">
            <p><strong>Weekly Tactical Priority Schedule:</strong></p>
            {site.get('tactical_schedule', '* Data loading...')}
        </div>
    """, unsafe_allow_stdio=True)

with col_right:
    # 3. Analytical Metrics
    st.caption("ANALYTICAL METRICS")
    st.metric("Soil Moisture (API)", site.get('soil_moisture', '0.000'))
    st.metric("Basin SB3 Capacity", site.get('basin_capacity', '0%'))
    st.metric("Sediment Accumulation", site.get('sediment', '0%'))
    st.metric("Temperature", f"{site['concrete']['temp_low']}°F")
    st.metric("Humidity", site.get('humidity', '0%'))

st.sidebar.markdown("---")
st.sidebar.info(f"Currently viewing data for the **{site['project_name']}** project.")
