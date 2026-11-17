"""
AgriAI Frontend - Reusable UI Card Components
Provides styled KPI cards, weather widgets, quick tool launchpad, and page banners.
"""

import streamlit as st


def render_kpi_row(
    total_production: str = "342.5 MT",
    production_delta: str = "↑ 12.5%",
    active_area: str = "2.8M Ha",
    area_delta: str = "↑ 8.3%",
    avg_mandi_price: str = "₹2,450 /Qtl",
    price_delta: str = "↑ 6.1%",
    current_weather: str = "32°C",
    weather_cond: str = "Partly Cloudy",
):
    """Render the 4-across top KPI metric cards with icons and trend badges."""
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-icon-circle kpi-icon-green">🍃</div>
                <div class="kpi-content">
                    <span class="kpi-label">Total Crop Production</span>
                    <span class="kpi-value">{total_production}</span>
                    <span class="kpi-trend-green">{production_delta}</span>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon-circle kpi-icon-emerald">🚜</div>
                <div class="kpi-content">
                    <span class="kpi-label">Gross Cultivated Area</span>
                    <span class="kpi-value">{active_area}</span>
                    <span class="kpi-trend-green">{area_delta}</span>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon-circle kpi-icon-gold">₹</div>
                <div class="kpi-content">
                    <span class="kpi-label">Avg Mandi Price</span>
                    <span class="kpi-value">{avg_mandi_price}</span>
                    <span class="kpi-trend-green">{price_delta}</span>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon-circle kpi-icon-sky">🌤️</div>
                <div class="kpi-content">
                    <span class="kpi-label">Current Weather</span>
                    <span class="kpi-value">{current_weather}</span>
                    <span style="font-size: 0.78rem; color: #0284c7; font-weight: 600; margin-top: 4px;">{weather_cond}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_weather_widget(
    district: str = "Guntur",
    temp_c: float = 32.0,
    condition: str = "Partly Cloudy",
    humidity: float = 68.0,
    wind: float = 12.0,
):
    """Render the interactive weather card with 5-day forecast strip."""
    st.markdown(
        f"""
        <div class="weather-saas-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <div>
                    <div style="font-size: 0.82rem; font-weight: 700; color: #64748b; text-transform: uppercase;">📍 {district}, Andhra Pradesh</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 4px 0;">{temp_c:.0f}°C</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #3b82f6;">{condition}</div>
                </div>
                <div style="font-size: 44px;">🌤️</div>
            </div>
            <div style="font-size: 0.82rem; color: #64748b; margin-bottom: 10px;">
                💧 Humidity: <b>{humidity:.0f}%</b> &nbsp;|&nbsp; 💨 Wind: <b>{wind:.0f} km/h</b>
            </div>
            <div class="weather-forecast-strip">
                <div class="forecast-day">
                    <span class="forecast-day-name">Tue</span>
                    <span class="forecast-icon">☀️</span>
                    <span class="forecast-temp">34°C</span>
                </div>
                <div class="forecast-day">
                    <span class="forecast-day-name">Wed</span>
                    <span class="forecast-icon">⛅</span>
                    <span class="forecast-temp">33°C</span>
                </div>
                <div class="forecast-day">
                    <span class="forecast-day-name">Thu</span>
                    <span class="forecast-icon">🌤️</span>
                    <span class="forecast-temp">32°C</span>
                </div>
                <div class="forecast-day">
                    <span class="forecast-day-name">Fri</span>
                    <span class="forecast-icon">🌧️</span>
                    <span class="forecast-temp">31°C</span>
                </div>
                <div class="forecast-day">
                    <span class="forecast-day-name">Sat</span>
                    <span class="forecast-icon">☀️</span>
                    <span class="forecast-temp">30°C</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
