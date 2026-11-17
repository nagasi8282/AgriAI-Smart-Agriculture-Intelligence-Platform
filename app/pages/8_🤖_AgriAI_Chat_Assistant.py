"""
AgriAI - Module 9: AgriAI Chat Assistant
Context-aware conversational assistant with agricultural guardrails for Andhra Pradesh.
Design inspiration: Microsoft Streamlit UI Chatbot Template.
"""

import streamlit as st
from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="AgriAI Assistant | AgriAI", page_icon="🤖", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Guntur")

render_page_header(
    title="AgriAI Conversational Agronomy Assistant",
    subtitle="Context-aware natural language assistant answering agricultural queries with real-time agronomic data grounding for Andhra Pradesh.",
    category_tag="GROUNDED GENERATIVE AI ASSISTANT",
)

# Context Selector Bar
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
col_c1, col_c2, col_c3 = st.columns([1, 1, 2])
with col_c1:
    district = st.selectbox(
        "Active Farming District",
        ["Guntur", "Krishna", "Kurnool", "Anantapur", "East Godavari", "Chittoor", "Prakasam", "West Godavari"],
        index=0,
    )
with col_c2:
    crop_focus = st.selectbox(
        "Target Crop Context",
        ["All Crops", "Paddy (Rice)", "Chillies", "Cotton", "Groundnut", "Maize"],
        index=0,
    )
with col_c3:
    st.info(f"🌾 Assistant context active for **{district} District** • Focus: **{crop_focus}**")
st.markdown('</div>', unsafe_allow_html=True)

# Prompt Suggestions
st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#64748b; margin-bottom:8px;'>SUGGESTED AGRONOMIC PROMPTS:</div>", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns(3)
quick_prompt = None

with p_col1:
    if st.button("💰 What are the latest chilli prices at Guntur APMC?", use_container_width=True):
        quick_prompt = "What are the latest chilli prices at Guntur APMC?"
with p_col2:
    if st.button("🌾 What is the average paddy yield in our district?", use_container_width=True):
        quick_prompt = "What is the average paddy yield in our district?"
with p_col3:
    if st.button("🍃 How do I identify and manage Early Blight in tomatoes?", use_container_width=True):
        quick_prompt = "How do I identify and manage Early Blight in tomatoes?"

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Initialize chat session
if "saas_chat_messages" not in st.session_state:
    st.session_state.saas_chat_messages = [
        {
            "role": "assistant",
            "content": (
                f"Hello! I am AgriAI, your smart agricultural assistant for {district}, Andhra Pradesh. "
                "How may I assist your farm operations, crop health, or mandi market decisions today?"
            ),
        }
    ]

# Render Chat History
chat_container = st.container()
with chat_container:
    for msg in st.session_state.saas_chat_messages:
        with st.chat_message(msg["role"], avatar="🌱" if msg["role"] == "assistant" else None):
            st.write(msg["content"])

# User Chat Input
user_input = st.chat_input("Ask an agricultural, weather, or market question...")
if quick_prompt:
    user_input = quick_prompt

if user_input:
    # Append user message
    st.session_state.saas_chat_messages.append({"role": "user", "content": user_input})
    with chat_container:
        with st.chat_message("user"):
            st.write(user_input)

    # Call backend assistant service
    with chat_container:
        with st.chat_message("assistant", avatar="🌱"):
            with st.spinner("Retrieving agricultural datasets and formulating grounded response..."):
                crop_param = None if crop_focus == "All Crops" else crop_focus
                res = api_client.chat_assistant(message=user_input, district=district, crop=crop_param)
                reply = res.get("response", "I encountered an error formulating an agricultural response.")
                st.write(reply)

                domains = res.get("source_domains", [])
                if domains:
                    st.caption(f"📚 Grounded in: {', '.join(domains)}")

                st.session_state.saas_chat_messages.append({"role": "assistant", "content": reply})

render_disclaimer(
    "AgriAI Assistant provides algorithmically grounded decision support. "
    "Do not prescribe chemical pesticides or hazardous chemicals without on-field validation by certified agricultural officers."
)
