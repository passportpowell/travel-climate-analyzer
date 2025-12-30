# 🌍 TravelTiming - AI Travel Planner with LLM Integration & Interactive Data Visualizations

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991.svg)](https://openai.com/)

**Full-stack travel intelligence app combining LLM-powered recommendations, real-time weather API integration, custom scoring algorithms, and interactive Plotly visualizations across 40+ global destinations.**

TravelTiming demonstrates advanced data science and AI engineering capabilities through intelligent travel planning. The application integrates OpenAI's GPT-4o-mini for natural language insights, Open-Meteo API for real-time climate data, custom recommendation algorithms, and professional data visualizations using Plotly and Streamlit.

[![Live Demo](https://img.shields.io/badge/Live-Demo-success)](http://99.81.223.163:8504/) <--Click Here to Test the App

---

## ✨ Features

### 🎯 Smart Recommendations
- **Personalized Scoring Algorithm**: Customizes recommendations based on your temperature preferences, budget, crowd tolerance, and priorities
- **40+ Global Destinations**: Coverage across all 6 continents with diverse climates and travel experiences
- **Month-by-Month Analysis**: Detailed breakdown of weather, crowds, and costs for every month

### 🤖 AI-Powered Insights
- **Natural Language Summaries**: GPT-4o-mini generates conversational travel advice
- **Context-Aware Recommendations**: AI considers your preferences and trade-offs
- **Insider Tips**: Get personalized suggestions based on your travel style

### 📊 Data Visualization
- **Interactive Charts**: Weather trends, rainfall patterns, and score comparisons
- **Professional UI**: Modern gradient design with responsive layout
- **Real-Time Updates**: Dynamic recommendations as you adjust preferences

### 🌐 Comprehensive Data Sources
- **Weather Data**: Historical climate from [Open-Meteo API](https://open-meteo.com/)
- **Tourism Patterns**: Seasonal tourism indices and crowd data
- **Cost Analysis**: Accommodation pricing and seasonal demand trends

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key (optional, for AI summaries)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/passportpowell/travel-climate-analyzer.git
cd travel-climate-analyzer
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (optional)
```bash
# Create .env file
echo OPENAI_API_KEY=your-api-key-here > .env
```

5. **Generate dataset**
```bash
python data_collector.py
```

6. **Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
travel-climate-analyzer/
│
├── app.py                      # Main Streamlit application
├── data_collector.py           # Weather data fetching script
├── scoring.py                  # Recommendation algorithm
├── requirements.txt            # Python dependencies
├── .env                        # API keys (not in repo)
│
├── data/
│   ├── cities.json            # City coordinates & metadata
│   └── processed_data.csv     # Generated weather dataset
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py             # Utility functions
│   └── llm_summaries.py       # AI integration (OpenAI)
│
└── README.md                  # You are here!
```

---

## 🎨 Technologies Used

### Core Stack
- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[Python 3.11](https://www.python.org/)**: Programming language
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation
- **[Plotly](https://plotly.com/)**: Interactive visualizations

### APIs & Services
- **[Open-Meteo API](https://open-meteo.com/)**: Historical weather data
- **[OpenAI GPT-4o-mini](https://openai.com/)**: AI-powered summaries (optional)

### Additional Libraries
- `requests`: HTTP library for API calls
- `python-dotenv`: Environment variable management
- `numpy`: Numerical computing

---

## 🌟 How It Works

### 1. Data Collection
The `data_collector.py` script fetches historical climate data from Open-Meteo API for all 40 cities, including:
- Average temperature (°C)
- Rainfall (mm)
- Humidity levels
- Monthly patterns

### 2. Scoring Algorithm
The `scoring.py` module calculates a travel score (0-10) based on:
- **Temperature Match**: How close actual temps are to your preference
- **Rain Tolerance**: Penalty for rainfall based on your tolerance
- **Crowd Factor**: Tourist density during peak vs off-peak seasons
- **Cost Optimization**: Budget-friendly vs luxury preferences
- **Priority Weighting**: Emphasizes what matters most to you

### 3. AI Enhancement (Optional)
When OpenAI API key is provided:
- Analyzes top 3 recommended months
- Generates natural language summaries
- Provides contextual insights and trade-offs
- Offers personalized tips based on preferences

---

## 🗺️ Supported Destinations

### 🌍 Europe (17)
Barcelona, Paris, Rome, Amsterdam, Lisbon, London, Berlin, Vienna, Prague, Athens, Istanbul, Stockholm, Copenhagen, Oslo, Dublin, Edinburgh, Reykjavik

### 🌏 Asia (9)
Tokyo, Bangkok, Singapore, Seoul, Hong Kong, Mumbai, Dubai, Kuala Lumpur, Bali

### 🌎 North America (5)
New York, Los Angeles, Toronto, Vancouver, Mexico City

### 🌎 South America (5)
Rio de Janeiro, Buenos Aires, Lima, Santiago, Bogotá

### 🌍 Africa (3)
Cape Town, Cairo, Marrakech

### 🌏 Oceania (1)
Sydney

---

## 🎯 Use Cases

- **Vacation Planning**: Find the best time for your next trip
- **Event Scheduling**: Plan conferences or weddings in ideal weather
- **Budget Travel**: Discover off-peak seasons for better deals
- **Digital Nomads**: Compare multiple cities for long-term stays
- **Photography**: Identify optimal lighting and weather conditions

---

## 🔧 Configuration

### Adding New Cities
Edit `data/cities.json`:
```json
{
  "name": "New City",
  "country": "Country",
  "latitude": 0.0,
  "longitude": 0.0,
  "tourist_peak_months": [6, 7, 8],
  "cost_index": 7.0
}
```

Then regenerate data:
```bash
python data_collector.py
```

### Customizing Scoring
Modify weights in `scoring.py`:
```python
# Example: Emphasize weather over crowds
temp_score_weight = 0.5  # Default: 0.4
crowd_score_weight = 0.2  # Default: 0.3
```

---

## 📊 Sample Output

**For Bali, Indonesia (April):**
- 🌡️ Temperature: 28°C
- 🌧️ Rainfall: 134mm
- 👥 Crowds: Low (4/10)
- 💰 Cost: Budget-friendly (5/10)
- ⭐ **Score: 8.3/10**

**AI Summary:**
> "April offers an excellent balance for visiting Bali, just as the wet season tapers off. While you'll encounter some afternoon showers (averaging 134mm), the lush greenery and lower tourist crowds make it worthwhile. Accommodation prices drop significantly compared to peak season in July-August, making it a sweet spot for budget-conscious travelers seeking authentic experiences without the masses."

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Ideas for Contributions
- Add more cities/destinations
- Implement additional data sources (flight prices, events)
- Enhance scoring algorithm
- Add multi-city comparison feature
- Create mobile-responsive design improvements
- Add user authentication and saved preferences

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Open-Meteo**: For providing free, high-quality weather data
- **Streamlit**: For the incredible app framework
- **OpenAI**: For powering intelligent summaries
- **Community**: All contributors and users of TravelTiming

---

## 📧 Contact

**Otis Powell**
- GitHub: [@passportpowell](https://github.com/passportpowell)
- LinkedIn: [linkedin.com/in/otispowell](https://www.linkedin.com/in/otispowell/)

**Project Link**: https://github.com/passportpowell/travel-climate-analyzer

---

## 🌟 Show Your Support

If this project helped you plan your trip, please ⭐ **star this repository** and share it with fellow travelers!

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/passportpowell">Otis Powell</a></sub>
</div>
