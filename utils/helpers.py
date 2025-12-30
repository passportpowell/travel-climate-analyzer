import pandas as pd
from datetime import datetime

def get_month_name(month_num):
    """Convert month number to name"""
    months = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    return months.get(month_num, "Unknown")

def get_season(month_num, hemisphere='north'):
    """Determine season based on month and hemisphere"""
    if hemisphere == 'north':
        if month_num in [12, 1, 2]:
            return "Winter"
        elif month_num in [3, 4, 5]:
            return "Spring"
        elif month_num in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"
    else:  # southern hemisphere
        if month_num in [12, 1, 2]:
            return "Summer"
        elif month_num in [3, 4, 5]:
            return "Autumn"
        elif month_num in [6, 7, 8]:
            return "Winter"
        else:
            return "Spring"

def normalize_score(value, min_val, max_val, invert=False):
    """Normalize a value to 0-10 scale"""
    if max_val == min_val:
        return 5.0
    
    normalized = (value - min_val) / (max_val - min_val) * 10
    
    if invert:
        normalized = 10 - normalized
    
    return round(normalized, 1)