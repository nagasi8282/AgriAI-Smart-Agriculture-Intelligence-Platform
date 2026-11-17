"""
AgriAI Frontend - Premium Agriculture SaaS Theme & Component System
Inspired by Agrivision AI, Microsoft Streamlit UI, Streamlit Facade, and official SaaS templates.
Color Palette: Forest Green (#0d3821), Agriculture Green (#22c55e), Harvest Gold (#f59e0b), Light Slate (#f8fafc).
"""

import streamlit as st
from datetime import datetime


def apply_saas_theme(dark_mode: bool = False):
    """
    Inject comprehensive CSS styling transforming Streamlit into a modern Agriculture SaaS platform.
    Features dark forest-green sidebar, custom card components, sleek typography, and responsive grid layout.
    """
    bg_color = "#0f172a" if dark_mode else "#f8fafc"
    card_bg = "#1e293b" if dark_mode else "#ffffff"
    card_border = "#334155" if dark_mode else "#e2e8f0"
    text_primary = "#f1f5f9" if dark_mode else "#0f172a"
    text_secondary = "#94a3b8" if dark_mode else "#64748b"

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

            /* Global Font and Body */
            html, body, [class*="css"] {{
                font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
                background-color: {bg_color};
                color: {text_primary};
            }}

            .main .block-container {{
                padding-top: 1.2rem;
                padding-bottom: 3.5rem;
                padding-left: 2rem;
                padding-right: 2rem;
                max-width: 1400px;
            }}

            /* ========================================================= */
            /* 1. SIDEBAR: Deep Forest Green (#0d3821) SaaS Aesthetic    */
            /* ========================================================= */
            /* Sidebar: Clean Expanded vs Collapsed States */
            section[data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #0d3821 0%, #114528 45%, #092c19 100%) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
                box-shadow: 4px 0 24px rgba(0, 0, 0, 0.25) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }}

            section[data-testid="stSidebar"][aria-expanded="true"] {{
                width: 320px !important;
                min-width: 300px !important;
            }}

            section[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {{
                width: 320px !important;
            }}

            section[data-testid="stSidebar"][aria-expanded="false"] {{
                margin-left: -340px !important;
                width: 0 !important;
                min-width: 0 !important;
                visibility: hidden !important;
                box-shadow: none !important;
                border-right: none !important;
            }}

            section[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {{
                width: 0 !important;
                min-width: 0 !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
                padding-top: 0.2rem !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul {{
                padding-left: 0 !important;
                list-style: none !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li {{
                margin: 4px 6px !important;
            }}

            /* Force bright, high-contrast, crystal-clear white text for all sidebar nav items */
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] * {{
                color: #ffffff !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
                color: #ffffff !important;
                background: rgba(255, 255, 255, 0.06) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                border-radius: 9px !important;
                padding: 10px 14px !important;
                display: flex !important;
                align-items: center !important;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
                text-decoration: none !important;
            }}

            /* Universal Sidebar Text Visibility Overrides */
            [data-testid="stSidebarNavLinkText"],
            [data-testid="stSidebarNavLink"] span,
            [data-testid="stSidebar"] ul li a span,
            [data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] [data-testid="stSidebarNavLinkText"],
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a span,
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a p {{
                color: #ffffff !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                white-space: normal !important;
                text-overflow: unset !important;
                overflow: visible !important;
                display: inline-block !important;
                line-height: 1.35 !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {{
                background: rgba(34, 197, 94, 0.28) !important;
                border-color: #22c55e !important;
                color: #ffffff !important;
                transform: translateX(4px) !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover span,
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover * {{
                color: #ffffff !important;
            }}

            /* Active Nav Item: Vibrant Emerald Green */
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"],
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a.active,
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li:has(a[aria-current="page"]) a {{
                background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
                border-color: #22c55e !important;
                color: #ffffff !important;
                font-weight: 700 !important;
                box-shadow: 0 4px 14px rgba(22, 163, 74, 0.45) !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] span,
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] *,
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li:has(a[aria-current="page"]) span {{
                color: #ffffff !important;
                font-weight: 700 !important;
            }}

            section[data-testid="stSidebar"] hr {{
                border-color: rgba(255, 255, 255, 0.12) !important;
                margin: 0.8rem 0 !important;
            }}

            /* Sidebar custom brand logo */
            .sidebar-brand-box {{
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 14px 20px 14px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 15px;
            }}
            .sidebar-brand-icon {{
                background: #22c55e;
                color: white;
                width: 38px;
                height: 38px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                box-shadow: 0 4px 10px rgba(34, 197, 94, 0.4);
            }}
            .sidebar-brand-title {{
                color: #ffffff;
                font-size: 1.45rem;
                font-weight: 800;
                letter-spacing: -0.5px;
                margin: 0;
            }}
            .sidebar-brand-tag {{
                color: #86efac;
                font-size: 0.72rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.8px;
            }}

            /* Sidebar Footer Card */
            .sidebar-footer-card {{
                background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
                border: 1px solid rgba(34, 197, 94, 0.25);
                border-radius: 12px;
                padding: 16px;
                margin: 20px 10px 10px 10px;
                text-align: center;
            }}
            .sidebar-footer-title {{
                color: #ffffff;
                font-weight: 700;
                font-size: 0.95rem;
                margin-top: 6px;
                margin-bottom: 4px;
            }}
            .sidebar-footer-sub {{
                color: #a7f3d0;
                font-size: 0.78rem;
            }}

            /* ========================================================= */
            /* 2. TOP APP BAR: Search, Badges & Profile                  */
            /* ========================================================= */
            .top-bar-container {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: {card_bg};
                border: 1px solid {card_border};
                border-radius: 12px;
                padding: 10px 18px;
                margin-bottom: 18px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
            }}
            .top-search-mock {{
                display: flex;
                align-items: center;
                gap: 10px;
                background: {'#0f172a' if dark_mode else '#f1f5f9'};
                border: 1px solid {card_border};
                border-radius: 8px;
                padding: 8px 14px;
                width: 380px;
                color: {text_secondary};
                font-size: 0.88rem;
            }}
            .top-actions-cluster {{
                display: flex;
                align-items: center;
                gap: 14px;
            }}
            .top-badge {{
                display: inline-flex !important;
                align-items: center !important;
                gap: 6px !important;
                padding: 6px 12px !important;
                border-radius: 20px !important;
                font-size: 0.82rem !important;
                font-weight: 600 !important;
                background: {'#1e293b' if dark_mode else '#f1f5f9'} !important;
                color: {text_primary} !important;
                border: 1px solid {card_border} !important;
                white-space: nowrap !important;
                flex-shrink: 0 !important;
            }}
            .user-profile-chip {{
                display: flex;
                align-items: center;
                gap: 10px;
                padding-left: 8px;
                border-left: 1px solid {card_border};
            }}
            .user-avatar {{
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background: #15803d;
                color: #ffffff;
                font-weight: 700;
                font-size: 0.85rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .user-meta {{
                display: flex;
                flex-direction: column;
                line-height: 1.2;
            }}
            .user-greeting {{
                font-size: 0.72rem;
                color: {text_secondary};
            }}
            .user-name {{
                font-size: 0.86rem;
                font-weight: 700;
                color: {text_primary};
            }}

            /* ========================================================= */
            /* 3. HERO WELCOME PANORAMA BANNER                           */
            /* ========================================================= */
            .hero-panorama-banner {{
                background: linear-gradient(135deg, rgba(13, 56, 33, 0.94) 0%, rgba(21, 102, 59, 0.82) 50%, rgba(34, 197, 94, 0.7) 100%),
                            url('https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1600&q=80') center/cover;
                border-radius: 16px;
                padding: 30px 36px;
                margin-bottom: 24px;
                color: white;
                box-shadow: 0 10px 25px rgba(13, 56, 33, 0.15);
                display: flex;
                align-items: center;
                justify-content: space-between;
                position: relative;
                overflow: hidden;
            }}
            .hero-title {{
                font-size: 2.1rem;
                font-weight: 800;
                color: #ffffff !important;
                margin: 0;
                letter-spacing: -0.5px;
            }}
            .hero-sub {{
                color: #d1fae5;
                font-size: 1.05rem;
                font-weight: 500;
                margin-top: 6px;
                margin-bottom: 0;
            }}
            .hero-location-badge {{
                background: rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(8px);
                border: 1px solid rgba(255, 255, 255, 0.35);
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                color: #ffffff;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }}

            /* ========================================================= */
            /* 4. KPI METRIC CARDS                                       */
            /* ========================================================= */
            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 16px;
                margin-bottom: 24px;
            }}
            .kpi-card {{
                background: {card_bg};
                border: 1px solid {card_border};
                border-radius: 14px;
                padding: 18px 20px;
                display: flex;
                align-items: center;
                gap: 16px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            .kpi-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            }}
            .kpi-icon-circle {{
                width: 52px;
                height: 52px;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                flex-shrink: 0;
            }}
            .kpi-icon-green {{
                background: rgba(34, 197, 94, 0.15);
                color: #16a34a;
            }}
            .kpi-icon-emerald {{
                background: rgba(16, 185, 129, 0.15);
                color: #059669;
            }}
            .kpi-icon-gold {{
                background: rgba(245, 158, 11, 0.15);
                color: #d97706;
            }}
            .kpi-icon-sky {{
                background: rgba(56, 189, 248, 0.15);
                color: #0284c7;
            }}
            .kpi-content {{
                display: flex;
                flex-direction: column;
            }}
            .kpi-label {{
                font-size: 0.82rem;
                font-weight: 600;
                color: {text_secondary};
                margin-bottom: 2px;
            }}
            .kpi-value {{
                font-size: 1.55rem;
                font-weight: 800;
                color: {text_primary};
                letter-spacing: -0.5px;
                line-height: 1.1;
            }}
            .kpi-trend-green {{
                font-size: 0.78rem;
                font-weight: 700;
                color: #16a34a;
                margin-top: 4px;
            }}

            /* ========================================================= */
            /* 5. WEATHER OVERVIEW CARD                                  */
            /* ========================================================= */
            .weather-saas-card {{
                background: {card_bg};
                border: 1px solid {card_border};
                border-radius: 14px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            }}
            .weather-forecast-strip {{
                display: flex;
                justify-content: space-between;
                border-top: 1px solid {card_border};
                padding-top: 14px;
                margin-top: 14px;
            }}
            .forecast-day {{
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 4px;
            }}
            .forecast-day-name {{
                font-size: 0.75rem;
                font-weight: 600;
                color: {text_secondary};
            }}
            .forecast-icon {{
                font-size: 20px;
            }}
            .forecast-temp {{
                font-size: 0.85rem;
                font-weight: 700;
                color: {text_primary};
            }}

            /* ========================================================= */
            /* 6. QUICK TOOLS 2x3 GRID                                   */
            /* ========================================================= */
            .quick-tools-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 14px;
                margin-bottom: 20px;
            }}
            .tool-card {{
                border-radius: 12px;
                padding: 16px;
                display: flex;
                align-items: center;
                gap: 12px;
                text-decoration: none !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                border: 1px solid transparent;
            }}
            .tool-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 14px rgba(0, 0, 0, 0.06);
            }}
            .tool-card-mint {{ background: #ecfdf5; border-color: #a7f3d0; color: #065f46; }}
            .tool-card-teal {{ background: #f0fdfa; border-color: #99f6e4; color: #115e59; }}
            .tool-card-amber {{ background: #fffbeb; border-color: #fde68a; color: #92400e; }}
            .tool-card-sky {{ background: #f0f9ff; border-color: #bae6fd; color: #075985; }}
            .tool-card-emerald {{ background: #f0fdf4; border-color: #bbf7d0; color: #166534; }}
            .tool-card-slate {{ background: #f8fafc; border-color: #e2e8f0; color: #334155; }}

            .tool-icon {{
                font-size: 24px;
                width: 42px;
                height: 42px;
                border-radius: 10px;
                background: white;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }}
            .tool-title {{
                font-size: 0.92rem;
                font-weight: 700;
                line-height: 1.2;
            }}

            /* ========================================================= */
            /* 7. PROMO BANNER (AI Powered Drone Farming)                */
            /* ========================================================= */
            .promo-banner {{
                background: linear-gradient(90deg, #134e2c 0%, #1e6b3f 60%, #22c55e 100%),
                            url('https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&w=1200&q=80') center/cover;
                border-radius: 14px;
                padding: 22px 28px;
                color: white;
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-top: 18px;
                margin-bottom: 24px;
            }}
            .promo-title {{
                font-size: 1.35rem;
                font-weight: 800;
                margin: 0;
            }}
            .promo-btn {{
                background: #f59e0b;
                color: #0f172a;
                font-weight: 700;
                font-size: 0.88rem;
                padding: 8px 18px;
                border-radius: 20px;
                border: none;
                display: inline-block;
                cursor: pointer;
            }}

            /* Standard SaaS Card Container */
            .saas-card {{
                background: {card_bg};
                border: 1px solid {card_border};
                border-radius: 14px;
                padding: 22px;
                margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            }}

            /* Standard Section Header */
            .section-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 16px;
            }}
            .section-title {{
                font-size: 1.15rem;
                font-weight: 700;
                color: {text_primary};
                display: flex;
                align-items: center;
                gap: 8px;
                margin: 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Comprehensive AgriAI search index across modules, crops, and datasets
SEARCH_INDEX = [
    {
        "keywords": ["crop", "rice", "paddy", "cotton", "chillies", "groundnut", "maize", "sugarcane", "production", "area", "harvest", "yield trend"],
        "title": "🌾 Crop Intelligence",
        "description": "Historical crop production, harvested area, and yield trends across 13 AP districts.",
        "page": "pages/1_🌾_Crop_Intelligence.py",
        "badge": "PRODUCTION ANALYTICS",
    },
    {
        "keywords": ["weather", "rain", "rainfall", "temperature", "temp", "humidity", "climate", "forecast", "monsoon", "drought"],
        "title": "🌦️ Weather Intelligence",
        "description": "Meteorological time-series, cumulative rainfall anomalies, and 5-day weather forecasts.",
        "page": "pages/2_🌦️_Weather_Intelligence.py",
        "badge": "CLIMATE MONITORING",
    },
    {
        "keywords": ["mandi", "price", "apmc", "market", "arrival", "modal", "wholesale", "spot price", "trading", "guntur mandi"],
        "title": "💰 Mandi Price Analytics",
        "description": "AGMARKNET wholesale commodity prices, daily arrivals, and inter-mandi price spreads.",
        "page": "pages/3_💰_Mandi_Price_Analytics.py",
        "badge": "MARKET INTELLIGENCE",
    },
    {
        "keywords": ["soil", "fertilizer", "urea", "dap", "mop", "ssp", "nitrogen", "phosphorus", "potassium", "npk", "ph", "angrau", "zinc", "gypsum", "lime"],
        "title": "🧪 Soil Health & Fertilizer Advisory",
        "description": "Soil nutrient diagnosis, ML formulation selection (98% accuracy), and ANGRAU 50kg bag schedules.",
        "page": "pages/4_🧪_Soil_and_Fertilizer.py",
        "badge": "PRECISION AGRONOMY",
    },
    {
        "keywords": ["yield", "predict yield", "yield forecast", "crop yield prediction", "tonnes", "quintal", "shap", "random forest yield"],
        "title": "📈 Crop Yield Prediction",
        "description": "ML regression forecasting crop harvest yield (Q/Ha) with TreeSHAP feature attributions.",
        "page": "pages/5_📈_Crop_Yield_Prediction.py",
        "badge": "PREDICTIVE ML",
    },
    {
        "keywords": ["price prediction", "price forecast", "future price", "modal price prediction", "time series price"],
        "title": "📊 Mandi Price Prediction",
        "description": "Statistical time-series forecasting projecting wholesale modal prices across 7 to 30 days.",
        "page": "pages/6_📊_Mandi_Price_Prediction.py",
        "badge": "FINANCIAL FORECASTING",
    },
    {
        "keywords": ["disease", "leaf", "plant disease", "blight", "rot", "spot", "mildew", "rust", "pathology", "grad-cam", "mobilenet", "efficientnet"],
        "title": "🍃 Plant Disease Detection",
        "description": "Transfer learning computer vision classifying leaf diseases with Grad-CAM visual heatmaps.",
        "page": "pages/7_🍃_Plant_Disease_Detection.py",
        "badge": "DEEP LEARNING VISION",
    },
    {
        "keywords": ["chat", "assistant", "bot", "ask ai", "agriai chat", "question", "advice", "agronomy questions"],
        "title": "🤖 AgriAI Chat Assistant",
        "description": "Conversational assistant grounded in regional agricultural datasets and ANGRAU guidelines.",
        "page": "pages/8_🤖_AgriAI_Chat_Assistant.py",
        "badge": "GENERATIVE AI",
    },
    {
        "keywords": ["pdf", "agridoc", "rag", "document", "research paper", "citations", "demilie", "pdf assistant", "upload pdf"],
        "title": "📄 AgriDoc AI PDF Assistant",
        "description": "Retrieval-Augmented Generation over agricultural papers with exact page-level citations.",
        "page": "pages/9_📄_AgriDoc_AI_PDF_Assistant.py",
        "badge": "LITERATURE RAG",
    },
    {
        "keywords": ["report", "download", "csv", "export", "audit", "dataset download"],
        "title": "📑 Reports & Downloads",
        "description": "Generate official agricultural audit reports and download sanitized datasets in CSV format.",
        "page": "pages/10_📑_Reports_and_Downloads.py",
        "badge": "EXPORT ENGINE",
    },
    {
        "keywords": ["about", "architecture", "thesis", "mtech", "methodology", "data flow", "snowflake", "dbt", "airflow"],
        "title": "ℹ️ About Project",
        "description": "Comprehensive M.Tech architectural profile, system specifications, and literature references.",
        "page": "pages/11_ℹ️_About_Project.py",
        "badge": "SYSTEM SPECS",
    },
]

PAGE_QUICK_JUMP = {
    "🏠 Dashboard Overview": "Home.py",
    "🌾 Crop Intelligence": "pages/1_🌾_Crop_Intelligence.py",
    "🌦️ Weather Intelligence": "pages/2_🌦️_Weather_Intelligence.py",
    "💰 Mandi Price Analytics": "pages/3_💰_Mandi_Price_Analytics.py",
    "🧪 Soil & Fertilizer Advisory": "pages/4_🧪_Soil_and_Fertilizer.py",
    "📈 Crop Yield Prediction": "pages/5_📈_Crop_Yield_Prediction.py",
    "📊 Mandi Price Prediction": "pages/6_📊_Mandi_Price_Prediction.py",
    "🍃 Plant Disease Detection": "pages/7_🍃_Plant_Disease_Detection.py",
    "🤖 AgriAI Chat Assistant": "pages/8_🤖_AgriAI_Chat_Assistant.py",
    "📄 AgriDoc AI PDF Assistant": "pages/9_📄_AgriDoc_AI_PDF_Assistant.py",
    "📑 Reports & Downloads": "pages/10_📑_Reports_and_Downloads.py",
    "ℹ️ About Project": "pages/11_ℹ️_About_Project.py",
}


def render_sidebar():
    """Render the standard Agrivision AI styled sidebar with visible navigation and quick jump."""
    with st.sidebar:
        # Brand logo
        st.markdown(
            """
            <div class="sidebar-brand-box">
                <div class="sidebar-brand-icon">🌱</div>
                <div>
                    <h2 class="sidebar-brand-title">AgriAI</h2>
                    <span class="sidebar-brand-tag">Smart Agriculture SaaS</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="padding: 0 10px; margin-bottom: 6px;">
                <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #86efac; font-weight: 700;">
                    Platform Modules
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Quick Page Switcher
        quick_select = st.selectbox(
            "⚡ Quick Page Switcher",
            options=["Select page to jump..."] + list(PAGE_QUICK_JUMP.keys()),
            index=0,
            key="sidebar_page_quick_jump",
            label_visibility="collapsed",
        )
        if quick_select != "Select page to jump...":
            target_script = PAGE_QUICK_JUMP[quick_select]
            st.switch_page(target_script)

        # Bottom Card
        st.markdown(
            """
            <div class="sidebar-footer-card">
                <div style="font-size: 32px; margin-bottom: 4px;">🌾</div>
                <div class="sidebar-footer-title">Growing Together with AgriAI</div>
                <div class="sidebar-footer-sub">Andhra Pradesh Edition • 2026</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_top_bar(current_district: str = "Guntur"):
    """
    Render top application bar with:
    1. Working Global Search Bar across crops, mandis, diseases, and pages.
    2. Real-time Location Pill & Current Date Badge.
    3. User Authentication Popover with full Login / Switch Account options.
    """
    # 1. State-aware authentication management
    if "auth_user" not in st.session_state:
        st.session_state.auth_user = {
            "is_logged_in": False,
            "name": "Guest Farmer",
            "role": "Farmer",
            "district": current_district or "Guntur",
        }

    current_date_str = datetime.now().strftime("%b %d, %Y")
    active_district = st.session_state.auth_user.get("district", current_district)
    user_name = st.session_state.auth_user.get("name", "Guest Farmer")
    user_role = st.session_state.auth_user.get("role", "Farmer")
    is_logged_in = st.session_state.auth_user.get("is_logged_in", False)

    # 2. Render Top Bar 3-Column Layout inside a crisp card container
    with st.container(border=True):
        col_search, col_meta, col_auth = st.columns([1.8, 1.3, 0.9], vertical_alignment="center")

        # Column 1: Working Search Bar
        with col_search:
            search_query = st.text_input(
                "Search AgriAI Platform",
                placeholder="🔍 Search crops, mandis, diseases, or pages...",
                label_visibility="collapsed",
                key="global_top_search_input",
            )

        # Column 2: Location and Date Badges
        with col_meta:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; justify-content:flex-end; gap:8px; white-space:nowrap; flex-wrap:nowrap;">
                    <span class="top-badge">📍 {active_district}, AP</span>
                    <span class="top-badge">📅 {current_date_str}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Column 3: User Login & Account Switch Option (Replacing static Jyoti Developer)
        with col_auth:
            if not is_logged_in:
                with st.popover("🔑 Sign In", use_container_width=True):
                    st.markdown("#### 🌾 AgriAI User Sign In")
                    st.caption("Sign in to access personalized farm analytics, model predictions, and advisory downloads.")
                    login_user = st.text_input("Username or Mobile Number", placeholder="e.g. nagasai or 9876543210", key="login_field_user")
                    login_pass = st.text_input("Password", type="password", placeholder="Enter your password", key="login_field_pass")
                    login_role = st.selectbox(
                        "User Category / Role",
                        ["Farmer", "Agronomist / Scientist", "Agricultural Extension Officer (RBK)", "Student / Researcher"],
                        index=0,
                        key="login_field_role",
                    )
                    login_dist = st.selectbox(
                        "Default Farm District",
                        ["Guntur", "Krishna", "Kurnool", "Anantapur", "East Godavari", "West Godavari", "Chittoor", "Prakasam"],
                        index=0,
                        key="login_field_dist",
                    )
                    bcol1, bcol2 = st.columns(2)
                    with bcol1:
                        if st.button("Sign In", type="primary", use_container_width=True, key="login_btn_submit"):
                            uname = login_user.strip() if login_user.strip() else "Nagasai Farmer"
                            st.session_state.auth_user = {
                                "is_logged_in": True,
                                "name": uname,
                                "role": login_role,
                                "district": login_dist,
                            }
                            st.rerun()
                    with bcol2:
                        if st.button("Quick Demo", use_container_width=True, key="login_btn_demo"):
                            st.session_state.auth_user = {
                                "is_logged_in": True,
                                "name": "Nagasai (Farmer)",
                                "role": "Farmer",
                                "district": "Guntur",
                            }
                            st.rerun()
            else:
                role_short = user_role.split()[0]
                with st.popover(f"👤 {user_name} ({role_short})", use_container_width=True):
                    st.markdown(f"### 🌾 {user_name}")
                    st.markdown(f"**Role:** {user_role}")
                    st.markdown(f"**Operating District:** {active_district}, Andhra Pradesh")
                    st.markdown("**Status:** Verified User 🟢")
                    st.markdown("---")
                    if st.button("Sign Out / Switch Account", type="secondary", use_container_width=True, key="logout_btn_submit"):
                        st.session_state.auth_user = {
                            "is_logged_in": False,
                            "name": "Guest Farmer",
                            "role": "Farmer",
                            "district": "Guntur",
                        }
                        st.rerun()

    # 3. Interactive Search Results Display (Triggered when user types a query)
    if search_query and search_query.strip():
        query_clean = search_query.strip().lower()
        matched_modules = []
        for mod in SEARCH_INDEX:
            if (
                any(kw in query_clean or query_clean in kw for kw in mod["keywords"])
                or query_clean in mod["title"].lower()
                or query_clean in mod["description"].lower()
            ):
                matched_modules.append(mod)

        st.markdown(
            f"""
            <div style="background:#ffffff; border:2px solid #22c55e; border-radius:12px; padding:16px 20px; margin: 10px 0 20px 0; box-shadow: 0 4px 14px rgba(34, 197, 94, 0.15);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <div style="font-weight:700; color:#0f172a; font-size:1.05rem;">
                        🔍 AgriAI Search Results for <span style="color:#15803d;">"{search_query}"</span> ({len(matched_modules)} modules found)
                    </div>
                    <span style="font-size:0.8rem; background:#ecfdf5; color:#15803d; padding:3px 10px; border-radius:12px; font-weight:700;">INSTANT NAVIGATION</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if matched_modules:
            m_cols = st.columns(min(len(matched_modules), 3))
            for idx, item in enumerate(matched_modules[:3]):
                with m_cols[idx]:
                    st.markdown(
                        f"""
                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-top:3px solid #16a34a; border-radius:8px; padding:14px; height:100%;">
                            <span style="font-size:0.7rem; font-weight:700; color:#15803d; text-transform:uppercase;">{item['badge']}</span>
                            <div style="font-weight:700; color:#0f172a; font-size:0.95rem; margin:4px 0;">{item['title']}</div>
                            <p style="font-size:0.82rem; color:#64748b; margin:0 0 10px 0;">{item['description']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.page_link(item["page"], label=f"Open {item['title'].split()[1]} ➔", use_container_width=True)
        else:
            st.info(f"No direct modules found for '{search_query}'. Try searching for: Cotton, Paddy, Mandi Prices, Weather, Fertilizer, Leaf Disease, Yield Prediction, or Research PDF.")


def render_hero_banner(
    title: str = "Welcome to AgriAI",
    subtitle: str = "Smart Farming. Brighter Future.",
    district: str = "Andhra Pradesh",
):
    """Render the panoramic agriculture hero banner."""
    st.markdown(
        f"""
        <div class="hero-panorama-banner">
            <div>
                <h1 class="hero-title">🌱 {title}</h1>
                <p class="hero-sub">{subtitle}</p>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
                <div class="hero-location-badge">📍 {district}</div>
                <div class="hero-location-badge">✨ AI-Powered Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
