import requests
import pandas as pd
import json
from datetime import datetime, timedelta

def fetch_weather_data(latitude, longitude, city_name):
    """
    Fetch weather data from Open-Meteo API (FREE - no API key needed)
    """
    # Get historical weather data for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "daily": "temperature_2m_mean,precipitation_sum",
        "timezone": "auto"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Process data by month
        df = pd.DataFrame({
            'date': pd.to_datetime(data['daily']['time']),
            'temp': data['daily']['temperature_2m_mean'],
            'rain': data['daily']['precipitation_sum']
        })
        
        df['month'] = df['date'].dt.month
        
        # Calculate monthly averages
        monthly_data = df.groupby('month').agg({
            'temp': 'mean',
            'rain': 'sum'
        }).reset_index()
        
        monthly_data['city'] = city_name
        monthly_data.columns = ['month', 'avg_temp_c', 'rainfall_mm', 'city']
        
        return monthly_data
    
    except Exception as e:
        print(f"Error fetching weather for {city_name}: {e}")
        return None

def calculate_crowd_index(month, peak_months):
    """
    Calculate crowd index (1-10 scale) based on peak tourist months
    10 = highest crowds, 1 = lowest crowds
    """
    if month in peak_months:
        return 9.0
    elif month in [m-1 if m > 1 else 12 for m in peak_months] or \
         month in [m+1 if m < 12 else 1 for m in peak_months]:
        return 7.0
    else:
        return 4.0

def generate_dataset():
    """
    Generate the complete dataset for all cities
    """
    # Load cities
    with open('data/cities.json', 'r') as f:
        cities_data = json.load(f)
    
    all_data = []
    
    print("Fetching weather data for all cities...")
    
    for city_info in cities_data['cities']:
        print(f"Processing {city_info['name']}...")
        
        # Fetch weather data
        weather_data = fetch_weather_data(
            city_info['latitude'],
            city_info['longitude'],
            city_info['name']
        )
        
        if weather_data is not None:
            # Add crowd and cost indices
            for _, row in weather_data.iterrows():
                month = int(row['month'])
                
                all_data.append({
                    'city': city_info['name'],
                    'country': city_info['country'],
                    'month': month,
                    'month_name': get_month_name(month),
                    'avg_temp_c': round(row['avg_temp_c'], 1),
                    'rainfall_mm': round(row['rainfall_mm'], 1),
                    'tourist_index': calculate_crowd_index(month, city_info['tourist_peak_months']),
                    'cost_index': city_info['cost_index']
                })
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to CSV
    df.to_csv('data/processed_data.csv', index=False)
    print(f"\nDataset generated successfully: {len(df)} rows")
    print(f"Saved to: data/processed_data.csv")
    
    return df

def get_month_name(month_num):
    """Convert month number to name"""
    months = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    return months.get(month_num, "Unknown")

if __name__ == "__main__":
    # Run data collection
    generate_dataset()