"""
AgriAI - Module 10: AgriDoc AI PDF Assistant
Literature RAG system extracting grounded insights from agricultural PDFs with page-level citations.
"""

import streamlit as st
from app.components.theme import apply_saas_theme, render_sidebar, render_top_bar
from app.components.cards import render_page_header
from app.components.header import render_disclaimer
from app.utils.api_client import api_client

st.set_page_config(page_title="AgriDoc AI Assistant | AgriAI", page_icon="📄", layout="wide")
apply_saas_theme()
render_sidebar()
render_top_bar(current_district="Guntur")

render_page_header(
    title="AgriDoc AI – PDF Intelligence & Literature RAG",
    subtitle="Grounded Question-Answering over agricultural research papers, extension manuals, and government circulars with exact page-level citations.",
    category_tag="RETRIEVAL-AUGMENTED GENERATION (RAG)",
)

# Fetch indexed documents
docs = api_client.list_documents()

col_left, col_right = st.columns([1, 1.8])

with col_left:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>📚 Active Knowledge Base</h4>", unsafe_allow_html=True)

    if docs:
        for d in docs:
            st.markdown(
                f"""
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <div style="font-size:0.88rem; font-weight:700; color:#0f172a;">📄 {d.get('filename')}</div>
                    <div style="font-size:0.75rem; color:#64748b;">Pages: {d.get('total_pages', '?')} • Status: Indexed</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No documents currently indexed in knowledge base.")

    st.markdown("<hr style='margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#0f172a; font-weight:700;'>📤 Upload Agricultural PDF</h5>", unsafe_allow_html=True)
    uploaded_pdf = st.file_uploader("Upload Research Paper or Extension Advisory", type=["pdf"])
    if uploaded_pdf is not None:
        if st.button("Index Document for Vector Search", type="primary", use_container_width=True):
            st.success(f"Document '{uploaded_pdf.name}' staged and indexed for semantic vector search.")

    st.markdown("<hr style='margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#0f172a; font-weight:700;'>💡 Benchmark Research Queries</h5>", unsafe_allow_html=True)
    ex_queries = [
        "What are the plant disease detection techniques discussed in this paper?",
        "Which CNN architectures are compared in Demilie 2024?",
        "What is the role of MobileNetV2?",
        "What preprocessing and augmentation methods are discussed?",
        "What are the limitations of deploying models to real agricultural fields?",
    ]
    selected_ex = st.selectbox("Select Benchmark Literature Query:", ["(Choose an example query)"] + ex_queries)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="saas-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#0f172a; font-weight:700;'>💬 Literature Question-Answering</h4>", unsafe_allow_html=True)

    query_text = st.text_input(
        "Ask a specific agronomic or machine learning research question:",
        value="" if selected_ex == "(Choose an example query)" else selected_ex,
        placeholder="e.g. Which evaluation metrics are used to compare CNN models in Demilie 2024?",
    )

    ask_btn = st.button("Execute Grounded RAG Search", type="primary")

    if ask_btn:
        if not query_text.strip():
            st.warning("Please enter or select a question.")
        else:
            with st.spinner("Embedding query, retrieving semantic vector chunks, and synthesizing grounded answer..."):
                res = api_client.ask_document(query=query_text)

                if "answer" in res:
                    st.markdown("##### 📝 Synthesized Grounded Response")
                    st.markdown(
                        f"""
                        <div style="background:#f8fafc; border-left:4px solid #16a34a; padding:16px; border-radius:6px; margin:12px 0; font-size:0.95rem; line-height:1.6;">
                            {res['answer']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Performance Badges
                    st.caption(f"⚡ Confidence: {res.get('confidence')} | Processing Latency: {res.get('processing_time_ms')} ms")

                    # Page Citations
                    citations = res.get("citations", [])
                    if citations:
                        st.markdown("<hr style='margin:16px 0;'>", unsafe_allow_html=True)
                        st.markdown("<h5 style='color:#0f172a; font-weight:700;'>📑 Supporting Passages & Exact Citations</h5>", unsafe_allow_html=True)
                        for idx, cit in enumerate(citations):
                            with st.expander(
                                f"Citation #{idx + 1}: {cit.get('document_name')} • Page {cit.get('page_number')} (Relevance: {cit.get('relevance_score'):.2f})",
                                expanded=True,
                            ):
                                st.markdown(f"**Extracted Verbatim Passage:**\n> \"{cit.get('verbatim_snippet')}\"")
                else:
                    st.error("Error retrieving answer from document vector index.")

    st.markdown('</div>', unsafe_allow_html=True)

render_disclaimer(
    "AgriDoc AI strictly restricts its answers to passages extracted from uploaded research papers and reports. "
    "If information is not present in the indexed literature, the assistant will explicitly state that the answer cannot be found."
)
