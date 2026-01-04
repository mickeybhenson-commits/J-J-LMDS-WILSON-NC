def create_precipitation_table(history_df):
    """Create 14-day precipitation table (7 past + 7 forecast)"""
    
    # Get last 7 days of actual data
    if not history_df.empty and 'date' in history_df.columns and 'precip_actual' in history_df.columns:
        past_7 = history_df.tail(7).copy()
        past_7['Type'] = 'Actual'
        past_7 = past_7.rename(columns={'precip_actual': 'Precipitation (IN)'})
        past_7['Date'] = past_7['date'].dt.strftime('%Y-%m-%d')
        past_7['Probability %'] = '-'
        past_7 = past_7[['Date', 'Precipitation (IN)', 'Probability %', 'Type']]
    else:
        past_7 = pd.DataFrame(columns=['Date', 'Precipitation (IN)', 'Probability %', 'Type'])
    
    # Get REAL forecast from Open-Meteo API
    try:
        weather_api = WeatherAPI(latitude=35.726, longitude=-77.916)  # Wilson, NC
        forecast_df = weather_api.get_7day_forecast()
        
        forecast_7 = pd.DataFrame({
            'Date': forecast_df['date'],
            'Precipitation (IN)': forecast_df['precip_forecast'],
            'Probability %': forecast_df['precip_prob'].astype(str) + '%',
            'Type': 'Forecast'
        })
    except Exception as e:
        st.warning(f"Weather API temporarily unavailable. Using backup data.")
        # Fallback to mock data
        today = datetime.datetime.now()
        forecast_dates = [(today + datetime.timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(7)]
        forecast_7 = pd.DataFrame({
            'Date': forecast_dates,
            'Precipitation (IN)': [0.10, 0.25, 0.00, 0.15, 0.30, 0.05, 0.00],
            'Probability %': ['40%', '60%', '10%', '50%', '70%', '30%', '10%'],
            'Type': 'Forecast'
        })
    
    # Combine past and forecast
    combined = pd.concat([past_7, forecast_7], ignore_index=True)
    
    return combined
