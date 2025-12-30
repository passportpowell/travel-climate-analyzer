import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scoring import calculate_best_time_score, get_best_months
from utils.llm_summaries import generate_travel_summary, get_openai_client
import json
import os

# Page config
st.set_page_config(
    page_title="TravelTiming - Smart Travel Planning",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.35em 0.65em;
        font-size: 0.85em;
        font-weight: 600;
        line-height: 1;
        color: #fff;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.375rem;
        margin: 0.2rem;
    }
    .badge-success { background-color: #28a745; }
    .badge-warning { background-color: #ffc107; color: #000; }
    .badge-danger { background-color: #dc3545; }
    .badge-info { background-color: #17a2b8; }
    
    /* GitHub badge */
    .github-badge {
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 999;
        background: #24292e;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    .github-badge:hover {
        background: #000;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Check if OpenAI is available
openai_available = get_openai_client() is not None

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/processed_data.csv')
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run data_collector.py first to generate the dataset.")
        st.stop()

df = load_data()

# GitHub Badge
st.markdown("""
<a href="https://github.com/passportpowell/AI-Travel-Planner-with-LLM-Integration-Interactive-Data-Visualizations" target="_blank" class="github-badge">
    ⭐ Star on GitHub
</a>
""", unsafe_allow_html=True)

# Professional Header
st.markdown("""
<div class="main-header">
    <h1>🌍 TravelTiming</h1>
    <p>Smart Travel Planning with AI-Powered Insights</p>
</div>
""", unsafe_allow_html=True)

# Features banner
col_feat1, col_feat2, col_feat3, col_feat4 = st.columns(4)
with col_feat1:
    st.markdown("**🌤️ Weather Data**")
    st.caption("Historical climate analysis")
with col_feat2:
    st.markdown("**👥 Crowd Insights**")
    st.caption("Tourism pattern tracking")
with col_feat3:
    st.markdown("**💰 Cost Analysis**")
    st.caption("Budget optimization")
with col_feat4:
    if openai_available:
        st.markdown("**✨ AI Advisor**")
        st.caption("Personalized recommendations")
    else:
        st.markdown("**📊 Data-Driven**")
        st.caption("Algorithm-based scoring")

st.markdown("---")

if not openai_available:
    st.info("💡 **Pro Tip:** Add an OpenAI API key to `.env` to unlock AI-powered travel summaries!")

# Sidebar - City Selection and Preferences
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <h2 style='color: #667eea; margin: 0;'>🎯 Your Preferences</h2>
    <p style='color: #666; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Customize your travel criteria</p>
</div>
""", unsafe_allow_html=True)

# City selector
cities = sorted(df['city'].unique())
selected_city = st.sidebar.selectbox("Select City", cities)

# Get country for the city
selected_country = df[df['city'] == selected_city]['country'].iloc[0]

st.sidebar.markdown("---")
st.sidebar.subheader("Temperature Preference")
temp_range = st.sidebar.slider(
    "Preferred Temperature Range (°C)",
    min_value=-10,
    max_value=40,
    value=(15, 28)
)

st.sidebar.markdown("---")
st.sidebar.subheader("Other Preferences")

rain_tolerance = st.sidebar.select_slider(
    "Rain Tolerance",
    options=['low', 'medium', 'high'],
    value='medium',
    help="Low = want dry weather, High = don't mind rain"
)

crowd_tolerance = st.sidebar.selectbox(
    "Crowd Preference",
    ['avoid', 'neutral', 'enjoy'],
    index=0,
    help="How do you feel about tourist crowds?"
)

budget_level = st.sidebar.selectbox(
    "Budget Level",
    ['budget', 'mid', 'luxury'],
    index=1
)

priority = st.sidebar.selectbox(
    "What matters most?",
    ['balanced', 'weather', 'avoid_crowds', 'budget'],
    index=0
)

# Create preferences dict
preferences = {
    'temp_min': temp_range[0],
    'temp_max': temp_range[1],
    'rain_tolerance': rain_tolerance,
    'crowd_tolerance': crowd_tolerance,
    'budget_level': budget_level,
    'priority': priority
}

# Calculate scores
city_data = df[df['city'] == selected_city].copy()
city_data['score'] = city_data.apply(
    lambda row: calculate_best_time_score(row, preferences),
    axis=1
)

# Get best months
best_months_df = get_best_months(df, selected_city, preferences, top_n=3)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # City header with styling
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
        <h2 style='color: white; margin: 0; font-size: 2rem;'>📍 {selected_city}, {selected_country}</h2>
        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>Personalized recommendations based on your preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI-Generated Summary (if available)
    if openai_available:
        with st.spinner("✨ Generating personalized travel insights..."):
            ai_summary = generate_travel_summary(
                selected_city, 
                selected_country,
                best_months_df, 
                preferences
            )
            
            if ai_summary:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                    <h3 style='color: white; margin: 0;'>🤖 AI Travel Advisor</h3>
                </div>
                """, unsafe_allow_html=True)
                st.info(ai_summary)
                st.markdown("---")
    
    # Best months recommendation with enhanced cards
    st.markdown("""
    <div style='background: #e8f5e9; padding: 1rem; border-radius: 8px; border-left: 4px solid #4caf50; margin-bottom: 1rem;'>
        <h3 style='margin: 0; color: #2e7d32;'>🎯 Top Recommended Months</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for idx, row in best_months_df.iterrows():
        # Determine badge colors
        score_color = "#4caf50" if row['score'] >= 8 else "#ff9800" if row['score'] >= 6 else "#f44336"
        crowd_level = 'High' if row['tourist_index'] > 7 else 'Medium' if row['tourist_index'] > 5 else 'Low'
        crowd_badge = "badge-danger" if row['tourist_index'] > 7 else "badge-warning" if row['tourist_index'] > 5 else "badge-success"
        cost_level = 'High' if row['cost_index'] > 7 else 'Medium' if row['cost_index'] > 5 else 'Budget'
        cost_badge = "badge-danger" if row['cost_index'] > 7 else "badge-warning" if row['cost_index'] > 5 else "badge-success"
        
        with st.expander(f"**{row['month_name']}** • Score: {row['score']}/10", expanded=(idx==0)):
            st.markdown(f"""
            <div style='background: linear-gradient(to right, {score_color}15, transparent); 
                        padding: 1rem; border-radius: 6px; border-left: 3px solid {score_color};'>
            """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                **🌡️ Temperature:** {row['avg_temp_c']}°C  
                **🌧️ Rainfall:** {row['rainfall_mm']}mm
                """)
            with col_b:
                st.markdown(f"""
                **👥 Crowds:** <span class='badge {crowd_badge}'>{crowd_level}</span>  
                **💰 Cost:** <span class='badge {cost_badge}'>{cost_level}</span>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Month-by-month breakdown
    st.subheader("📊 Month-by-Month Analysis")
    
    # Temperature and Rainfall chart with professional styling
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=city_data['month_name'],
        y=city_data['avg_temp_c'],
        name='Temperature (°C)',
        line=dict(color='#667eea', width=3, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)',
        yaxis='y'
    ))
    
    fig.add_trace(go.Bar(
        x=city_data['month_name'],
        y=city_data['rainfall_mm'],
        name='Rainfall (mm)',
        marker_color='#4ECDC4',
        yaxis='y2',
        opacity=0.7
    ))
    
    fig.update_layout(
        title=dict(text="<b>Weather Overview</b>", font=dict(size=20)),
        xaxis_title="<b>Month</b>",
        yaxis=dict(title="<b>Temperature (°C)</b>", side='left', gridcolor='rgba(0,0,0,0.1)'),
        yaxis2=dict(title="<b>Rainfall (mm)</b>", overlaying='y', side='right', gridcolor='rgba(0,0,0,0.05)'),
        hovermode='x unified',
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif"),
        margin=dict(t=60, b=40, l=60, r=60)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Overall score chart with enhanced styling
    fig2 = px.bar(
        city_data,
        x='month_name',
        y='score',
        title="<b>Best Time Score by Month</b>",
        labels={'score': 'Score (0-10)', 'month_name': 'Month'},
        color='score',
        color_continuous_scale=[
            [0, '#f44336'],
            [0.5, '#ff9800'], 
            [0.7, '#ffc107'],
            [0.85, '#8bc34a'],
            [1, '#4caf50']
        ],
        text='score'
    )
    
    fig2.update_traces(
        texttemplate='%{text:.1f}',
        textposition='outside',
        textfont=dict(size=12, color='black', family='Arial, sans-serif')
    )
    
    fig2.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)', range=[0, 10.5]),
        font=dict(family="Arial, sans-serif"),
        showlegend=True,
        title=dict(font=dict(size=20)),
        margin=dict(t=60, b=40, l=60, r=60)
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
        <h3 style='color: white; margin: 0;'>📈 Quick Stats</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display key metrics with icons
    avg_temp = city_data['avg_temp_c'].mean()
    total_rain = city_data['rainfall_mm'].sum()
    avg_crowd = city_data['tourist_index'].mean()
    avg_cost = city_data['cost_index'].mean()
    best_score = city_data['score'].max()
    
    st.metric("🌡️ Avg Temperature", f"{avg_temp:.1f}°C", delta=None)
    st.metric("🌧️ Annual Rainfall", f"{total_rain:.0f}mm", delta=None)
    st.metric("👥 Avg Crowd Level", f"{avg_crowd:.1f}/10", delta=None)
    st.metric("💰 Cost Index", f"{avg_cost:.1f}/10", delta=None)
    st.metric("⭐ Best Month Score", f"{best_score:.1f}/10", delta=None)
    
    st.markdown("---")
    
    # Detailed monthly table
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
        <h3 style='color: white; margin: 0;'>📋 Detailed Breakdown</h3>
    </div>
    """, unsafe_allow_html=True)
    
    display_df = city_data[['month_name', 'avg_temp_c', 'rainfall_mm', 'tourist_index', 'cost_index', 'score']].copy()
    display_df.columns = ['Month', 'Temp (°C)', 'Rain (mm)', 'Crowds', 'Cost', 'Score']
    display_df = display_df.sort_values('Score', ascending=False)
    
    # Format numbers for better display
    display_df['Temp (°C)'] = display_df['Temp (°C)'].round(1)
    display_df['Rain (mm)'] = display_df['Rain (mm)'].round(0).astype(int)
    display_df['Crowds'] = display_df['Crowds'].round(1)
    display_df['Cost'] = display_df['Cost'].round(1)
    display_df['Score'] = display_df['Score'].round(1)
    
    st.dataframe(
        display_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score",
                format="%.1f",
                min_value=0,
                max_value=10,
            ),
        }
    )

# Footer
st.markdown("---")
if openai_available:
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.9em;'>
        <p><strong>Data Sources:</strong></p>
        <p>
            🌤️ Weather Data: <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a> (Historical Climate Data)<br>
            👥 Tourism Patterns: Based on seasonal tourism indices and regional data<br>
            💰 Cost Indices: Derived from accommodation pricing trends and seasonal demand
        </p>
        <p>✨ AI summaries powered by <a href="https://platform.openai.com/" target="_blank">OpenAI GPT-4o-mini</a></p>
        <p>Built with <a href="https://streamlit.io/" target="_blank">Streamlit</a> 🎈 | Open Source Project</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.9em;'>
        <p><strong>Data Sources:</strong></p>
        <p>
            🌤️ Weather Data: <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a> (Historical Climate Data)<br>
            👥 Tourism Patterns: Based on seasonal tourism indices and regional data<br>
            💰 Cost Indices: Derived from accommodation pricing trends and seasonal demand
        </p>
        <p>Built with <a href="https://streamlit.io/" target="_blank">Streamlit</a> 🎈 | Open Source Project</p>
    </div>
    """, unsafe_allow_html=True)