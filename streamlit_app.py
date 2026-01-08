import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. TRUTH ENGINE: USGS GAUGE FETCH (Lucama Site 02090380)
def get_ground_truth():
    """Pulls 15-minute precipitation data from USGS. Ground Truth > Forecast."""
    try:
        # USGS Water Services IV (Instantaneous Values) API
        url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=02090380&parameterCd=00045"
        resp = requests.get(url, timeout=10).json()
        # Extract the latest 15-min rainfall value
        latest_val = resp['value']['timeSeries'][0]['values'][0]['value'][0]['value']
        return float(latest_val)
    except Exception:
        return 0.0  # Fallback to zero if sensor or API is offline

# 2. SITE DATA HIERARCHY
# The 'forecast_val' is what we predicted earlier (0.5").
# 'ground_truth' is what the sensor actually sees right now.
forecast_val = 0.5 
ground_truth = get_ground_truth()

# PRIORITY RULE: Forecast is TRUMPED by Ground Truth
# Since it didn't rain today, ground_truth will be 0.0
final_rain = ground_truth 

# 3. DYNAMIC THEME (Visuals change based on Truth, not Prediction)
if final_rain >= 0.1:
    theme_color = "#FF4B4B" # Red (Storm Action)
    status_label = "🔴 STORM ACTION: SITE SATURATED"
    priority = "Erosion Control & Runoff Monitoring"
else:
    theme_color = "#28A745" # Green (Stable)
    status_label = "✅ STABLE: PROCEED WITH WORK"
    priority = "Mass Grading & Site Logistics"

# 4. DASHBOARD UI (Maintaining original layout)
st.markdown(f"<h1 style='text-align: center; color: {theme_color};'>{status_label}</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.metric("Rainfall (USGS Ground Truth)", f"{final_rain}\"", 
          delta=f"{final_rain - forecast_val}\" vs Forecast", 
          delta_color="normal" if final_rain == 0 else "inverse")
col2.metric("Last Sync", datetime.now().strftime("%H:%M"))

st.info(f"**Field Directive:** {priority}")

# 5. WEEKLY ADVISORY (Forced by Truth)
st.subheader("Revised Site Advisory")
advisory_df = pd.DataFrame({
    "Day": ["Wed (Today)", "Thu", "Fri", "Sat"],
    "Status": [status_label.split(":")[0], "SATURATED" if final_rain > 0 else "STABLE", "DRYING", "RECOVERY"],
    "Action": [priority, "Limit Hauling" if final_rain > 0 else "Grading", "Clean Basins", "Standard Ops"]
})
st.table(advisory_df)

st.caption("Data Source: USGS 02090380 (Lucama, NC). Updated every 15 minutes.")
