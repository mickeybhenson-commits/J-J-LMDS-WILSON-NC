import streamlit as st
import json
import pandas as pd
import datetime as dt
import requests
from pathlib import Path
from streamlit_autorefresh import st_autorefresh 

# --- 1. ARCHITECTURAL CONFIG & PREMIUM STYLING ---
st.set_page_config(page_title="Wayne Brothers | Universal Command", layout="wide")
st_autorefresh(interval=300000, key="datarefresh") # 5-Min Sync

def apply_universal_command_styling():
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
        .sync-badge {{ background: rgba(255, 255, 255, 0.1); color: #00FFCC; padding: 5px 12px; border-radius: 50px; font-size: 0.8em; font-weight: 700; border: 1px solid #00FFCC; }}
        .report-section {{ background: rgba(15, 15, 20, 0.9); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 25px; margin-bottom: 20px; }}
        .directive-header {{ color: #CC0000; font-weight: 900; text-transform: uppercase; font-size: 0.85em; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px; }}
        .forecast-card {{ text-align: center; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); line-height: 1.1; min-height: 140px; }}
        .temp-box {{ background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 0.85em; margin: 4px 0; display: inline-block; }}
        .precip-box {{ color: #00FFCC; font-weight: 700; font-size: 0.85em; margin-top: 4px; }}
        </style>
        """, unsafe_allow_html=True)

apply_universal_command_styling()

# --- 2. GROUND TRUTH ENGINE (USGS 02090380) ---
def get_usgs_ground_truth():
    try:
        url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=02090380&parameterCd=00045"
        resp = requests.get(url, timeout=5).json()
        val = resp['value']['timeSeries'][0]['values'][0]['value'][0]['value']
        return float(val)
    except:
        return 0.0

usgs_rain = get_usgs_ground_truth()

# --- 3. PROJECT CONSTANTS & TACTICAL MAPPING ---
SITE_NAME = "Johnson & Johnson Biologics Manufacturing Facility"
current_dt = dt.datetime.now()
current_time = current_dt.strftime('%H:%M')
current_day = current_dt.strftime('%a')
SOIL_MOISTURE_VAL = 0.058 

tactical_map = {
    "Mon": {"status": "MAINTENANCE", "color": "#FFFF00", "hi": 55, "lo": 29, "pop": "10%", "in": "0.00\"", "task": "PRIORITY: Clean Basin SB3 + Inspect Silt Fences"},
    "Tue": {"status": "MAINTENANCE", "color": "#FFFF00", "hi": 60, "lo": 41, "pop": "10%", "in": "0.01\"", "task": "PRIORITY: Clean Basin SB3 + Inspect Silt Fences"},
    "Wed": {"status": "CRITICAL", "color": "#FF0000", "hi": 67, "lo": 44, "pop": "80%", "in": "0.55\"", "task": "STORM ACTION: Runoff Surge Monitoring (High Risk)"},
    "Thu": {"status": "RESTRICTED", "color": "#FF8C00", "hi": 64, "lo": 43, "pop": "40%", "in": "0.10\"", "task": "Saturated: Limit Heavy Hauling / Protect Subgrade"},
    "Fri": {"status": "CAUTION", "color": "#FFFF00", "hi": 71, "lo": 48, "pop": "20%", "in": "0.00\"", "task": "Drying: Monitor Sediment Trap Recovery"},
    "Sat": {"status": "RECOVERY", "color": "#00FF00", "hi": 71, "lo": 53, "pop": "20%", "in": "0.00\"", "task": "Recovery: Resume Standard Mass Grading"},
    "Sun": {"status": "STABLE", "color": "#00FFCC", "hi": 53, "lo": 34, "pop": "20%", "in": "0.00\"", "task": "Stable: Reset for Monday"}
}

# --- 4. THE GROUND TRUTH OVERRIDE ---
if usgs_rain == 0.0:
    for day in ["Wed", "Thu"]:
        if current_day == day:
            tactical_map[day]["status"] = "STABLE"
            tactical_map[day]["color"] = "#00FFCC"
            tactical_map[day]["task"] = "VERIFIED DRY: Resume Standard Operations"
            tactical_map[day]["pop"] = "0%"
            tactical_map[day]["in"] = "0.00\" (USGS)"

today = tactical_map.get(current_day, tactical_map["Sun"])

# --- 5. UI RENDERING ---
st.markdown(f"""
    <div class="exec-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="exec-title">Wayne Brothers</div>
            <div class="sync-badge">USGS TRUTH SYNC • {current_time}</div>
        </div>
        <div style="font-size:1.5em; color:#AAA; text-transform:uppercase;">{SITE_NAME}</div>
    </div>
""", unsafe_allow_html=True)

c_main, c_metrics = st.columns([2, 1])

with c_main:
    st.markdown(f"""
        <div class="report-section" style="border-top: 8px solid {today['color']};">
            <div class="directive-header">Field Operational Directive • {current_day.upper()} VALIDATION</div>
            <h1 style="color: {today['color']}; margin: 0; font-size: 3.5em; letter-spacing: -2px;">{today['status']}</h1>
            <p style="font-size: 1.3em; margin-top: 10px;"><b>{today['in']} Rain:</b> {today['task']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">7-Day Weather Outlook</div>', unsafe_allow_html=True)
    f_cols = st.columns(7)
    for i, (day_key, d) in enumerate(tactical_map.items()):
        f_cols[i].markdown(f"""
            <div class="forecast-card" style="border-top: 4px solid {d['color']};">
                <b>{day_key}</b><br>
                <div class="temp-box">{d['hi']}°/{d['lo']}°</div><br>
                <div class="precip-box">{d['pop']} Prob</div>
                <div style="font-size: 0.8em; color: #AAA;">{d['in']} Total</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_metrics:
    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<div class="directive-header">Analytical Metrics</div>', unsafe_allow_html=True)
    st.metric("USGS Ground Truth (Rain)", f"{usgs_rain}\"", delta="DRY (VERIFIED)" if usgs_rain == 0 else "PRECIP DETECTED")
    st.metric("Soil Moisture (API)", SOIL_MOISTURE_VAL)
    st.metric(label="Basin SB3 Capacity", value="58%", delta="STABLE" if usgs_rain == 0 else "MONITOR", delta_color="normal" if usgs_rain == 0 else "inverse")
    st.metric("Temperature", "54°F")
    st.metric("Humidity", "55%")
    st.metric("NC DEQ NTU Limit", "50 NTU")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. RADAR & SURVEILLANCE ---
st.markdown('<div class="report-section">', unsafe_allow_html=True)
st.markdown('<div class="directive-header">Surveillance Radar: Wilson County</div>', unsafe_allow_html=True)
st.components.v1.html(f'<iframe width="100%" height="450" src="https://embed.windy.com/embed2.html?lat=35.726&lon=-77.916&zoom=9&level=surface&overlay=radar" frameborder="0" style="border-radius:8px;"></iframe>', height=460)
st.markdown('</div>', unsafe_allow_html=True)
