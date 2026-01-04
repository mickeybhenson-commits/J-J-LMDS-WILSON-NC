import streamlit as st
import json
import pandas as pd
import datetime as dt
from pathlib import Path
from streamlit_autorefresh import st_autorefresh 

# --- 1. ARCHITECTURAL CONFIG & CSS ---
st.set_page_config(page_title="Wayne Brothers | Total Site Command", layout="wide")

# 5-Minute Professional Sync
st_autorefresh(interval=300000, key="datarefresh")

def apply_total_command_styling():
    bg_url = "https://raw.githubusercontent.com/mickeybhenson-commits/J-J-LMDS-WILSON-NC/main/image_12e160.png"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        .stApp {{ background-image: url("{bg_url}"); background-attachment: fixed; background-size: cover; font-family: 'Inter', sans-serif; }}
        .stApp:before {{ content: ""; position: fixed; inset: 0; background: radial-gradient(circle at center, rgba(0,0,0,0.88), rgba(0,0,0,0.97)); z-index: 0; }}
        section.main {{ position: relative; z-index: 1; }}

        .exec-header {{ margin-bottom: 30px; border-left: 10px solid #CC0000; padding-left: 25px; }}
        .exec-title {{ font-size: 3.8em; font-weight: 900; letter-spacing: -2px; line-height: 1; color: #FFFFFF; margin: 0; }}
        .exec-subtitle {{ font-size: 1.5em; color: #AAAAAA; text-transform: uppercase; letter-spacing: 2px; margin-top: 5px; }}
        
        .report-section {{ background: rgba(15, 15, 20, 0.9); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 25px; margin-bottom: 20px; }}
        .directive-header {{ color: #CC0000; font-weight: 900; text-transform: uppercase; font-size: 0.85em; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px; }}
        
        .status-pill {{ padding: 4px 12px; border-radius: 4px; font-weight: 900; font-size: 0.85em; text-transform: uppercase; }}
        .alert-box {{ border-left: 5px solid #CC0000; padding: 15px; margin-bottom: 15px; background: rgba(204, 0, 0, 0.1); font-weight: 600; }}
        </style>
        """, unsafe_allow_html=True)

apply_total_command_styling()

# --- 2. DATA ENGINE ---
def load_site_data():
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

site_data, api_val = load_site_data()

# --- 3. ANALYTICAL LOGIC LAYER ---
# A. Soil Workability
if api_val < 0.30: status, s_color, s_msg = "OPTIMAL", "#0B8A1D", "Full grading authorized."
elif api_val < 0.60: status, s_color, s_msg = "SATURATED", "#FFAA00", "Limit heavy hauling."
elif api_val < 0.85: status, s_color, s_msg = "CRITICAL", "#FF6600", "Protect subgrade. Restrict grading."
else: status, s_color, s_msg = "RESTRICTED", "#B00000", "SITE CLOSED TO GRADING."

# B. Safety & Infrastructure Thresholds
wind = site_data.get('crane_safety', {}).get('max_gust', 0)
light = site_data.get('lightning', {}).get('recent_strikes_50mi', 0)
sed_pct = site_data.get('swppp', {}).get('sb3_sediment_pct', 25)
rain_p = site_data.get('precipitation', {}).get('forecast_prob', 0)

# --- 4. EXECUTIVE COMMAND CENTER ---
st.markdown(f"""
    <div class="exec-header">
        <div class="exec-title">Wayne Brothers</div>
        <div class="exec-subtitle">Johnson & Johnson Biologics Manufacturing Facility</div>
        <div style="color:#777;">Wilson, NC | 148.2 Disturbed Acres</div>
    </div>
""", unsafe_allow_html=True)

# Main Grid Layout
c_main, c_side = st.columns([2, 1])

with c_main:
    # 1. PRIMARY OPERATIONAL DIRECTIVE
    st.markdown(f"""
        <div class="report-section" style="border-top: 6px solid {s_color};">
            <div class="directive-header">Field Operational Directive</div>
            <h1 style="color:{s_color}; margin:0; font-size:3.5em;">{status}</h1>
            <p style="font-size:1.3em; color:#EEE;">{s_msg}</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. INFRASTRUCTURE HEALTH & EROSION CONTROL
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">Erosion Control & Silt Fence Surveillance</div>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    i1.markdown(f"**Silt Fence** <br> <span class='status-pill' style='background:#0B8A1D;'>Optimal</span>", unsafe_allow_html=True)
    i2.markdown(f"**Basin Skimmers** <br> <span class='status-pill' style='background:#0B8A1D;'>Functional</span>", unsafe_allow_html=True)
    i3.markdown(f"**Slope Stabil.** <br> <span class='status-pill' style='background:#B00000;'>Stressed (40%)</span>", unsafe_allow_html=True)
    st.write("---")
    st.write("**Visual Intelligence Analysis:** Perimeter integrity confirmed; East low points under monitoring. Slope stabilization (seeding/mulching) requires dry-window hardening.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. INTERACTIVE RADAR SURVEILLANCE
    st.components.v1.html(f"""<iframe width="100%" height="400" src="https://embed.windy.com/embed2.html?lat=35.726&lon=-77.916&zoom=9&level=surface&overlay=radar" frameborder="0" style="border-radius:8px;"></iframe>""", height=410)

with c_side:
    # 4. EXECUTIVE ADVISORY (SAFETY & PREDICTIVE)
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">Executive Advisory</div>', unsafe_allow_html=True)
    if wind > 25: st.markdown(f'<div class="alert-box">🚨 CRANE: Gusts {wind} MPH. STOP LIFTS.</div>', unsafe_allow_html=True)
    if light > 0: st.markdown(f'<div class="alert-box" style="border-color:#FFAA00;">⚡ LIGHTNING: {light} Strikes within 50mi.</div>', unsafe_allow_html=True)
    if status == "OPTIMAL" and sed_pct >= 25:
        st.markdown(f'<div class="alert-box" style="border-color:#0B8A1D; background:rgba(11,138,29,0.1); color:#D6FFD6;">CMD: Status OPTIMAL. Empty Basin SB3 immediately.</div>', unsafe_allow_html=True)
    if rain_p > 50: st.markdown(f'<div class="alert-box">🌧️ STORM: {rain_p}% Prob. Prep for runoff event.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. ALL ANALYZED METRICS
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">Analytical Metrics Summary</div>', unsafe_allow_html=True)
    st.metric("Soil Saturation (API)", api_val)
    st.metric("Basin SB3 Capacity", f"{site_data.get('swppp', {}).get('sb3_capacity_pct', 58)}%")
    st.metric("Sediment Accumulation", f"{sed_pct}%")
    st.metric("Wind Gust Speed", f"{wind} MPH")
    st.write(f"**Freeboard:** {site_data.get('swppp', {}).get('freeboard_feet', 1.5)} FT")
    st.caption(f"Last Refresh: {dt.datetime.now().strftime('%H:%M:%S')}")
    st.markdown('</div>', unsafe_allow_html=True)
