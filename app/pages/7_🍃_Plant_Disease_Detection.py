"""
AgriAI - Module 8: Plant Disease Detection (Deep Learning Computer Vision)
Leaf foliage pathology classification using transfer learning (MobileNetV2 / EfficientNetB0)
and Grad-CAM visual attention heatmaps. Literature reference: Demilie (2024), Journal of Big Data.
"""

import streamlit as st
from PIL import Image
import io

from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="Plant Disease Detection | AgriAI", page_icon="🍃", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Guntur")

render_page_header(
    title="Plant Disease Diagnosis & Visual Saliency (Grad-CAM)",
    subtitle="Convolutional neural network foliage pathology screening featuring MobileNetV2 / EfficientNetB0 backbones with Grad-CAM heatmaps.",
    category_tag="DEEP LEARNING COMPUTER VISION",
)

col_u1, col_u2 = st.columns([1, 1.2])

with col_u1:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📸 1. Foliage Image Capture / Upload</h4>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Plant Leaf Photograph (JPEG / PNG)",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear, focused leaf photograph with visible foliage.",
    )

    crop_hint = st.selectbox(
        "Crop Context (Optional)",
        ["Auto-detect", "Tomato", "Potato", "Pepper Bell", "Corn (Maize)"],
        index=0,
    )
    hint_val = None if crop_hint == "Auto-detect" else crop_hint

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Leaf Photograph", use_column_width=True)
        predict_btn = st.button("Run Deep Learning Diagnostic Model", type="primary", use_container_width=True)
    else:
        st.info("Upload a plant leaf image above to initiate deep learning inference.")
        predict_btn = False

    st.markdown('</div>', unsafe_allow_html=True)

with col_u2:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>🔬 2. Diagnostic Report & Saliency Overlay</h4>", unsafe_allow_html=True)

    if uploaded_file is not None and predict_btn:
        with st.spinner("Executing convolutional inference and computing Grad-CAM saliency gradients..."):
            file_bytes = uploaded_file.getvalue()
            res = api_client.predict_disease(file_bytes, uploaded_file.name, crop_hint=hint_val)

            if "error" in res:
                st.error(f"Diagnostic error: {res['error']}")
            elif not res.get("is_valid_plant", True):
                st.warning(f"Uncertain / Invalid Input: {res.get('predicted_class')}. {res.get('disclaimer')}")
            else:
                pred_class = res.get("predicted_class", "Unknown")
                crop_name = res.get("crop_name", "")
                condition = res.get("condition", "")
                conf = res.get("confidence", 0.0)
                conf_level = res.get("confidence_level", "Moderate")

                # Diagnostic Status Banner
                is_healthy = "healthy" in pred_class.lower()
                status_color = "#16a34a" if is_healthy else "#dc2626"
                status_bg = "#f0fdf4" if is_healthy else "#fef2f2"
                status_border = "#bbf7d0" if is_healthy else "#fecaca"

                st.markdown(
                    f"""
                    <div style="background:{status_bg}; border:1px solid {status_border}; border-radius:10px; padding:16px; margin-bottom:16px;">
                        <span style="font-size:0.75rem; text-transform:uppercase; font-weight:700; color:{status_color};">Pathological Diagnosis</span>
                        <h3 style="margin:4px 0 0 0; color:{status_color}; font-weight:800;">{crop_name} • {condition}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Confidence and Model KPIs
                k1, k2 = st.columns(2)
                with k1:
                    st.metric("Model Confidence", f"{conf:.1f}%", f"{conf_level} Confidence")
                with k2:
                    st.metric("Backbone Architecture", res.get("model_name", "MobileNetV2"))

                # Grad-CAM Heatmap
                gradcam_b64 = res.get("gradcam_heatmap_base64")
                if gradcam_b64:
                    st.markdown("##### 🔍 Grad-CAM Visual Attention Saliency Map")
                    st.caption("Focal regions (red/yellow) indicate convolutional features driving the classification decision:")
                    st.image(
                        f"data:image/png;base64,{gradcam_b64}",
                        caption="Grad-CAM Saliency Overlay (Layer: features.18)",
                        use_column_width=True,
                    )

                # Alternative Classes
                alternatives = res.get("top_alternatives", [])
                if alternatives:
                    st.markdown("##### Alternative Class Likelihoods")
                    for alt in alternatives:
                        prob_pct = alt.get("probability", 0.0) * 100.0
                        st.progress(min(prob_pct / 100.0, 1.0))
                        st.caption(f"{alt.get('class_name')}: {prob_pct:.1f}%")

                # Agronomic Management Guidelines
                practices = res.get("management_practices", [])
                if practices:
                    st.markdown("##### 🛡️ Recommended Cultural Practices")
                    for p in practices:
                        st.markdown(f"- {p}")

                render_disclaimer(res.get("disclaimer", ""))
    elif uploaded_file is None:
        st.write("Upload a leaf photograph on the left to view the automated diagnosis, confidence rating, and Grad-CAM visual explanation.")

    st.markdown('</div>', unsafe_allow_html=True)

# Model Card & Literature Card
st.markdown('<div class="saas-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📚 Scientific Literature & Benchmark Architecture</h4>", unsafe_allow_html=True)
st.markdown(
    """
    - **Literature Reference**: Demilie, W.B. (2024). *Plant disease detection and classification techniques: a comparative study of the performances*, **Journal of Big Data (SpringerOpen)**, 11:71.
    - **Evaluated Architectures**: MobileNetV2 (depthwise separable convolutions) and EfficientNetB0 (compound scaling).
    - **Field Generalization**: Controlled laboratory benchmarks may exhibit performance variations in open Andhra Pradesh fields due to dust accumulation, high solar glare, or concurrent nutrient deficiencies.
    """
)
st.markdown('</div>', unsafe_allow_html=True)
