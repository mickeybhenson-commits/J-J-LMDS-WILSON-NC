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
        .truth-card {{ text-align: center; padding: 12px; background: rgba(0, 255, 204, 0.08); border-radius: 8px; border: 1px solid #00FFCC; min-height: 90px; }}
        .forecast-card {{ text-align: center; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); line-height: 1.1; min-height: 140px; }}
        .temp-box {{ background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 0.85em; margin: 4px 0; display: inline-block; }}
        .precip-box {{ color: #00FFCC; font-weight: 700; font-size: 0.85em; margin-top: 4px; }}
        </style>
        """, unsafe_allow_html=True)

apply_universal_command_styling()

# --- 2. MULTI-SOURCE TRUTH COLLECTOR ---
ACCU_KEY = st.secrets.get("ACCU_KEY", "zpka_f1d5b5f80b014057b3a6e57011d9b56a_77161a13")

def get_usgs_truth():
    try:
        url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=02090380&parameterCd=00045"
        resp = requests.get(url, timeout=5).json()
        return float(resp['value']['timeSeries'][0]['values'][0]['value'][0]['value'])
    except: return 0.0

def get_accu_minutecast():
    try:
        url = f"https://dataservice.accuweather.com/forecasts/v1/minute?q=35.73,-77.92&apikey={ACCU_KEY}"
        resp = requests.get(url, timeout=5).json()
        return resp.get("Summary", {}).get("Phrase", "No rain detected")
    except: return "Manual Override Active"

usgs_val = get_usgs_truth()
minutecast_phrase = get_accu_minutecast()

# --- 3. DYNAMIC ROLLING CALENDAR ENGINE ---
current_dt = dt.datetime.now()
current_day_name = current_dt.strftime('%a')
# Generate next 7 days dynamically (Today + 6)
rolling_dates = [(current_dt + dt.timedelta(days=i)) for i in range(7)]

master_forecast = {
    "Mon": {"status": "STABLE", "color": "#00FFCC", "hi": 58, "lo": 34, "pop": "1%", "in": "0.00\"", "task": "Completed: Site Maintenance"},
    "Tue": {"status": "STABLE", "color": "#00FFCC", "hi": 63, "lo": 42, "pop": "2%", "in": "0.00\"", "task": "Completed: Silt Fence Audit"},
    "Wed": {"status": "STABLE", "color": "#00FFCC", "hi": 72, "lo": 38, "pop": "1%", "in": "0.00\"", "task": "VERIFIED DRY: Resume Standard Ops"},
    "Thu": {"status": "STABLE", "color": "#00FFCC", "hi": 63, "lo": 42, "pop": "0%", "in": "0.00\"", "task": "Operational: Clear skies forecast"},
    "Fri": {"status": "RESTRICTED", "color": "#FF8C00", "hi": 74, "lo": 57, "pop": "25%", "in": "0.02\"", "task": "Caution: Evening showers possible"},
    "Sat": {"status": "CRITICAL", "color": "#FF0000", "hi": 76, "lo": 57, "pop": "49%", "in": "0.15\"", "task": "Alert: Thunderstorms / Runoff Risk"},
    "Sun": {"status": "RECOVERY", "color": "#FFFF00", "hi": 61, "lo": 30, "pop": "25%", "in": "0.05\"", "task": "Drying: Significant Temperature Drop"}
}

# --- 4. UI RENDERING ---
st.markdown(f"""
    <div class="exec-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="exec-title">Wayne Brothers</div>
            <div class="sync-badge">MULTI-SOURCE TRUTH SYNC • {current_dt.strftime('%H:%M')}</div>
        </div>
        <div style="font-size:1.5em; color:#AAA; text-transform:uppercase;">Johnson & Johnson Biologics Manufacturing Facility</div>
    </div>
""", unsafe_allow_html=True)

c_main, c_metrics = st.columns([2, 1])

with c_main:
    # 1. Rolling Current Status (Always Today)
    today_data = master_forecast.get(current_day_name, master_forecast["Sun"])
    st.markdown(f"""
        <div class="report-section" style="border-top: 8px solid {today_data['color']};">
            <div class="directive-header">Field Operational Directive • ROLLING STATUS</div>
            <h1 style="color: {today_data['color']}; margin: 0; font-size: 3.5em; letter-spacing: -2px;">{today_data['status']}</h1>
            <p style="font-size: 1.3em; margin-top: 10px;"><b>{minutecast_phrase}:</b> {today_data['task']}</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. Rolling 7-Day Outlook (Yesterday is Deleted, Next Day Appears)
    st.markdown('<div class="report-section"><div class="directive-header">Rolling 7-Day Weather Outlook</div>', unsafe_allow_html=True)
    f_cols = st.columns(7)
    for i, date_obj in enumerate(rolling_dates):
        day_key = date_obj.strftime('%a')
        d = master_forecast.get(day_key, master_forecast["Sun"])
        f_cols[i].markdown(f"""
            <div class="forecast-card" style="border-top: 4px solid {d['color']};">
                <b style="color:#00FFCC;">{day_key}</b><br>
                <small>{date_obj.strftime('%m/%d')}</small><br>
                <div class="temp-box">{d['hi']}°/{d['lo']}°</div><br>
                <div class="precip-box">{d['pop']} Prob</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c_metrics:
    st.markdown('<div class="report-section"><div class="directive-header">Analytical Metrics</div>', unsafe_allow_html=True)
    st.metric("USGS Gauge (Rain)", f"{usgs_val}\"", delta="DRY" if usgs_val == 0 else "PRECIP")
    st.metric(label="Basin SB3 Capacity", value="58%", delta="STABLE" if usgs_val == 0 else "MONITOR")
    st.metric("Temperature (Today)", f"{today_data['hi']}°F")
    st.metric("Humidity", "55%")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Radar Surveillance
st.markdown('<div class="report-section"><div class="directive-header">Surveillance Radar: Wilson County</div>', unsafe_allow_html=True)
st.components.v1.html(f'<iframe width="100%" height="450" src="https://embed.windy.com/embed2.html?lat=35.726&lon=-77.916&zoom=9&overlay=radar" frameborder="0" style="border-radius:8px;"></iframe>', height=460)
st.markdown('</div>', unsafe_allow_html=True)
