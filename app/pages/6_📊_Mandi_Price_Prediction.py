"""
AgriAI - Module 7: Mandi Price Prediction
Time-series aware regression model projecting commodity wholesale modal prices.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="Price Prediction | AgriAI", page_icon="📊", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Guntur")

render_page_header(
    title="Mandi Wholesale Price Forecasting",
    subtitle="Time-series aware regression projecting future modal commodity prices and volatility ranges across Andhra Pradesh APMC yards.",
    category_tag="TIME-SERIES COMMODITY FORECASTING",
)

st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📝 Market Forecast Parameters</h4>", unsafe_allow_html=True)

with st.form("price_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        commodity = st.selectbox("Select Commodity", ["Chillies", "Cotton", "Paddy", "Groundnut", "Maize", "Bengal Gram", "Sugarcane"])
    with col2:
        market = st.selectbox("Select APMC Market Yard", [
            "Guntur APMC", "Kurnool APMC", "Vijayawada Market", "Adoni Mandi", "Tirupati Mandi", "Rajahmundry Yard"
        ])
    with col3:
        horizon = st.slider("Forecast Horizon (Days Ahead)", min_value=1, max_value=30, value=7)

    predict_btn = st.form_submit_button("Generate Modal Price Forecast", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

if predict_btn:
    with st.spinner("Processing time-series lag features and generating price trajectory..."):
        payload = {
            "state": "Andhra Pradesh",
            "district": "Guntur" if "Guntur" in market else "Kurnool",
            "market": market,
            "commodity": commodity,
            "forecast_horizon_days": horizon,
        }
        res = api_client.predict_price(payload)

        if "error" in res:
            st.error(f"Prediction error: {res['error']}")
        else:
            curr_p = res.get("current_modal_price", 0.0)
            pred_p = res.get("predicted_modal_price", 0.0)
            chg_pct = res.get("price_change_pct", 0.0)

            # Results KPI Row
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-icon-circle kpi-icon-sky">🏷️</div>
                        <div class="kpi-content">
                            <span class="kpi-label">Current Spot Modal Price</span>
                            <span class="kpi-value">₹{curr_p:,.0f}</span>
                            <span style="font-size:0.75rem; color:#64748b;">per Quintal</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c2:
                trend_color = "#16a34a" if chg_pct >= 0 else "#ef4444"
                arrow = "↑" if chg_pct >= 0 else "↓"
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-icon-circle kpi-icon-gold">🔮</div>
                        <div class="kpi-content">
                            <span class="kpi-label">Projected Modal Price</span>
                            <span class="kpi-value">₹{pred_p:,.0f}</span>
                            <span style="font-size:0.78rem; color:{trend_color}; font-weight:700;">{arrow} {abs(chg_pct):.2f}% expected</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-icon-circle kpi-icon-green">📅</div>
                        <div class="kpi-content">
                            <span class="kpi-label">Forecast Horizon</span>
                            <span class="kpi-value">{horizon} Days</span>
                            <span style="font-size:0.75rem; color:#64748b;">Trained Model v{res.get('model_version', '1.0')}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            # Trajectory Chart Card
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📈 Projected Price Trajectory ({commodity} @ {market})</h4>", unsafe_allow_html=True)
            trend = res.get("historical_price_trend", [])
            if trend:
                df_trend = pd.DataFrame(trend)
                df_trend = pd.concat([
                    df_trend,
                    pd.DataFrame([{"day_offset": horizon, "price": pred_p}])
                ], ignore_index=True)

                fig = px.line(
                    df_trend,
                    x="day_offset",
                    y="price",
                    markers=True,
                    color_discrete_sequence=["#16a34a"],
                )
                fig.add_vline(x=0, line_dash="dash", line_color="#94a3b8", annotation_text="Today")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=280,
                    xaxis=dict(title="Day Offset from Today", showgrid=True, gridcolor="#f1f5f9"),
                    yaxis=dict(title="Modal Price (₹/Quintal)", showgrid=True, gridcolor="#f1f5f9"),
                )
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            render_disclaimer(res.get("disclaimer", ""))
