import streamlit as st
import json
import pandas as pd
import datetime as dt
from pathlib import Path

# --- 1. ARCHITECTURAL CONFIG & STYLING ---
st.set_page_config(page_title="Wayne Brothers | Executive Command", layout="wide")

def apply_industrial_premium_styling():
    bg_url = "https://raw.githubusercontent.com/mickeybhenson-commits/J-J-LMDS-WILSON-NC/main/image_12e160.png"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        
        .stApp {{ 
            background-image: url("{bg_url}"); 
            background-attachment: fixed; 
            background-size: cover; 
            font-family: 'Inter', sans-serif;
        }}
        .stApp:before {{ 
            content: ""; position: fixed; inset: 0; 
            background: radial-gradient(circle at center, rgba(0,0,0,0.85), rgba(0,0,0,0.98)); 
            z-index: 0; 
        }}
        section.main {{ position: relative; z-index: 1; }}

        /* Professional Header block */
        .exec-header {{ margin-bottom: 40px; border-left: 8px solid #CC0000; padding-left: 25px; }}
        .exec-title {{ font-size: 3.5em; font-weight: 900; letter-spacing: -2px; line-height: 1; color: #FFFFFF; margin: 0; }}
        .exec-subtitle {{ font-size: 1.5em; color: #AAAAAA; font-weight: 400; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px; }}
        .exec-location {{ font-size: 1.1em; color: #777777; margin-top: 2px; }}

        /* Directive & Risk Cards */
        .directive-container {{
            background: rgba(20, 20, 25, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        }}
        .directive-label {{ font-weight: 900; text-transform: uppercase; letter-spacing: 1px; color: #CC0000; margin-bottom: 15px; font-size: 0.9em; }}
        
        .metric-box {{ text-align: center; padding: 20px; border-right: 1px solid rgba(255,255,255,0.1); }}
        .metric-label {{ color: #777; font-size: 0.8em; text-transform: uppercase; font-weight: 700; }}
        .metric-value {{ font-size: 2.2em; font-weight: 900; color: #FFF; }}
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
if api_val < 0.30:
    status, color, grading_rec = "Optimal", "#0B8A1D", "Soil stability is maximum. Unrestricted grading operations authorized."
elif api_val < 0.60:
    status, color, grading_rec = "Saturated", "#FFAA00", "Soil moisture elevated. Hauling restricted to stabilized access roads."
elif api_val < 0.85:
    status, color, grading_rec = "Critical", "#FF6600", "High rutting risk. Grading restricted to prevent subgrade damage."
else:
    status, color, grading_rec = "Restricted", "#B00000", "SITE CLOSED TO GRADING. Operations suspended for soil structure defense."

# --- 4. EXECUTIVE INTERFACE ---

# High-Tier Header
st.markdown(f"""
    <div class="exec-header">
        <div class="exec-title">Wayne Brothers</div>
        <div class="exec-subtitle">Johnson & Johnson Biologics Manufacturing Facility</div>
        <div class="exec-location">Wilson, North Carolina | 148.2 Disturbed Acres</div>
    </div>
""", unsafe_allow_html=True)

# Main Dashboard Grid
col_main, col_side = st.columns([2, 1])

with col_main:
    # Top-Level Directives
    st.markdown(f"""
        <div class="directive-container" style="border-top: 5px solid {color};">
            <div class="directive-label">Field Operational Directive</div>
            <h2 style="margin:0; color:{color}; font-weight:900;">STATUS: {status.upper()}</h2>
            <p style="font-size:1.2em; margin-top:10px; color:#EEE;">{grading_rec}</p>
        </div>
    """, unsafe_allow_html=True)

    # Predictive Intelligence Section
    st.markdown("### Predictive Environmental Risk")
    st.components.v1.html(f"""
        <iframe width="100%" height="400" 
            src="https://embed.windy.com/embed2.html?lat=35.726&lon=-77.916&zoom=9&level=surface&overlay=radar&metricWind=mph&metricTemp=%C2%B0F" 
            frameborder="0" style="border-radius:8px;"></iframe>
    """, height=410)

with col_side:
    # Critical SWPPP Metrics
    st.markdown("### Compliance Analytics")
    st.markdown(f"""
        <div class="directive-container">
            <div class="directive-label">Sediment Basin SB3</div>
            <div style="font-size: 2.5em; font-weight:900;">{site_data['swppp']['sb3_capacity_pct']}%</div>
            <div style="color:#777; margin-bottom:15px;">CAPACITY UTILIZED</div>
            <div class="metric-label">Available Freeboard</div>
            <div style="font-size:1.5em; font-weight:700;">{site_data['swppp']['freeboard_feet']} FT</div>
        </div>
    """, unsafe_allow_html=True)

    # Risk Forecast
    if site_data['precipitation']['forecast_prob'] > 50:
        st.error(f"STORM ALERT: {site_data['precipitation']['forecast_prob']}% probability of precipitation. Pre-storm stabilization required for 148.2-acre perimeter.")
    else:
        st.success("Stable weather window detected for the next 24 hours.")

# Multi-Metric Footer Strip
st.markdown("---")
m_cols = st.columns(4)
with m_cols[0]:
    st.markdown(f'<div class="metric-box"><p class="metric-label">Soil Saturation (API)</p><p class="metric-value">{api_val}</p></div>', unsafe_allow_html=True)
with m_cols[1]:
    st.markdown(f'<div class="metric-box"><p class="metric-label">24H Rain Actual</p><p class="metric-value">{site_data["precipitation"]["actual_24h"]} IN</p></div>', unsafe_allow_html=True)
with m_cols[2]:
    st.markdown(f'<div class="metric-box"><p class="metric-label">Max Wind Gust</p><p class="metric-value">{site_data["crane_safety"]["max_gust"]} MPH</p></div>', unsafe_allow_html=True)
with m_cols[3]:
    st.markdown(f'<div class="metric-box" style="border:none;"><p class="metric-label">Lightning Threat</p><p class="metric-value">{site_data["lightning"]["forecast"]}</p></div>', unsafe_allow_html=True)
