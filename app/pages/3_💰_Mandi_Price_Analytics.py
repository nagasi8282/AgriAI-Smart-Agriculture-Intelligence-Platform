"""
AgriAI - Module 4: Mandi Price Analytics
Wholesale commodity pricing, daily arrival volumes, and APMC yard comparisons.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="Mandi Price Analytics | AgriAI", page_icon="💰", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Guntur")

render_page_header(
    title="Mandi Price Analytics & Market Intelligence",
    subtitle="AGMARKNET daily wholesale commodity prices, arrival volumes, and price dispersion across Andhra Pradesh APMC yards.",
    category_tag="WHOLESALE MARKET INTELLIGENCE",
)

# Fetch data
mandi_records = api_client.get_mandi_prices()
if not mandi_records:
    st.warning("No mandi price records available from backend services.")
    st.stop()

df = pd.DataFrame(mandi_records)
df["arrival_date"] = pd.to_datetime(df["arrival_date"])

# Controls
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🔍 Market Filters</h4>", unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    districts = ["All"] + sorted(df["district"].unique().tolist())
    sel_dist = st.selectbox("Filter District", districts)
with col_f2:
    commodities = ["All"] + sorted(df["commodity"].unique().tolist())
    sel_comm = st.selectbox("Filter Commodity", commodities)
with col_f3:
    markets = ["All"] + sorted(df["market"].unique().tolist())
    sel_market = st.selectbox("Filter Market Yard", markets)
st.markdown('</div>', unsafe_allow_html=True)

filtered_df = df.copy()
if sel_dist != "All":
    filtered_df = filtered_df[filtered_df["district"] == sel_dist]
if sel_comm != "All":
    filtered_df = filtered_df[filtered_df["commodity"] == sel_comm]
if sel_market != "All":
    filtered_df = filtered_df[filtered_df["market"] == sel_market]

# Summary KPI Cards
m1, m2, m3, m4 = st.columns(4)
avg_modal = filtered_df["modal_price_inr"].mean() if not filtered_df.empty else 0.0
highest_price = filtered_df["max_price_inr"].max() if not filtered_df.empty else 0.0
lowest_price = filtered_df["min_price_inr"].min() if not filtered_df.empty else 0.0
tot_arrivals = filtered_df["arrival_tonnes"].sum() if not filtered_df.empty else 0.0

with m1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-green">₹</div>
            <div class="kpi-content">
                <span class="kpi-label">Average Modal Price</span>
                <span class="kpi-value">₹{avg_modal:,.0f}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-gold">📈</div>
            <div class="kpi-content">
                <span class="kpi-label">Highest Spot Price</span>
                <span class="kpi-value">₹{highest_price:,.0f}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-sky">📉</div>
            <div class="kpi-content">
                <span class="kpi-label">Lowest Spot Price</span>
                <span class="kpi-value">₹{lowest_price:,.0f}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with m4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon-circle kpi-icon-emerald">⚖️</div>
            <div class="kpi-content">
                <span class="kpi-label">Recorded Arrivals</span>
                <span class="kpi-value">{tot_arrivals:,.0f} T</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Charts Section
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📊 Modal Price Trajectory (₹/Quintal)</h4>", unsafe_allow_html=True)
    fig_price = px.line(
        filtered_df,
        x="arrival_date",
        y="modal_price_inr",
        color="commodity",
        color_discrete_sequence=["#16a34a", "#eab308", "#3b82f6", "#ef4444", "#8b5cf6"],
    )
    fig_price.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        xaxis=dict(title="", showgrid=True, gridcolor="#f1f5f9"),
        yaxis=dict(title="Price (₹/Qtl)", showgrid=True, gridcolor="#f1f5f9"),
    )
    st.plotly_chart(fig_price, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_c2:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🏷️ Trading Price Spread (Min - Modal - Max)</h4>", unsafe_allow_html=True)
    recent_records = filtered_df.drop_duplicates(subset=["market", "commodity"], keep="last")
    fig_spread = px.bar(
        recent_records,
        x="commodity",
        y=["min_price_inr", "modal_price_inr", "max_price_inr"],
        barmode="group",
        color_discrete_sequence=["#93c5fd", "#22c55e", "#f59e0b"],
    )
    fig_spread.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        xaxis=dict(title=""),
        yaxis=dict(title="Price (₹/Qtl)", showgrid=True, gridcolor="#f1f5f9"),
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center", title=""),
    )
    st.plotly_chart(fig_spread, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Market Comparison Boxplot
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🏛️ Cross-Market APMC Yard Price Dispersion</h4>", unsafe_allow_html=True)
fig_box = px.box(
    filtered_df,
    x="market",
    y="modal_price_inr",
    color="commodity",
    color_discrete_sequence=["#16a34a", "#eab308", "#3b82f6", "#ef4444"],
)
fig_box.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=30),
    height=300,
    xaxis=dict(title="", tickangle=-20),
    yaxis=dict(title="Modal Price (₹/Qtl)", showgrid=True, gridcolor="#f1f5f9"),
)
st.plotly_chart(fig_box, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Data Table & Export
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📋 Wholesale Price Feed</h4>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, height=240)
st.download_button(
    "📥 Download Mandi Price Records (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name=f"mandi_analytics_{sel_comm}.csv",
    mime="text/csv",
)
st.markdown('</div>', unsafe_allow_html=True)

render_disclaimer(
    "AGMARKNET prices reflect official wholesale transaction values at regulated APMC yards."
)
