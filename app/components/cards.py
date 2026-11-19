"""
AgriAI Frontend - Reusable UI Card Components
Provides styled KPI cards, weather widgets, quick tool launchpad, and page banners.
"""

import streamlit as st
from typing import Optional, List, Dict, Any


def render_kpi_row(
    total_production: str = "342.5 MT",
    production_delta: str = "↑ 12.5%",
    active_area: str = "2.8M Ha",
    area_delta: str = "↑ 8.3%",
    avg_mandi_price: str = "₹2,450 /Qtl",
    price_delta: str = "↑ 6.1%",
    current_weather: str = "32°C",
    weather_cond: str = "Partly Cloudy",
    weather_icon: str = "🌤️",
):
    """Render the 4-across top KPI metric cards with icons and trend badges."""
    kpi_html = (
        f'<div class="kpi-grid">'
        f'<div class="kpi-card">'
        f'<div class="kpi-icon-circle kpi-icon-green">🍃</div>'
        f'<div class="kpi-content">'
        f'<span class="kpi-label">Total Crop Production</span>'
        f'<span class="kpi-value">{total_production}</span>'
        f'<span class="kpi-trend-green">{production_delta}</span>'
        f'</div>'
        f'</div>'
        f'<div class="kpi-card">'
        f'<div class="kpi-icon-circle kpi-icon-emerald">🚜</div>'
        f'<div class="kpi-content">'
        f'<span class="kpi-label">Gross Cultivated Area</span>'
        f'<span class="kpi-value">{active_area}</span>'
        f'<span class="kpi-trend-green">{area_delta}</span>'
        f'</div>'
        f'</div>'
        f'<div class="kpi-card">'
        f'<div class="kpi-icon-circle kpi-icon-gold">₹</div>'
        f'<div class="kpi-content">'
        f'<span class="kpi-label">Avg Mandi Price</span>'
        f'<span class="kpi-value">{avg_mandi_price}</span>'
        f'<span class="kpi-trend-green">{price_delta}</span>'
        f'</div>'
        f'</div>'
        f'<div class="kpi-card">'
        f'<div class="kpi-icon-circle kpi-icon-sky">{weather_icon}</div>'
        f'<div class="kpi-content">'
        f'<span class="kpi-label">Current Weather</span>'
        f'<span class="kpi-value">{current_weather}</span>'
        f'<span style="font-size:0.78rem;color:#0284c7;font-weight:600;margin-top:4px;">{weather_cond}</span>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(kpi_html, unsafe_allow_html=True)


def render_weather_widget(
    district: str = "Guntur",
    temp_c: float = 30.0,
    condition: str = "Partly Cloudy",
    humidity: float = 60.0,
    wind: float = 10.0,
    icon: str = "🌤️",
    forecast: Optional[List[Dict[str, Any]]] = None,
    is_live: bool = True,
    feels_like: Optional[float] = None,
):
    """Render the interactive live weather card with dynamic 5-day forecast strip."""
    live_badge = (
        '<span style="display:inline-flex;align-items:center;gap:5px;font-size:0.70rem;font-weight:700;'
        'color:#059669;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:9999px;padding:2px 8px;letter-spacing:0.5px;">'
        '<span style="width:6px;height:6px;border-radius:50%;background:#10b981;display:inline-block;"></span>'
        'LIVE METEOROLOGY</span>'
    ) if is_live else ""

    forecast_items_html = []
    if forecast and len(forecast) > 0:
        items = forecast[1:6] if len(forecast) >= 6 else forecast[:5]
        for item in items:
            d_name = item.get("day", "Day")
            d_icon = item.get("icon", "🌤️")
            d_max = item.get("temp_max", 32.0)
            forecast_items_html.append(
                f'<div class="forecast-day">'
                f'<span class="forecast-day-name">{d_name}</span>'
                f'<span class="forecast-icon">{d_icon}</span>'
                f'<span class="forecast-temp">{d_max:.0f}°C</span>'
                f'</div>'
            )
    else:
        default_days = [("Thu", "⛅", 32), ("Fri", "☀️", 33), ("Sat", "☁️", 31), ("Sun", "🌦️", 30), ("Mon", "🌤️", 32)]
        for d_name, d_icon, d_temp in default_days:
            forecast_items_html.append(
                f'<div class="forecast-day">'
                f'<span class="forecast-day-name">{d_name}</span>'
                f'<span class="forecast-icon">{d_icon}</span>'
                f'<span class="forecast-temp">{d_temp}°C</span>'
                f'</div>'
            )

    forecast_strip = "".join(forecast_items_html)
    feels_str = f"&nbsp;|&nbsp; 🌡️ Feels: <b>{feels_like:.0f}°C</b>" if feels_like is not None else ""

    card_html = (
        f'<div class="weather-saas-card">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
        f'<div style="font-size:0.80rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">📍 {district}, Andhra Pradesh</div>'
        f'{live_badge}'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">'
        f'<div>'
        f'<div style="font-size:2.2rem;font-weight:800;color:#0f172a;margin:2px 0;line-height:1.1;">{temp_c:.0f}°C</div>'
        f'<div style="font-size:0.95rem;font-weight:600;color:#0284c7;">{condition}</div>'
        f'</div>'
        f'<div style="font-size:46px;line-height:1;">{icon}</div>'
        f'</div>'
        f'<div style="font-size:0.82rem;color:#64748b;margin-bottom:12px;background:#f8fafc;padding:6px 10px;border-radius:8px;">'
        f'💧 Humidity: <b>{humidity:.0f}%</b> &nbsp;|&nbsp; 💨 Wind: <b>{wind:.0f} km/h</b>{feels_str}'
        f'</div>'
        f'<div class="weather-forecast-strip">{forecast_strip}</div>'
        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)


def render_quick_tools():
    """Render the 2x3 interactive tool grid."""
    st.markdown(
        """
        <div class="quick-tools-grid">
            <a href="Plant_Disease_Detection" target="_self" class="tool-card tool-card-mint">
                <div class="tool-icon">🍃</div>
                <div>
                    <div class="tool-title">Disease Detection</div>
                    <div style="font-size: 0.75rem; opacity: 0.85;">Deep learning diagnosis</div>
                </div>
            </a>
            <a href="Crop_Yield_Prediction" target="_self" class="tool-card tool-card-teal">
                <div class="tool-icon">📈</div>
                <div>
                    <div class="tool-title">Yield Prediction</div>
                    <div style="font-size: 0.75rem; opacity: 0.85;">SHAP ML estimation</div>
                </div>
            </a>
            <a href="Mandi_Price_Prediction" target="_self" class="tool-card tool-card-amber">
                <div class="tool-icon">₹</div>
                <div>
                    <div class="tool-title">Price Prediction</div>
                    <div style="font-size: 0.75rem; opacity: 0.85;">Modal price forecasts</div>
                </div>
            </a>
            <a href="AgriDoc_AI_PDF_Assistant" target="_self" class="tool-card tool-card-sky">
                <div class="tool-icon">📄</div>
                <div>
                    <div class="tool-title">AgriDoc AI (PDF)</div>
                    <div style="font-size: 0.75rem; opacity: 0.85;">Literature RAG with citations</div>
                </div>
            </a>
            <a href="AgriAI_Chat_Assistant" target="_self" class="tool-card tool-card-emerald">
                <div class="tool-icon">💬</div>
                <div>
                    <div class="tool-title">Chat with AgriAI</div>
                    <div style="font-size: 0.75rem; opacity: 0.85;">Grounded agronomy AI</div>
                </div>
            </a>
            <a href="Reports_and_Downloads" target="_self" class="tool-card tool-card-slate">
                <div class="tool-icon">📥</div>
                <div>
                    <div class="tool-title">Download Reports</div>
                    <div style="font-size: 0.75rem; opacity: 0.85;">Audit summaries & CSVs</div>
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_promo_banner():
    """Render the bottom promotional AI drone banner."""
    st.markdown(
        """
        <div class="promo-banner">
            <div>
                <h3 class="promo-title">Smarter Agriculture Powered by AI</h3>
                <p style="margin: 4px 0 0 0; color: #dcfce7; font-size: 0.92rem;">
                    Empowering farmers, researchers, and extension officers with end-to-end data intelligence.
                </p>
            </div>
            <div>
                <a href="About_Project" target="_self" style="text-decoration: none;">
                    <button class="promo-btn">Explore Architecture →</button>
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str, category_tag: str = "AGRICULTURE INTELLIGENCE"):
    """Standardized header for deep-dive application pages."""
    st.markdown(
        f"""
        <div style="margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #16a34a; letter-spacing: 1px; text-transform: uppercase;">
                {category_tag}
            </div>
            <h1 style="font-size: 2rem; font-weight: 800; color: #0f172a; margin: 4px 0 6px 0; letter-spacing: -0.5px;">
                {title}
            </h1>
            <p style="font-size: 1rem; color: #64748b; margin: 0;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
