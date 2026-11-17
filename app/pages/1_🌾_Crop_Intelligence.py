"""
AgriAI - Module 2: Crop Intelligence
SaaS-style multi-year crop production, area cultivation, and harvest yield analytics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="Crop Intelligence | AgriAI", page_icon="🌾", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Andhra Pradesh")

render_page_header(
    title="Crop Intelligence & Production Analytics",
    subtitle="Multi-decade empirical analysis of cultivated acreage, gross harvest production, and yield efficiencies across Andhra Pradesh.",
    category_tag="AGRONOMIC PRODUCTION INTELLIGENCE",
)

# Fetch crop data
crop_records = api_client.get_crop_production()
if not crop_records:
    st.warning("No crop production data available from backend services.")
    st.stop()

df = pd.DataFrame(crop_records)

# SaaS Card: Interactive Query Filters
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🔍 Advanced Filters</h4>", unsafe_allow_html=True)
col_f1, col_f2, col_f3, col_f4 = st.columns(4)

with col_f1:
    districts = ["All"] + sorted(df["district_name"].unique().tolist())
    selected_district = st.selectbox("Select District", districts)
with col_f2:
    crops = ["All"] + sorted(df["crop"].unique().tolist())
    selected_crop = st.selectbox("Select Crop", crops)
with col_f3:
    seasons = ["All"] + sorted(df["season"].unique().tolist())
    selected_season = st.selectbox("Select Season", seasons)
with col_f4:
    min_year = int(df["crop_year"].min())
    max_year = int(df["crop_year"].max())
    selected_years = st.slider("Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))
st.markdown('</div>', unsafe_allow_html=True)

# Apply Filters
filtered_df = df.copy()
if selected_district != "All":
    filtered_df = filtered_df[filtered_df["district_name"] == selected_district]
if selected_crop != "All":
    filtered_df = filtered_df[filtered_df["crop"] == selected_crop]
if selected_season != "All":
    filtered_df = filtered_df[filtered_df["season"] == selected_season]
filtered_df = filtered_df[
    (filtered_df["crop_year"] >= selected_years[0]) & (filtered_df["crop_year"] <= selected_years[1])
]

# Summary KPI Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-green">📊</div>
            <div class="kpi-content">
                <span class="kpi-label">Filtered Records</span>
                <span class="kpi-value">{len(filtered_df):,}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-emerald">🚜</div>
            <div class="kpi-content">
                <span class="kpi-label">Total Cultivated Area</span>
                <span class="kpi-value">{filtered_df['area_hectares'].sum():,.0f} Ha</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-gold">🌾</div>
            <div class="kpi-content">
                <span class="kpi-label">Gross Production</span>
                <span class="kpi-value">{filtered_df['production_tonnes'].sum() / 1000.0:,.1f}K T</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c4:
    avg_yield = filtered_df["yield_quintal_per_ha"].mean() if not filtered_df.empty else 0.0
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-sky">⚖️</div>
            <div class="kpi-content">
                <span class="kpi-label">Average Yield</span>
                <span class="kpi-value">{avg_yield:.2f} Q/Ha</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Charts Section
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown(
        """
        <div class="saas-card">
            <h4 style="margin-top:0; color:#0f172a; font-weight:700;">📈 Annual Production Trajectory</h4>
        """,
        unsafe_allow_html=True,
    )
    trend_df = filtered_df.groupby(["crop_year", "crop"])["production_tonnes"].sum().reset_index()
    trend_df["Prod_K"] = trend_df["production_tonnes"] / 1000.0
    fig_trend = px.line(
        trend_df,
        x="crop_year",
        y="Prod_K",
        color="crop",
        markers=True,
        color_discrete_sequence=["#16a34a", "#eab308", "#3b82f6", "#ef4444", "#8b5cf6"],
    )
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        xaxis=dict(title="", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="'000 Tonnes", showgrid=True, gridcolor="#f1f5f9"),
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart2:
    st.markdown(
        """
        <div class="saas-card">
            <h4 style="margin-top:0; color:#0f172a; font-weight:700;">🌱 Area vs. Harvest Production</h4>
        """,
        unsafe_allow_html=True,
    )
    fig_scatter = px.scatter(
        filtered_df,
        x="area_hectares",
        y="production_tonnes",
        color="crop",
        size="yield_quintal_per_ha",
        hover_data=["district_name", "crop_year"],
        color_discrete_sequence=["#16a34a", "#eab308", "#3b82f6", "#ef4444", "#8b5cf6"],
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        xaxis=dict(title="Cultivated Area (Ha)", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Production (Tonnes)", showgrid=True, gridcolor="#f1f5f9"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# District-wise Comparison
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🗺️ District-wise Yield Comparison (Quintals/Hectare)</h4>", unsafe_allow_html=True)
fig_bar = px.bar(
    filtered_df,
    x="district_name",
    y="yield_quintal_per_ha",
    color="crop",
    barmode="group",
    color_discrete_sequence=["#16a34a", "#eab308", "#3b82f6", "#ef4444", "#8b5cf6"],
)
fig_bar.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=30),
    height=320,
    xaxis=dict(title="", tickangle=-25),
    yaxis=dict(title="Yield (Q/Ha)", showgrid=True, gridcolor="#f1f5f9"),
)
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Data Table & Export
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📋 Filtered Records Dataset</h4>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, height=260)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Crop Production Dataset (CSV)",
    data=csv_data,
    file_name=f"crop_intelligence_{selected_district}_{selected_crop}.csv",
    mime="text/csv",
)
st.markdown('</div>', unsafe_allow_html=True)

render_disclaimer(
    "Data ingested from the Directorate of Economics and Statistics (DES) & Open Government Data (data.gov.in) portal."
)
