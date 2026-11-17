"""
AgriAI - Module 12: About Project & Academic Architecture
Comprehensive overview of system architecture, scientific foundations, and M.Tech thesis scope.
"""

import streamlit as st
from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer

st.set_page_config(page_title="About Project | AgriAI", page_icon="ℹ️", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Andhra Pradesh")

render_page_header(
    title="About AgriAI – Academic & Architectural Profile",
    subtitle="End-to-End Smart Agriculture Intelligence Platform: Engineering Architecture, Scientific Literature, and Research Scope.",
    category_tag="ACADEMIC & TECHNICAL SPECIFICATIONS",
)

st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown(
    """
    <h3 style="color:#0f172a; font-weight:800; margin-top:0;">1. Executive Summary & Thesis Scope</h3>
    <p style="color:#334155; line-height:1.7;">
        <b>AgriAI</b> is engineered as a Master of Technology (M.Tech) dissertation platform resolving critical agricultural data fragmentation,
        market price opacity, and crop pathology bottlenecks across <b>Andhra Pradesh, India</b>.
    </p>
    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:16px; margin:20px 0;">
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:16px;">
            <h4 style="color:#166534; margin:0 0 6px 0;">🏗️ Modern Data Engineering</h4>
            <p style="font-size:0.86rem; color:#14532d; margin:0;">
                Medallion Lakehouse (Bronze, Silver, Gold), Snowflake analytics warehouse, dbt Core transformations, and Apache Airflow scheduled DAGs.
            </p>
        </div>
        <div style="background:#f0fdfa; border:1px solid #99f6e4; border-radius:10px; padding:16px;">
            <h4 style="color:#115e59; margin:0 0 6px 0;">🧠 Predictive Machine Learning</h4>
            <p style="font-size:0.86rem; color:#134e4a; margin:0;">
                Crop yield regression with TreeSHAP feature attributions and time-series mandi modal price forecasting across APMC yards.
            </p>
        </div>
        <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:10px; padding:16px;">
            <h4 style="color:#92400e; margin:0 0 6px 0;">🍃 Deep Learning Computer Vision</h4>
            <p style="font-size:0.86rem; color:#78350f; margin:0;">
                Foliage pathology classification (MobileNetV2 / EfficientNetB0) with Grad-CAM visual attention overlays guided by Demilie (2024).
            </p>
        </div>
        <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:10px; padding:16px;">
            <h4 style="color:#075985; margin:0 0 6px 0;">📄 Grounded Generative AI & RAG</h4>
            <p style="font-size:0.86rem; color:#0c4a6e; margin:0;">
                AgriDoc AI literature question-answering with exact document page citations and strict anti-hallucination guardrails.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# Literature Reference Card
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown(
    """
    <h3 style="color:#0f172a; font-weight:800; margin-top:0;">2. Scientific Literature Reference</h3>
    <p style="color:#334155; line-height:1.7;">
        The deep learning vision architecture and comparative methodology are directly guided by:
    </p>
    <div style="background:#f8fafc; border-left:4px solid #16a34a; padding:16px; border-radius:6px; margin:12px 0;">
        <b>Demilie, Wubetu Barud (2024)</b>. <i>Plant disease detection and classification techniques: a comparative study of the performances</i>.
        <b>Journal of Big Data (SpringerOpen)</b>, 11:71. <a href="https://doi.org/10.1186/s40537-024-00927-1" target="_blank">https://doi.org/10.1186/s40537-024-00927-1</a>
    </div>
    <p style="font-size:0.88rem; color:#64748b;">
        Key principles implemented: Depthwise separable convolutions (MobileNetV2) for resource-constrained edge smartphones,
        compound scaling (EfficientNetB0) for server-side accuracy, training-only data augmentation, and visual saliency interpretability.
    </p>
    """,
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# Technology Stack Table Card
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown(
    """
    <h3 style="color:#0f172a; font-weight:800; margin-top:0;">3. Enterprise Technology Stack</h3>
    <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:0.9rem;">
        <thead>
            <tr style="background:#f1f5f9; border-bottom:2px solid #e2e8f0; text-align:left;">
                <th style="padding:10px 14px;">Domain</th>
                <th style="padding:10px 14px;">Technology Components</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 14px; font-weight:700;">Backend & Microservices</td>
                <td style="padding:10px 14px;">FastAPI, Pydantic v2, Uvicorn, Python 3.12</td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 14px; font-weight:700;">Storage & Warehousing</td>
                <td style="padding:10px 14px;">PostgreSQL 16, Snowflake (Bronze/Silver/Gold), AWS S3, Local Parquet Lake</td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 14px; font-weight:700;">Transformation & Orchestration</td>
                <td style="padding:10px 14px;">dbt Core (dbt-snowflake / dbt-postgres), Apache Airflow 2.9</td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 14px; font-weight:700;">Predictive ML</td>
                <td style="padding:10px 14px;">Scikit-learn, RandomForest, GradientBoosting, TreeSHAP Explainability</td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 14px; font-weight:700;">Deep Learning & Vision</td>
                <td style="padding:10px 14px;">MobileNetV2, EfficientNetB0, Grad-CAM Saliency, PIL/OpenCV</td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 14px; font-weight:700;">Generative AI & RAG</td>
                <td style="padding:10px 14px;">SentenceTransformers (all-MiniLM-L6-v2), PyMuPDF, FAISS / Dense Vector Store</td>
            </tr>
            <tr style="border-bottom:1px solid #f1f5f9;">
                <td style="padding:10px 14px; font-weight:700;">Frontend Dashboard</td>
                <td style="padding:10px 14px;">Streamlit, Plotly Express & Graph Objects, Custom SaaS CSS</td>
            </tr>
        </tbody>
    </table>
    """,
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

render_disclaimer(
    "AgriAI Platform - Master of Technology (M.Tech) in Computer Science & Engineering / Data Engineering."
)
