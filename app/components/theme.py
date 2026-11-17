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
            section[data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #0d3821 0%, #114528 45%, #092c19 100%) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
                box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
                padding-top: 0.5rem;
            }}

            /* Sidebar Nav Links */
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li a {{
                color: #e2e8f0 !important;
                font-weight: 500 !important;
                font-size: 0.92rem !important;
                border-radius: 9px !important;
                padding: 10px 14px !important;
                margin: 3px 10px !important;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
                display: flex !important;
                align-items: center !important;
            }}

            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li a:hover {{
                background: rgba(255, 255, 255, 0.1) !important;
                color: #ffffff !important;
                transform: translateX(3px);
            }}

            /* Active Nav Item: Vibrant Emerald Green Pill */
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li a[aria-current="page"],
            section[data-testid="stSidebar"] [data-testid="stSidebarNav"] ul li a.active {{
                background: #22c55e !important;
                color: #ffffff !important;
                font-weight: 700 !important;
                box-shadow: 0 4px 12px rgba(34, 197, 94, 0.35) !important;
            }}

            section[data-testid="stSidebar"] hr {{
                border-color: rgba(255, 255, 255, 0.12) !important;
                margin: 1rem 0 !important;
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
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.82rem;
                font-weight: 600;
                background: {'#1e293b' if dark_mode else '#f1f5f9'};
                color: {text_primary};
                border: 1px solid {card_border};
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


def render_sidebar():
    """Render the standard Agrivision AI styled sidebar."""
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
            <div style="padding: 0 10px; margin-bottom: 10px;">
                <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #86efac; font-weight: 700;">
                    Platform Modules
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
    """Render the top SaaS application bar with search, state/district pill, date, and user profile."""
    current_date_str = datetime.now().strftime("%b %d, %Y")
    st.markdown(
        f"""
        <div class="top-bar-container">
            <div class="top-search-mock">
                <span>🔍</span>
                <span>Search crops, mandis, or advisory literature...</span>
            </div>
            <div class="top-actions-cluster">
                <div class="top-badge">📍 {current_district}, Andhra Pradesh</div>
                <div class="top-badge">📅 {current_date_str}</div>
                <div class="user-profile-chip">
                    <div class="user-avatar">JD</div>
                    <div class="user-meta">
                        <span class="user-greeting">Welcome,</span>
                        <span class="user-name">Jyoti Developer</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
