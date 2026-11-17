"""
AgriAI - Module 6: Crop Yield Prediction
Machine learning driven crop yield estimation with TreeSHAP explainability.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="Yield Prediction | AgriAI", page_icon="📈", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Guntur")

render_page_header(
    title="Crop Yield Prediction & Explainability",
    subtitle="Machine-learning inference estimating harvest yield (Quintals/Hectare) and total production using environmental, meteorological, and soil features.",
    category_tag="PREDICTIVE MACHINE LEARNING",
)

st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📝 Farm & Environmental Feature Inputs</h4>", unsafe_allow_html=True)

with st.form("yield_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox("District", [
            "Guntur", "Krishna", "Kurnool", "Anantapur", "East Godavari",
            "Chittoor", "Prakasam", "West Godavari", "Visakhapatnam", "Nellore"
        ])
        crop = st.selectbox("Target Crop", [
            "Paddy (Rice)", "Cotton", "Chillies", "Groundnut", "Maize", "Bengal Gram", "Sugarcane"
        ])
        season = st.selectbox("Agricultural Season", ["Kharif", "Rabi", "Summer", "Whole Year"])
        area_ha = st.number_input("Cultivated Area (Hectares)", min_value=0.5, max_value=500.0, value=5.0, step=0.5)

    with col2:
        crop_year = st.number_input("Target Harvest Year", min_value=2024, max_value=2030, value=2024)
        rainfall = st.number_input("Seasonal Rainfall (mm)", min_value=200.0, max_value=2500.0, value=850.0, step=25.0)
        temp_avg = st.number_input("Mean Ambient Temperature (°C)", min_value=15.0, max_value=45.0, value=29.0, step=0.5)

    with col3:
        soil_ph = st.slider("Soil pH Value", min_value=4.0, max_value=9.5, value=7.2, step=0.1)
        nitrogen = st.number_input("Available Nitrogen (kg/ha)", min_value=50.0, max_value=600.0, value=310.0, step=10.0)
        phosphorus = st.number_input("Available Phosphorus (kg/ha)", min_value=5.0, max_value=80.0, value=22.0, step=2.0)
        potassium = st.number_input("Available Potassium (kg/ha)", min_value=50.0, max_value=500.0, value=190.0, step=10.0)

    submit_btn = st.form_submit_button("Compute Yield Prediction & SHAP Analysis", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

if submit_btn:
    with st.spinner("Executing trained ensemble regression pipeline and calculating TreeSHAP feature attributions..."):
        payload = {
            "state": "Andhra Pradesh",
            "district": district,
            "crop": crop,
            "season": season,
            "crop_year": int(crop_year),
            "area_hectares": float(area_ha),
            "rainfall_mm": float(rainfall),
            "temp_avg_c": float(temp_avg),
            "soil_ph": float(soil_ph),
            "nitrogen_kg_ha": float(nitrogen),
            "phosphorus_kg_ha": float(phosphorus),
            "potassium_kg_ha": float(potassium),
        }
        res = api_client.predict_yield(payload)

        if "error" in res:
            st.error(f"Inference error: {res['error']}")
        else:
            pred_yield = res.get("predicted_yield_quintal_per_ha", 0.0)
            tot_prod = res.get("estimated_total_production_tonnes", 0.0)
            ci = res.get("prediction_confidence_interval", {})

            # Result KPI Cards
            res_col1, res_col2, res_col3 = st.columns(3)
            with res_col1:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-icon-circle kpi-icon-green">🌾</div>
                        <div class="kpi-content">
                            <span class="kpi-label">Predicted Yield</span>
                            <span class="kpi-value">{pred_yield:.2f} Q/Ha</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with res_col2:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-icon-circle kpi-icon-emerald">⚖️</div>
                        <div class="kpi-content">
                            <span class="kpi-label">Estimated Production</span>
                            <span class="kpi-value">{tot_prod:.2f} T</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with res_col3:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-icon-circle kpi-icon-gold">🎯</div>
                        <div class="kpi-content">
                            <span class="kpi-label">95% Confidence Band</span>
                            <span class="kpi-value" style="font-size:1.15rem;">
                                {ci.get('lower_bound_quintals', 0):.1f} - {ci.get('upper_bound_quintals', 0):.1f}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            # SHAP Explanation Card
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#0f172a; font-weight:700;">📊 TreeSHAP Feature Attribution Breakdown</h4>
                    <span style="font-size:0.8rem; background:#f1f5f9; padding:4px 10px; border-radius:12px; font-weight:600;">
                        Model: {res.get('model_algorithm')}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            importance = res.get("feature_importance", {})
            if importance:
                df_imp = pd.DataFrame(list(importance.items()), columns=["Feature", "Attribution Weight"])
                df_imp = df_imp.sort_values(by="Attribution Weight", ascending=True)

                fig_shap = px.bar(
                    df_imp,
                    x="Attribution Weight",
                    y="Feature",
                    orientation="h",
                    color="Attribution Weight",
                    color_continuous_scale=["#bbf7d0", "#22c55e", "#15803d"],
                )
                fig_shap.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=260,
                    xaxis=dict(title="Relative Contribution", showgrid=True, gridcolor="#f1f5f9"),
                    yaxis=dict(title=""),
                    coloraxis_showscale=False,
                )
                st.plotly_chart(fig_shap, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            render_disclaimer(res.get("disclaimer", ""))
