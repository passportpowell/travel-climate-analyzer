import pandas as pd

def calculate_weather_score(temp, rain, temp_pref_min, temp_pref_max, rain_tolerance):
    """
    Calculate weather score based on preferences
    """
    # Temperature score (0-10)
    if temp_pref_min <= temp <= temp_pref_max:
        temp_score = 10
    elif temp < temp_pref_min:
        temp_score = max(0, 10 - (temp_pref_min - temp) * 0.5)
    else:
        temp_score = max(0, 10 - (temp - temp_pref_max) * 0.5)
    
    # Rainfall score (0-10)
    # rain_tolerance: 'low' = want dry, 'medium' = okay with some rain, 'high' = don't mind rain
    if rain_tolerance == 'low':
        rain_score = max(0, 10 - rain / 10)
    elif rain_tolerance == 'medium':
        rain_score = max(0, 10 - rain / 20)
    else:  # high tolerance
        rain_score = max(0, 10 - rain / 30)
    
    # Weighted average
    weather_score = (temp_score * 0.6 + rain_score * 0.4)
    return round(weather_score, 1)

def calculate_best_time_score(row, preferences):
    """
    Calculate overall score based on weather, crowds, and cost
    """
    # Get preference weights
    if preferences['priority'] == 'weather':
        weights = {'weather': 0.5, 'crowds': 0.25, 'cost': 0.25}
    elif preferences['priority'] == 'avoid_crowds':
        weights = {'weather': 0.3, 'crowds': 0.5, 'cost': 0.2}
    elif preferences['priority'] == 'budget':
        weights = {'weather': 0.3, 'crowds': 0.2, 'cost': 0.5}
    else:  # balanced
        weights = {'weather': 0.35, 'crowds': 0.35, 'cost': 0.3}
    
    # Calculate component scores
    weather_score = calculate_weather_score(
        row['avg_temp_c'],
        row['rainfall_mm'],
        preferences['temp_min'],
        preferences['temp_max'],
        preferences['rain_tolerance']
    )
    
    # Crowd score (invert tourist_index if avoiding crowds)
    if preferences['crowd_tolerance'] == 'avoid':
        crowd_score = 10 - row['tourist_index']
    elif preferences['crowd_tolerance'] == 'neutral':
        crowd_score = 7.0  # neutral score
    else:  # 'enjoy'
        crowd_score = row['tourist_index']
    
    # Cost score (lower cost_index = higher score if budget-conscious)
    if preferences['budget_level'] == 'budget':
        cost_score = 10 - row['cost_index']
    elif preferences['budget_level'] == 'mid':
        cost_score = 7.0
    else:  # luxury
        cost_score = row['cost_index']
    
    # Calculate weighted total
    total_score = (
        weather_score * weights['weather'] +
        crowd_score * weights['crowds'] +
        cost_score * weights['cost']
    )
    
    return round(total_score, 1)

def get_best_months(df, city, preferences, top_n=3):
    """
    Get the top N best months for a city based on preferences
    """
    city_data = df[df['city'] == city].copy()
    
    # Calculate scores for each month
    city_data['score'] = city_data.apply(
        lambda row: calculate_best_time_score(row, preferences),
        axis=1
    )
    
    # Sort by score
    best_months = city_data.nlargest(top_n, 'score')
    
    return best_months