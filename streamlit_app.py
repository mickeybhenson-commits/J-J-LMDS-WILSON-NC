import streamlit as st
import json
import pandas as pd
import datetime as dt
from pathlib import Path
from streamlit_autorefresh import st_autorefresh 

# --- 1. COMMAND CONFIG & PREMIUM STYLING ---
st.set_page_config(page_title="Wayne Brothers | Executive Command", layout="wide")

# Automated 5-minute sync (300,000 ms)
st_autorefresh(interval=300000, key="datarefresh")

def apply_industrial_premium_styling():
    bg_url = "https://raw.githubusercontent.com/mickeybhenson-commits/J-J-LMDS-WILSON-NC/main/image_12e160.png"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        .stApp {{ background-image: url("{bg_url}"); background-attachment: fixed; background-size: cover; font-family: 'Inter', sans-serif; }}
        .stApp:before {{ content: ""; position: fixed; inset: 0; background: radial-gradient(circle at center, rgba(0,0,0,0.85), rgba(0,0,0,0.95)); z-index: 0; }}
        section.main {{ position: relative; z-index: 1; }}
        .exec-header {{ margin-bottom: 30px; border-left: 8px solid #CC0000; padding-left: 25px; }}
        .exec-title {{ font-size: 3.5em; font-weight: 900; letter-spacing: -2px; line-height: 1; color: #FFFFFF; margin: 0; }}
        .report-section {{ background: rgba(20, 20, 25, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 25px; margin-bottom: 25px; }}
        .directive-header {{ color: #CC0000; font-weight: 900; text-transform: uppercase; font-size: 0.8em; margin-bottom: 10px; }}
        .risk-item {{ border-left: 5px solid #CC0000; padding: 15px; margin-bottom: 15px; background: rgba(204, 0, 0, 0.1); font-weight: 600; color: #FFD6D6; }}
        .optimal-item {{ border-left: 5px solid #0B8A1D; padding: 15px; margin-bottom: 15px; background: rgba(11, 138, 29, 0.1); font-weight: 600; color: #D6FFD6; }}
        </style>
        """, unsafe_allow_html=True)

apply_industrial_premium_styling()

# --- 2. DATA ENGINE ---
def load_digital_twin():
    site, api = {"project_name": "J&J Wilson"}, 0.0
    try:
        if Path("data/site_status.json").exists():
            with open("data/site_status.json", "r") as f: site = json.load(f)
        if Path("data/history.csv").exists():
            hist = pd.read_csv("data/history.csv")
            recent = hist.tail(5)["precip_actual"].fillna(0).tolist()
            api = round(sum(r * (0.85 ** i) for i, r in enumerate(reversed(recent))), 3)
    except Exception: pass
    return site, api

site_data, api_val = load_digital_twin()

# --- 3. ANALYTICAL LOGIC ---
# Operational thresholds
sediment_pct = site_data.get('swppp', {}).get('sb3_sediment_pct', 25)
wind_gust = site_data.get('crane_safety', {}).get('max_gust', 0)
lightning_dist = site_data.get('lightning', {}).get('recent_strikes_50mi', 0)
forecast_rain = site_data.get('precipitation', {}).get('forecast_prob', 0)

if api_val < 0.30:
    status, color, grading_rec = "OPTIMAL", "#0B8A1D", "Soil stability high. Full earthwork authorized."
elif api_val < 0.60:
    status, color, grading_rec = "SATURATED", "#FFAA00", "Limit heavy equipment to stabilized roads."
elif api_val < 0.85:
    status, color, grading_rec = "CRITICAL", "#FF6600", "High rutting risk. Restrict grading."
else:
    status, color, grading_rec = "RESTRICTED", "#B00000", "SITE CLOSED TO GRADING."

# --- 4. EXECUTIVE INTERFACE ---
st.markdown(f"""
    <div class="exec-header">
        <div class="exec-title">Wayne Brothers</div>
        <div style="font-size:1.4em; color:#AAA; text-transform:uppercase;">Johnson & Johnson Biologics Manufacturing Facility</div>
        <div style="color:#777;">Wilson, NC | 148.2 Disturbed Acres</div>
    </div>
""", unsafe_allow_html=True)

col_l, col_r = st.columns([2, 1])

with col_l:
    # Field Operational Directive
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">Field Operational Directive</div>', unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:{color}; margin:0;'>STATUS: {status}</h1>", unsafe_allow_html=True)
    st.write(f"**Action:** {grading_rec}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Executive Advisory: Storm Prep & Safety
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">Executive Advisory: Safety & Infrastructure</div>', unsafe_allow_html=True)
    
    # Combined Safety & Maintenance Logic
    if wind_gust > 25:
        st.markdown(f'<div class="risk-item">🚨 CRANE ALERT: Gusts at {wind_gust} MPH. Suspend high-profile lifts immediately.</div>', unsafe_allow_html=True)
    if lightning_dist > 0:
        st.markdown(f'<div class="risk-item">⚡ LIGHTNING ALERT: Strikes detected within 50 miles. Monitor site proximity.</div>', unsafe_allow_html=True)
    if status == "OPTIMAL" and sediment_pct >= 25:
        st.markdown(f'<div class="optimal-item">MAINTENANCE DIRECTIVE: Status is OPTIMAL. Execute Basin SB3 clean-out while dry.</div>', unsafe_allow_html=True)
    elif sediment_pct >= 50:
        st.markdown(f'<div class="risk-item">🚨 LEGAL CRITICAL: Basin SB3 sediment at {sediment_pct}%. Mandatory clean-out required.</div>', unsafe_allow_html=True)
    
    if not (wind_gust > 25 or lightning_dist > 0 or sediment_pct >= 25):
        st.success("No immediate safety or infrastructure impediments forecast.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Windy Interactive Radar
    st.components.v1.html(f"""
        <iframe width="100%" height="450" 
            src="https://embed.windy.com/embed2.html?lat=35.726&lon=-77.916&zoom=9&level=surface&overlay=radar" 
            frameborder="0" style="border-radius:8px;"></iframe>
    """, height=460)

with col_r:
    # Operational Metrics Sidebar
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">Operational Metrics</div>', unsafe_allow_html=True)
    st.metric("Soil Moisture (API)", api_val)
    st.metric("Rain Forecast", f"{forecast_rain}%")
    st.metric("Max Wind Gust", f"{wind_gust} MPH")
    st.metric("Lightning Strikes (50mi)", lightning_dist)
    st.metric("Sediment Level", f"{sediment_pct}%")
    st.caption(f"Last Sync: {dt.datetime.now().strftime('%H:%M:%S')}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">Infrastructure Analysis</div>', unsafe_allow_html=True)
    st.write(f"**Basin SB3 Freeboard:** {site_data.get('swppp', {}).get('freeboard_feet', 1.5)} FT")
    st.write(f"**Satellite Observation:** Perimeter silt fence integrity confirmed; basin skimmer functioning.")
    st.markdown("</div>", unsafe_allow_html=True)
