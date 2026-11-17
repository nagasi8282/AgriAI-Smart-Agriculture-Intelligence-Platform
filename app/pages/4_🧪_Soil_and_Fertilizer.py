"""
AgriAI - Module 5: Soil and Fertilizer Intelligence
Comprehensive soil diagnostic, ML formulation recommendation, and ANGRAU/ICAR precision bag schedules.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="Soil & Fertilizer | AgriAI", page_icon="🧪", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Guntur")

render_page_header(
    title="Soil Health & Precision Fertilizer Advisory",
    subtitle="AI-driven nutrient deficit balancing, ML formulation selection, and ANGRAU-calibrated commercial product bag schedules.",
    category_tag="AGRONOMIC NUTRIENT MANAGEMENT",
)

# Fetch baseline soil profiles
soil_data = api_client.get_soil()
df_soil = pd.DataFrame(soil_data) if soil_data else pd.DataFrame()

tab1, tab2 = st.tabs(["🌱 Precision Fertilizer Generator", "🗺️ AP District Soil Profiles"])

with tab1:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📝 Farm & Soil Test Diagnostic Inputs</h4>", unsafe_allow_html=True)
    st.caption("Enter soil test laboratory results or Soil Health Card measurements for precision nutrient recommendation.")

    col_in1, col_in2, col_in3 = st.columns(3)

    with col_in1:
        district_list = sorted(df_soil["district"].unique().tolist()) if not df_soil.empty else [
            "Anantapur", "Chittoor", "East Godavari", "Guntur", "Kadapa", "Krishna", 
            "Kurnool", "Nellore", "Prakasam", "Srikakulam", "Visakhapatnam", "Vizianagaram", "West Godavari"
        ]
        crop_district = st.selectbox("Farm District", district_list, index=3)
        crop_name = st.selectbox(
            "Target Crop",
            ["Paddy (Rice)", "Cotton", "Chillies", "Groundnut", "Maize", "Bengal Gram", "Sugarcane"]
        )
        farm_acres = st.number_input("Farm Acreage (Acres)", min_value=0.25, max_value=250.0, value=2.5, step=0.5)

    with col_in2:
        nitrogen = st.number_input("Available Nitrogen (N) [kg/ha]", min_value=40.0, max_value=800.0, value=240.0, step=10.0, help="Soil Health Card available N (Standard: <280 Deficient, 280-560 Medium, >560 High)")
        phosphorus = st.number_input("Available Phosphorus (P) [kg/ha]", min_value=3.0, max_value=120.0, value=14.0, step=1.0, help="Available P2O5 (Standard: <10 Deficient, 10-25 Medium, >25 High)")
        potassium = st.number_input("Available Potassium (K) [kg/ha]", min_value=40.0, max_value=700.0, value=195.0, step=10.0, help="Available K2O (Standard: <108 Deficient, 108-280 Medium, >280 High)")

    with col_in3:
        soil_ph = st.slider("Soil pH Value", min_value=4.5, max_value=9.5, value=7.2, step=0.1, help="Neutral range: 6.5 - 7.5. Acidic < 6.0, Alkaline > 8.2")
        soil_type = st.selectbox("Predominant Soil Type", ["Black Cotton", "Coastal Alluvial", "Red Sandy Loam", "Laterite"])
        organic_carbon = st.slider("Soil Organic Carbon (OC %)", min_value=0.1, max_value=1.5, value=0.55, step=0.05, help="Standard: <0.5% Low, 0.5-0.75% Medium, >0.75% High")

    gen_btn = st.button("🔬 Formulate Precision Fertilizer Schedule", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if gen_btn:
        with st.spinner("Analyzing soil balance, running ML classifier, and computing bag dosages..."):
            payload = {
                "crop": crop_name,
                "district": crop_district,
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "soil_ph": soil_ph,
                "soil_type": soil_type,
                "farm_area_acres": farm_acres,
                "organic_carbon_pct": organic_carbon,
            }
            res = api_client.recommend_fertilizer(payload)

            if "error" in res:
                st.error(f"Error calculating fertilizer recommendation: {res['error']}")
            else:
                st.success("Agronomic Fertilizer Recommendation Generated Successfully!")

                # ML Formulation Hero Highlight Banner
                blend_name = res.get("recommended_blend", "Urea + DAP + MOP")
                confidence = res.get("ml_confidence_pct", 95.0)
                total_bags = res.get("total_50kg_bags", 0.0)
                hectares = res.get("farm_area_hectares", round(farm_acres * 0.404686, 2))

                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, #0d3821 0%, #15803d 100%); padding: 22px 28px; border-radius: 14px; color: white; margin-bottom: 24px; box-shadow: 0 4px 14px rgba(13,56,33,0.15);">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
                            <div>
                                <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; background:rgba(255,255,255,0.2); padding:4px 10px; border-radius:20px; font-weight:700;">AI FORMULATION SELECTION</span>
                                <h2 style="margin:8px 0 4px 0; color:#ffffff; font-size:1.6rem; font-weight:800;">{blend_name}</h2>
                                <p style="margin:0; opacity:0.9; font-size:0.95rem;">Optimized for {crop_name} across {farm_acres} Acres ({hectares} Hectares) in {soil_type} soil.</p>
                            </div>
                            <div style="display:flex; gap:20px; text-align:right;">
                                <div style="background:rgba(255,255,255,0.12); padding:10px 18px; border-radius:10px;">
                                    <div style="font-size:0.75rem; opacity:0.85;">ML CONFIDENCE</div>
                                    <div style="font-size:1.4rem; font-weight:800; color:#fde047;">{confidence:.1f}%</div>
                                </div>
                                <div style="background:rgba(255,255,255,0.12); padding:10px 18px; border-radius:10px;">
                                    <div style="font-size:0.75rem; opacity:0.85;">TOTAL 50KG BAGS</div>
                                    <div style="font-size:1.4rem; font-weight:800; color:#ffffff;">{total_bags} Bags</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Diagnostic Soil Status KPI Cards
                status = res.get("nutrient_status", {})
                n_stat = status.get("Nitrogen (N)", "N/A")
                p_stat = status.get("Phosphorus (P)", "N/A")
                k_stat = status.get("Potassium (K)", "N/A")

                # pH Diagnostic Tag
                if soil_ph < 6.0:
                    ph_tag = "Acidic (Lime Required)"
                    ph_color = "kpi-icon-gold"
                elif soil_ph > 8.2:
                    ph_tag = "Alkaline (Gypsum Required)"
                    ph_color = "kpi-icon-gold"
                else:
                    ph_tag = "Optimal (Neutral)"
                    ph_color = "kpi-icon-green"

                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.markdown(
                        f"""
                        <div class="kpi-card">
                            <div class="kpi-icon-circle kpi-icon-green">N</div>
                            <div class="kpi-content">
                                <span class="kpi-label">Available Nitrogen</span>
                                <span class="kpi-value" style="font-size:1.15rem;">{n_stat}</span>
                                <span style="font-size:0.75rem; color:#64748b;">Soil Test: {nitrogen} kg/ha</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with k2:
                    st.markdown(
                        f"""
                        <div class="kpi-card">
                            <div class="kpi-icon-circle kpi-icon-gold">P</div>
                            <div class="kpi-content">
                                <span class="kpi-label">Available Phosphorus</span>
                                <span class="kpi-value" style="font-size:1.15rem;">{p_stat}</span>
                                <span style="font-size:0.75rem; color:#64748b;">Soil Test: {phosphorus} kg/ha</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with k3:
                    st.markdown(
                        f"""
                        <div class="kpi-card">
                            <div class="kpi-icon-circle kpi-icon-sky">K</div>
                            <div class="kpi-content">
                                <span class="kpi-label">Available Potassium</span>
                                <span class="kpi-value" style="font-size:1.15rem;">{k_stat}</span>
                                <span style="font-size:0.75rem; color:#64748b;">Soil Test: {potassium} kg/ha</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with k4:
                    st.markdown(
                        f"""
                        <div class="kpi-card">
                            <div class="kpi-icon-circle {ph_color}">pH</div>
                            <div class="kpi-content">
                                <span class="kpi-label">Soil Reaction</span>
                                <span class="kpi-value" style="font-size:1.15rem;">{ph_tag}</span>
                                <span style="font-size:0.75rem; color:#64748b;">Tested pH: {soil_ph:.1f}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

                # Commercial Fertilizer Products Section
                st.markdown('<div class="saas-card">', unsafe_allow_html=True)
                st.markdown(f"<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📦 Commercial Fertilizer Product Requirements ({farm_acres} Acres)</h4>", unsafe_allow_html=True)
                st.caption("Exact quantities calculated from ANGRAU stoichiometric nutrient balancing formulas.")

                products = res.get("fertilizer_products", [])
                if products:
                    prod_cols = st.columns(len(products))
                    for idx, prod in enumerate(products):
                        with prod_cols[idx]:
                            st.markdown(
                                f"""
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-top:4px solid #16a34a; border-radius:10px; padding:16px; height:100%;">
                                    <div style="font-weight:700; color:#0f172a; font-size:1.05rem;">{prod.get('name')}</div>
                                    <div style="display:flex; align-items:baseline; gap:8px; margin:10px 0;">
                                        <span style="font-size:1.8rem; font-weight:800; color:#15803d;">{prod.get('quantity_kg')}</span>
                                        <span style="font-size:0.85rem; color:#64748b; font-weight:600;">kg total</span>
                                    </div>
                                    <div style="background:#e0f2fe; color:#0369a1; padding:4px 8px; border-radius:6px; font-weight:700; font-size:0.85rem; display:inline-block; margin-bottom:8px;">
                                        📦 {prod.get('bags_50kg')} Bags (50kg)
                                    </div>
                                    <p style="font-size:0.8rem; color:#64748b; margin:6px 0 0 0;">{prod.get('purpose')}</p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

                # Growth Stage Application Schedule & Nutrient Comparison
                col_sch, col_chart = st.columns([1.1, 0.9])

                with col_sch:
                    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
                    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📅 Crop Growth Split Application Schedule</h4>", unsafe_allow_html=True)
                    st.caption("Splitting fertilizer doses avoids nitrogen volatilization and matches plant uptake curve.")

                    schedule = res.get("application_schedule", [])
                    for i, step in enumerate(schedule, start=1):
                        st.markdown(
                            f"""
                            <div style="display:flex; gap:12px; margin-bottom:12px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:12px 16px;">
                                <div style="background:#16a34a; color:white; width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:0.85rem; flex-shrink:0;">
                                    {i}
                                </div>
                                <div style="color:#166534; font-size:0.9rem; line-height:1.4;">
                                    {step}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    # Micronutrients
                    micronutrients = res.get("micronutrients", [])
                    if micronutrients:
                        st.markdown("<h5 style='margin-top:16px; margin-bottom:8px; color:#0f172a;'>🔬 Micronutrient Application</h5>", unsafe_allow_html=True)
                        for micro in micronutrients:
                            st.warning(f"**Micronutrient Note:** {micro}")

                    st.markdown('</div>', unsafe_allow_html=True)

                with col_chart:
                    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
                    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📊 Nutrient Balancing Diagnostic</h4>", unsafe_allow_html=True)
                    st.caption("Base ANGRAU RDF Target vs Soil-Adjusted Recommended Dose (kg/ha)")

                    target_rdf = res.get("target_rdf_kg_ha", {"N": 120, "P2O5": 60, "K2O": 40})
                    adj_rdf = res.get("adjusted_rdf_kg_ha", {"N": 150, "P2O5": 60, "K2O": 40})

                    categories = ["Nitrogen (N)", "Phosphorus (P2O5)", "Potassium (K2O)"]
                    fig_bal = go.Figure()
                    fig_bal.add_trace(go.Bar(
                        x=categories,
                        y=[target_rdf.get("N", 0), target_rdf.get("P", target_rdf.get("P2O5", 0)), target_rdf.get("K", target_rdf.get("K2O", 0))],
                        name="Standard Crop RDF",
                        marker_color="#94a3b8",
                    ))
                    fig_bal.add_trace(go.Bar(
                        x=categories,
                        y=[adj_rdf.get("N", 0), adj_rdf.get("P2O5", adj_rdf.get("P", 0)), adj_rdf.get("K2O", adj_rdf.get("K", 0))],
                        name="Adjusted Farm Dosage",
                        marker_color="#16a34a",
                    ))
                    fig_bal.update_layout(
                        barmode="group",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10, r=10, t=20, b=20),
                        height=260,
                        yaxis=dict(title="Dose (kg/ha)", showgrid=True, gridcolor="#f1f5f9"),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    )
                    st.plotly_chart(fig_bal, use_container_width=True)

                    # Soil Health & Amendments Alerts
                    amendment = res.get("soil_amendment_advice")
                    if amendment:
                        st.error(f"🛡️ **Soil Amendment Required:** {amendment}")

                    oc_advice = res.get("organic_matter_advice")
                    if oc_advice:
                        st.info(f"🌿 **Organic Matter Advisory:** {oc_advice}")

                    st.markdown('</div>', unsafe_allow_html=True)

                render_disclaimer(res.get("advisory_disclaimer", res.get("safety_notice", "")))

with tab2:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🗺️ District Soil Health Indices across Andhra Pradesh</h4>", unsafe_allow_html=True)
    st.caption("Official Soil Health Card portal aggregated macronutrient availability and pH levels across 13 Andhra Pradesh districts.")

    if not df_soil.empty:
        st.dataframe(df_soil, use_container_width=True)
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fig_npk = go.Figure()
            fig_npk.add_trace(go.Bar(x=df_soil["district"], y=df_soil["available_nitrogen_kg_ha"], name="Nitrogen (kg/ha)", marker_color="#16a34a"))
            fig_npk.add_trace(go.Bar(x=df_soil["district"], y=df_soil["available_potassium_kg_ha"], name="Potassium (kg/ha)", marker_color="#eab308"))
            fig_npk.update_layout(
                title="Available Nitrogen & Potassium by District",
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=30),
                height=320,
                xaxis=dict(title="", tickangle=-25),
                yaxis=dict(title="Nutrient (kg/ha)", showgrid=True, gridcolor="#f1f5f9"),
            )
            st.plotly_chart(fig_npk, use_container_width=True)

        with col_c2:
            fig_ph = go.Figure()
            fig_ph.add_trace(go.Scatter(
                x=df_soil["district"],
                y=df_soil["soil_ph"],
                mode="lines+markers",
                name="Soil pH",
                line=dict(color="#0284c7", width=2),
                marker=dict(size=8, color="#0369a1"),
            ))
            fig_ph.add_hline(y=7.0, line_dash="dash", line_color="#94a3b8", annotation_text="Neutral (7.0)")
            fig_ph.update_layout(
                title="Average Soil pH across AP Districts",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=30),
                height=320,
                xaxis=dict(title="", tickangle=-25),
                yaxis=dict(title="pH Value", range=[5.0, 9.0], showgrid=True, gridcolor="#f1f5f9"),
            )
            st.plotly_chart(fig_ph, use_container_width=True)
    else:
        st.info("Loading baseline soil profiles...")
    st.markdown('</div>', unsafe_allow_html=True)
