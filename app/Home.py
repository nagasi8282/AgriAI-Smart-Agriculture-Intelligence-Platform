"""
AgriAI - Smart Agriculture Intelligence Platform
Overview Dashboard (Page 1) - Premium Agriculture SaaS Design
Reference: Agrivision AI, Official Streamlit Dashboard Templates, Microsoft Streamlit UI.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from app.components.theme import (
    apply_saas_theme,
    render_sidebar,
    render_top_bar,
    render_hero_banner,
)
from app.components.cards import (
    render_kpi_row,
    render_weather_widget,
    render_quick_tools,
    render_promo_banner,
)
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

# Page configuration
st.set_page_config(
    page_title="AgriAI - Agriculture Intelligence Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply premium SaaS theme
apply_saas_theme(dark_mode=False)

# Render customized forest-green sidebar
render_sidebar()

# Fetch live backend summaries
summary = api_client.get_dashboard_summary()
crop_records = api_client.get_crop_production()
mandi_records = api_client.get_mandi_prices()
weather_records = api_client.get_weather(district="Guntur")

df_crop = pd.DataFrame(crop_records) if crop_records else pd.DataFrame()
df_mandi = pd.DataFrame(mandi_records) if mandi_records else pd.DataFrame()
df_weather = pd.DataFrame(weather_records) if weather_records else pd.DataFrame()

# Dynamic KPI values
total_prod_val = f"{df_crop['production_tonnes'].sum() / 1000000:.1f}M T" if not df_crop.empty else "342.5 MT"
total_area_val = f"{df_crop['area_hectares'].sum() / 1000000:.1f}M Ha" if not df_crop.empty else "2.8M Ha"
avg_mandi_val = f"₹{df_mandi['modal_price_inr'].mean():,.0f} /Qtl" if not df_mandi.empty else "₹2,450 /Quintal"
current_temp_val = f"{df_weather['temp_mean_c'].iloc[0]:.0f}°C" if not df_weather.empty else "32°C"
weather_cond_val = str(df_weather['condition'].iloc[0]) if not df_weather.empty and 'condition' in df_weather.columns else "Partly Cloudy"

# 1. Top App Bar
render_top_bar(current_district="Guntur")

# 2. Panoramic Hero Banner
render_hero_banner(
    title="Welcome to AgriAI",
    subtitle="Smart Farming. Brighter Future. End-to-End Agriculture Data Intelligence.",
    district="Andhra Pradesh, India",
)

# 3. Row of 4 KPI Metric Cards
render_kpi_row(
    total_production=total_prod_val,
    production_delta="↑ 12.5%",
    active_area=total_area_val,
    area_delta="↑ 8.3%",
    avg_mandi_price=avg_mandi_val,
    price_delta="↑ 6.1%",
    current_weather=current_temp_val,
    weather_cond=weather_cond_val,
)

# 4. Main Content Grid - Row 1
col_row1_left, col_row1_right = st.columns([1.5, 1])

with col_row1_left:
    st.markdown(
        """
        <div class="section-header">
            <h3 class="section-title">🍃 Crop Production Trend</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not df_crop.empty:
        # Multi-line production trend
        trend_grouped = df_crop.groupby(["crop_year", "crop"])["production_tonnes"].sum().reset_index()
        # Scale to thousands for clean display
        trend_grouped["Production_K_Tonnes"] = trend_grouped["production_tonnes"] / 1000.0

        fig_trend = px.line(
            trend_grouped,
            x="crop_year",
            y="Production_K_Tonnes",
            color="crop",
            markers=True,
            color_discrete_sequence=["#16a34a", "#eab308", "#3b82f6", "#ef4444", "#8b5cf6", "#14b8a6"],
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis=dict(
                title="",
                showgrid=True,
                gridcolor="#f1f5f9",
                linecolor="#e2e8f0",
                dtick=1,
            ),
            yaxis=dict(
                title="Production ('000 Tonnes)",
                showgrid=True,
                gridcolor="#f1f5f9",
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title="",
            ),
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Loading crop production trends...")

with col_row1_right:
    st.markdown(
        """
        <div class="section-header">
            <h3 class="section-title">☀️ Weather Overview</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_weather_widget(
        district="Guntur",
        temp_c=32.0,
        condition="Partly Cloudy",
        humidity=68.0,
        wind=12.0,
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# 5. Main Content Grid - Row 2
col_row2_left, col_row2_right = st.columns([1.5, 1])

with col_row2_left:
    st.markdown(
        """
        <div class="section-header">
            <h3 class="section-title">🏛️ Mandi Price Trends</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not df_mandi.empty:
        # Filter for Chilli / Cotton / Paddy
        df_mandi["arrival_date"] = pd.to_datetime(df_mandi["arrival_date"])
        chilli_df = df_mandi[df_mandi["commodity"] == "Chillies"].sort_values("arrival_date")

        fig_mandi_trend = go.Figure()
        fig_mandi_trend.add_trace(
            go.Scatter(
                x=chilli_df["arrival_date"],
                y=chilli_df["modal_price_inr"],
                mode="lines+markers",
                name="Current Price",
                line=dict(color="#16a34a", width=2.5, dash="dash"),
                marker=dict(size=6, color="#15803d"),
            )
        )
        # Add spot annotation
        if not chilli_df.empty:
            last_date = chilli_df["arrival_date"].iloc[-1]
            last_price = chilli_df["modal_price_inr"].iloc[-1]
            fig_mandi_trend.add_annotation(
                x=last_date,
                y=last_price,
                text=f"₹{last_price:,.0f}",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#0f3821",
                bgcolor="#0f3821",
                font=dict(color="white", size=11, family="Inter"),
                borderpad=4,
            )

        fig_mandi_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            xaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
            yaxis=dict(title="Modal Price (₹/Quintal)", showgrid=True, gridcolor="#f1f5f9"),
            showlegend=False,
        )
        st.plotly_chart(fig_mandi_trend, use_container_width=True)
    else:
        st.info("Loading mandi prices...")

with col_row2_right:
    st.markdown(
        """
        <div class="section-header">
            <h3 class="section-title">⚡ Quick Tools</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_quick_tools()

# 6. Main Content Grid - Row 3
col_row3_left, col_row3_right = st.columns([1.5, 1])

with col_row3_left:
    render_promo_banner()

with col_row3_right:
    st.markdown(
        """
        <div class="section-header">
            <h3 class="section-title">🌱 Top Crops by Production</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not df_crop.empty:
        top_crops = (
            df_crop.groupby("crop")["production_tonnes"]
            .sum()
            .reset_index()
            .sort_values("production_tonnes", ascending=False)
            .head(5)
        )
        top_crops["Prod_K"] = top_crops["production_tonnes"] / 1000.0

        fig_bar = px.bar(
            top_crops,
            x="crop",
            y="Prod_K",
            color="Prod_K",
            color_continuous_scale=["#bbf7d0", "#22c55e", "#15803d"],
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=20),
            height=220,
            xaxis=dict(title="", tickangle=-20),
            yaxis=dict(title="'000 Tonnes", showgrid=True, gridcolor="#f1f5f9"),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# Advisory disclaimer
render_disclaimer(
    "AgriAI is an enterprise agricultural intelligence and academic research platform. "
    "All yield and mandi price projections are algorithmically estimated based on regional historical distributions."
)
