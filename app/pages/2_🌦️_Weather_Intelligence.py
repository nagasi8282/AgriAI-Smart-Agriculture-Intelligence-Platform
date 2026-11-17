"""
AgriAI - Module 3: Weather Intelligence
Meteorological monitoring, rainfall distribution, and agro-climatic indicators.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header, render_weather_widget
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="Weather Intelligence | AgriAI", page_icon="🌦️", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Guntur")

render_page_header(
    title="Weather Intelligence & Agro-Climatology",
    subtitle="District-level meteorological time-series, rainfall anomalies, ambient temperature shifts, and humidity monitoring for Andhra Pradesh.",
    category_tag="METEOROLOGICAL & CLIMATE ANALYTICS",
)

# Fetch weather data
records = api_client.get_weather()
if not records:
    st.warning("No meteorological records available. Verify backend services.")
    st.stop()

df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date"])

# Filter
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
districts = ["All"] + sorted(df["district"].unique().tolist())
selected_district = st.selectbox("Select District for Meteorological Focus", districts, index=1 if len(districts) > 1 else 0)
st.markdown('</div>', unsafe_allow_html=True)

filtered_df = df.copy()
if selected_district != "All":
    filtered_df = filtered_df[filtered_df["district"] == selected_district]

# Top KPI Metric Cards
w1, w2, w3, w4 = st.columns(4)
max_t = filtered_df["temp_max_c"].max() if not filtered_df.empty else 0.0
min_t = filtered_df["temp_min_c"].min() if not filtered_df.empty else 0.0
tot_rain = filtered_df["rainfall_mm"].sum() if not filtered_df.empty else 0.0
avg_hum = filtered_df["relative_humidity_pct"].mean() if not filtered_df.empty else 0.0

with w1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-gold">🔥</div>
            <div class="kpi-content">
                <span class="kpi-label">Highest Recorded Temp</span>
                <span class="kpi-value">{max_t:.1f}°C</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with w2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-sky">❄️</div>
            <div class="kpi-content">
                <span class="kpi-label">Lowest Recorded Temp</span>
                <span class="kpi-value">{min_t:.1f}°C</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with w3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-green">🌧️</div>
            <div class="kpi-content">
                <span class="kpi-label">Cumulative Rainfall</span>
                <span class="kpi-value">{tot_rain:.1f} mm</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with w4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-emerald">💧</div>
            <div class="kpi-content">
                <span class="kpi-label">Avg Relative Humidity</span>
                <span class="kpi-value">{avg_hum:.1f}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Main Grid
col_w_left, col_w_right = st.columns([1.5, 1])

with col_w_left:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🌡️ Temperature Fluctuations ({selected_district})</h4>", unsafe_allow_html=True)
    fig_temp = px.line(
        filtered_df,
        x="date",
        y=["temp_max_c", "temp_min_c", "temp_mean_c"],
        color_discrete_map={"temp_max_c": "#ef4444", "temp_min_c": "#3b82f6", "temp_mean_c": "#10b981"},
    )
    fig_temp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        xaxis=dict(title="", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Temperature (°C)", showgrid=True, gridcolor="#f1f5f9"),
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center", title=""),
    )
    st.plotly_chart(fig_temp, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_w_right:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🌦️ 5-Day Numerical Forecast</h4>", unsafe_allow_html=True)
    render_weather_widget(
        district=selected_district if selected_district != "All" else "Guntur",
        temp_c=float(filtered_df["temp_mean_c"].mean()) if not filtered_df.empty else 32.0,
        condition="Partly Cloudy",
        humidity=avg_hum,
        wind=14.0,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Rainfall Chart
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown(f"<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🌧️ Daily Rainfall Distribution ({selected_district})</h4>", unsafe_allow_html=True)
fig_rain = px.bar(
    filtered_df,
    x="date",
    y="rainfall_mm",
    color="rainfall_mm",
    color_continuous_scale=["#bfdbfe", "#3b82f6", "#1d4ed8"],
)
fig_rain.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=260,
    xaxis=dict(title="", showgrid=True, gridcolor="#f1f5f9"),
    yaxis=dict(title="Precipitation (mm)", showgrid=True, gridcolor="#f1f5f9"),
    coloraxis_showscale=False,
)
st.plotly_chart(fig_rain, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Download
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📋 Meteorological Data Extract</h4>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, height=220)
st.download_button(
    "📥 Download Meteorological Records (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name=f"weather_intelligence_{selected_district}.csv",
    mime="text/csv",
)
st.markdown('</div>', unsafe_allow_html=True)

render_disclaimer(
    "Meteorological observations sourced from IMD gridded datasets and Open-Meteo archive APIs."
)
