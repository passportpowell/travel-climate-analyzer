# TravelTiming

Streamlit application for comparing travel timing across the destinations in `data/cities.json`. It combines historical climate observations, a preference-based scoring function, Plotly charts and optional OpenAI-generated summaries.

> **Project status:** source and local setup are available. A public demo has not been verified, so this repository does not claim a working hosted demo.

## What it does

- Fetches historical temperature and rainfall observations from the Open-Meteo Archive API.
- Scores months against temperature, rainfall, crowd and cost preferences using the documented rules in `scoring.py`.
- Shows monthly comparisons in a Streamlit interface.
- Optionally asks OpenAI `gpt-4o-mini` for a natural-language summary of the already calculated recommendations. The model does not calculate the scores.

## Data and limits

Weather values are historical observations, not a forecast. Crowd and cost indices are configured estimates in `data/cities.json`; they are not live visitor counts, prices or booking quotes. Results are planning aids and depend on those assumptions and the selected preferences.

## Run locally

Requires Python 3.11 or newer and internet access to fetch the weather data.

```powershell
git clone https://github.com/passportpowell/travel-climate-analyzer.git
cd travel-climate-analyzer
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python data_collector.py
streamlit run app.py
```

Open `http://localhost:8501`.

OpenAI summaries are optional. Without a key, the climate comparison and scoring features remain available. To enable summaries, set `OPENAI_API_KEY` in your local environment before starting the app. Do not commit API keys.

## Implementation

- `data_collector.py` fetches archive observations for configured destinations and writes `data/processed_data.csv`.
- `scoring.py` applies preference weights and configured crowd/cost indices.
- `app.py` renders the Streamlit interface and imports the optional language-model helpers.
- `utils/llm_summaries.py` contains the OpenAI summary calls.

## Stack

Python · Streamlit · Pandas · Plotly · Open-Meteo Archive API · OpenAI API (optional)

## Licence and acknowledgements

See [LICENSE](LICENSE). Weather data is provided by [Open-Meteo](https://open-meteo.com/).

## Links

- [Source repository](https://github.com/passportpowell/travel-climate-analyzer)
- [Otis Powell on GitHub](https://github.com/passportpowell)
- [LinkedIn](https://www.linkedin.com/in/otispowell/)
