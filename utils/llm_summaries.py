import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_openai_client():
    """Initialize OpenAI client if API key is available"""
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your-api-key-here':
        try:
            return OpenAI(api_key=api_key)
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            return None
    return None


def generate_travel_summary(city, country, best_months_data, preferences):
    """
    Generate a natural language summary of the best time to visit
    """
    client = get_openai_client()

    if not client:
        return None

    # Prepare the data for the prompt
    months_info = []
    for _, row in best_months_data.iterrows():
        months_info.append({
            'month': row['month_name'],
            'score': row['score'],
            'temp': row['avg_temp_c'],
            'rain': row['rainfall_mm'],
            'crowds': row['tourist_index'],
            'cost': row['cost_index']
        })

    # Create a detailed prompt
    prompt = f"""You are a travel expert providing personalized recommendations. 

Destination: {city}, {country}

User's Preferences:
- Temperature range: {preferences['temp_min']}°C to {preferences['temp_max']}°C
- Rain tolerance: {preferences['rain_tolerance']}
- Crowd preference: {preferences['crowd_tolerance']}
- Budget level: {preferences['budget_level']}
- Priority: {preferences['priority']}

Top 3 Recommended Months:
"""

    for month in months_info:
        prompt += f"""
{month['month']}: Score {month['score']}/10
- Temperature: {month['temp']}°C
- Rainfall: {month['rain']}mm
- Crowd level: {month['crowds']}/10
- Cost index: {month['cost']}/10
"""

    prompt += """
Write a friendly, concise 2-3 paragraph travel recommendation. Include:
1. Which month(s) are best and why
2. What to expect (weather, crowds, costs)
3. Any trade-offs or insider tips

Keep it conversational and helpful. Don't use bullet points."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cheaper and faster
            messages=[
                {"role": "system", "content": "You are a knowledgeable travel advisor who gives personalized, concise recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating summary: {e}")
        return None


def generate_quick_insight(city, month_name, month_data):
    """
    Generate a quick one-liner insight for a specific month
    """
    client = get_openai_client()

    if not client:
        return None

    prompt = f"""Give a single sentence insight about visiting {city} in {month_name}.

Data:
- Temperature: {month_data['avg_temp_c']}°C
- Rainfall: {month_data['rainfall_mm']}mm
- Crowds: {month_data['tourist_index']}/10
- Cost: {month_data['cost_index']}/10

Make it specific and helpful. No generic statements."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel expert providing concise insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.8
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating insight: {e}")
        return None