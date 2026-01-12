import streamlit as st
from dotenv import load_dotenv
import os
import time

from gemini_engine import init_gemini, generate_with_plagiarism_control
from formatter import generate_docx, generate_pdf

# --------------------------------------------------
# ENV & PAGE CONFIG
# --------------------------------------------------
load_dotenv()
st.set_page_config(page_title="AI Journal Generator", layout="centered")

# --------------------------------------------------
# CSS LOADING (SAFE)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(BASE_DIR, "assets", "style.css")

if os.path.exists(CSS_PATH):
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE & INPUTS
# --------------------------------------------------
st.title("AI-Assisted Academic Document Generator")

context = st.text_area(
    "Enter Research Context / Dataset Summary",
    height=150
)

references_text = st.text_area(
    "Paste Reference Texts (separate by ---)",
    height=150
)

references = references_text.split("---")

# --------------------------------------------------
# SESSION STATE (CRITICAL)
# --------------------------------------------------
if "model" not in st.session_state:
    st.session_state.model = init_gemini()

if "sections" not in st.session_state:
    st.session_state.sections = {}

if "cooldown_until" not in st.session_state:
    st.session_state.cooldown_until = 0

# --------------------------------------------------
# SECTION SELECTOR
# --------------------------------------------------
section_to_generate = st.selectbox(
    "Select section to generate",
    ["Abstract", "Introduction", "Methodology", "Results", "Conclusion"]
)

# --------------------------------------------------
# COOLDOWN HANDLING
# --------------------------------------------------
now = time.time()
if now < st.session_state.cooldown_until:
    remaining = int(st.session_state.cooldown_until - now)
    st.warning(f"⏳ Gemini quota cooldown active. Retry in {remaining} seconds.")
    st.stop()

# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------
if st.button("Generate Selected Section"):
    if not context.strip():
        st.error("Please enter research context.")
        st.stop()

    with st.spinner(f"Generating {section_to_generate}..."):
        try:
            text = generate_with_plagiarism_control(
                st.session_state.model,
                section_to_generate,
                context,
                references
            )
            st.session_state.sections[section_to_generate] = text
            st.success(f"{section_to_generate} generated successfully!")

        except RuntimeError as e:
            # QUOTA EXCEEDED
            if "QUOTA_EXCEEDED" in str(e) or "429" in str(e):
                st.session_state.cooldown_until = time.time() + 45
                st.error("⚠️ Gemini free quota exhausted.")
                st.info("⏳ Please wait ~45 seconds before retrying.")
                st.stop()
            else:
                st.error(str(e))
                st.stop()

# --------------------------------------------------
# DISPLAY GENERATED CONTENT
# --------------------------------------------------
st.divider()
st.subheader("Generated Sections")

if not st.session_state.sections:
    st.info("No sections generated yet.")
else:
    for title, content in st.session_state.sections.items():
        st.markdown(f"### {title}")
        st.write(content)

# --------------------------------------------------
# DOWNLOAD OPTIONS
# --------------------------------------------------
if st.session_state.sections:
    st.divider()
    st.subheader("Download Document")

    docx_file = generate_docx(st.session_state.sections)
    pdf_file = generate_pdf(st.session_state.sections)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_file,
            file_name="ai_generated_paper.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    with col2:
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_file,
            file_name="ai_generated_paper.pdf",
            mime="application/pdf"
        )
