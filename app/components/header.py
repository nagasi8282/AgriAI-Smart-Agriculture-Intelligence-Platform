"""
AgriAI Frontend - UI Components & Styling Module
Provides agriculture-themed CSS tokens, branding headers, and status cards.
"""

import streamlit as st


def apply_custom_theme():
    """Inject custom CSS for an agriculture-inspired theme (Forest Green, Emerald, Neutral Slate)."""
    st.markdown(
        """
        <style>
            /* Main container aesthetic */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1200px;
            }
            /* Metric card styling */
            div[data-testid="stMetric"] {
                background-color: #f7faf7;
                border: 1px solid #d4edd4;
                border-radius: 8px;
                padding: 12px 16px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            div[data-testid="stMetricLabel"] {
                font-size: 0.85rem !important;
                font-weight: 600 !important;
                color: #2d5a27 !important;
            }
            div[data-testid="stMetricValue"] {
                font-size: 1.6rem !important;
                color: #1b4332 !important;
            }
            /* AgriAI custom banner */
            .agri-banner {
                background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
                color: white;
                padding: 24px 30px;
                border-radius: 12px;
                margin-bottom: 25px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.08);
            }
            .agri-banner h1 {
                color: #d8f3dc !important;
                margin: 0;
                font-size: 2.2rem;
                font-weight: 700;
            }
            .agri-banner p {
                color: #e9f5ed;
                margin-top: 6px;
                margin-bottom: 0;
                font-size: 1.05rem;
            }
            /* Disclaimer box */
            .disclaimer-box {
                background-color: #fff9db;
                border-left: 4px solid #f59f00;
                padding: 12px 18px;
                border-radius: 4px;
                font-size: 0.88rem;
                color: #5f370e;
                margin-top: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str, icon: str = "🌾"):
    """Render consistent header banner across application pages."""
    apply_custom_theme()
    st.markdown(
        f"""
        <div class="agri-banner">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer(message: str):
    """Render a warning or agronomic disclaimer callout."""
    st.markdown(
        f"""
        <div class="disclaimer-box">
            <strong>Advisory Notice:</strong> {message}
        </div>
        """,
        unsafe_allow_html=True,
    )
