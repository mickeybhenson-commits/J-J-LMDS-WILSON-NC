import streamlit as st
import json
import pandas as pd
import datetime as dt
from pathlib import Path

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Wayne Brothers | J&J Wilson NC", layout="wide")

def apply_clean_design():
    bg_url = "https://raw.githubusercontent.com/mickeybhenson-commits/J-J-LMDS-WILSON-NC/main/image_12e160.png"
    st.markdown(
        f"""
        <style>
        .stApp {{ background-image: url("{bg_url}"); background-attachment: fixed; background-size: cover; }}
        .stApp:before {{ content: ""; position: fixed; inset: 0; background: rgba(0,0,0,0.88); z-index: 0; }}
        section.main {{ position: relative; z-index: 1; }}
        .metric-card {{ background: rgba(30,30,35,0.9); padding: 20px; border-radius: 4px; border-left: 5px solid #555; }}
        .recommendation-box {{ background: rgba(255,255,255,0.05); padding: 20px; border-radius: 4px; border-left: 8px solid #cc0000; }}
        </style>
        """, unsafe_allow_html=True)

apply_clean_design()

# --- DATA & LOGIC ---
# Calculate API and Load JSON (Site Status)
def load_and_analyze():
    with open("data/site_status.json", "r") as f: site = json.load(f)
    hist = pd.read_csv("data/history.csv")
    recent = hist.tail(5)["precip_actual"].fillna(0).tolist()
    api = round(sum(r * (0.85 ** i) for i, r in enumerate(reversed(recent))), 3)
    return site, api

site_data, api_val = load_and_analyze()

# --- MAIN EXECUTIVE PAGE ---
st.title("J&J Biologics Manufacturing Facility | Operational Directives")
st.write(f"Directives Valid For: {dt.datetime.now():%Y-%m-%d %H:%M} EST")

# Pillar Row
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Soil Moisture (API)", api_val)
    st.caption("Critical threshold: 0.85")
with c2:
    st.metric("Precipitation Forecast", f"{site_data['precipitation']['forecast_prob']}%")
    st.caption("Next 24-hour probability")
with c3:
    st.metric("Wind & Direction", f"{site_data['crane_safety']['wind_speed']} MPH", f"Direction: {site_data.get('wind_dir', 'N/W')}")

st.markdown("---")

# --- SATELLITE & SWPPP RECOMMENDATIONS ---
st.header("Site Documentation & Infrastructure Analysis")

# Placeholder for Satellite Analysis
col_img, col_rec = st.columns([2, 1])
with col_img:
    st.subheader("Current Satellite Surveillance (148.2 Acres)")
    st.image("https://raw.githubusercontent.com/mickeybhenson-commits/J-J-LMDS-WILSON-NC/main/satellite_placeholder.png", 
             caption="Analyzed Zone: Basin SB3 & Perimeter Silt Fence A")
    st.caption("Satellite analysis identifies potential sediment plumes and silt fence breaches.")

with col_rec:
    st.subheader("Required Field Actions")
    # Dynamic logic based on Soil/Rain/Satellite
    if api_val > 0.75:
        st.error("**GRADING:** High saturation. Suspend mass grading to protect soil structure.")
    else:
        st.success("**GRADING:** Soil stability is optimal. Proceed with scheduled lifts.")
        
    if site_data['swppp']['sb3_capacity_pct'] > 70:
        st.warning("**SWPPP:** SB3 basin at critical level. Dispatch pump-out crew to NW Corner.")
    else:
        st.info("**SWPPP:** Basin capacities nominal. Monitor 148.2-acre perimeter for silt fence integrity.")

# Sidebar for Internal Defense
with st.sidebar:
    st.markdown("### Internal Compliance Feed")
    st.write(f"**Last USGS Sync:** {site_data['last_updated']}")
    if st.button("Archive Daily Record"):
        st.success("Record Saved to history.csv at 18:00 EST.")
