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
    """, unsafe_allow_html=True) # FIXED: changed stdio to html

# --- Sidebar Selector ---
st.sidebar.image("https://www.waynebrothers.com/wp-content/uploads/2021/01/logo.png", width=200)
st.sidebar.title("Site Command")
project_choice = st.sidebar.selectbox("Choose Site:", ["Wilson - J&J LMDS", "Charlotte - South Blvd"])

# --- Routing Data based on Selection ---
data_path = "data/wilson_site.json" if "Wilson" in project_choice else "data/charlotte_site.json"

# Load the file with a safety check
try:
    with open(data_path) as f:
        site = json.load(f)
except Exception as e:
    st.error(f"Waiting for site data update... ({e})")
    st.stop()

# --- Header Section (Matched to your original Screenshot) ---
st.write(f"### Wayne Brothers")
st.title(site.get('project_name', 'SITE PROJECT').upper())
st.write(f"📍 {site.get('location', 'N/A')} | {site.get('acreage', 'N/A')} | {site.get('coords', 'N/A')}")
st.markdown(f"<div style='text-align: right; color: #00ff00;'>SYSTEM ACTIVE • UPDATED: {site.get('last_updated', 'N/A')}</div>", unsafe_allow_html=True)

st.divider()

# --- Main Dashboard Layout (Two Columns) ---
col_left, col_right = st.columns([2, 1])

with col_left:
    # 1. Field Operational Directive
    st.caption("FIELD OPERATIONAL DIRECTIVE")
    rain_val = site['swppp'].get('rain_24h', 0.0)
    status = "OPTIMAL" if rain_val < 0.5 else "ACTION REQUIRED"
    status_color = "#00ff00" if status == "OPTIMAL" else "#ff0000"
    
    st.markdown(f"""
        <div style="border-left: 10px solid {status_color}; padding: 20px; background-color: #111111; border-radius: 5px;">
            <h1 style="color: {status_color}; margin: 0;">{status}</h1>
            <p style="font-size: 1.5rem; color: #ffffff;">{site['swppp'].get('notes', 'No notes available.')}</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. Executive Advisory
    st.write("")
    st.caption("EXECUTIVE ADVISORY: SAFETY & TACTICAL PRIORITY")
    st.markdown(f"""
        <div style="background-color: #000000; padding: 10px; border: 1px solid #333333;">
            <p><strong>Weekly Tactical Priority Schedule:</strong></p>
            {site.get('tactical_schedule', '• Loading schedule...')}
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # 3. Analytical Metrics
    st.caption("ANALYTICAL METRICS")
    st.metric("Soil Moisture (API)", site.get('soil_moisture', '0.049'))
    st.metric("Basin SB3 Capacity", site.get('basin_capacity', '58.0%'))
    st.metric("Sediment Accumulation", site.get('sediment', '25%'))
    st.metric("Temperature", f"{site['concrete'].get('temp_low', 'N/A')}°F")
    st.metric("Humidity", site.get('humidity', '60%'))

st.sidebar.markdown("---")
st.sidebar.info(f"Viewing: **{site.get('project_name')}**")
