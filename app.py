import streamlit as st
from dotenv import load_dotenv
import os
from formatter import generate_docx, generate_pdf

from gemini_engine import init_gemini, generate_with_plagiarism_control

load_dotenv()

st.set_page_config(page_title="AI Journal Generator", layout="centered")

# ---- CSS LOADING (ROBUST) ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(BASE_DIR, "assets", "style.css")

if os.path.exists(CSS_PATH):
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("CSS file not found. Running without custom styling.")

# ---- UI ----
st.title("AI-Assisted Academic Document Generator")

context = st.text_area("Enter Research Context / Dataset Summary")
references_text = st.text_area(
    "Paste Reference Texts (separate by ---)",
    help="Paste reference content, separated by ---"
)

if st.button("Generate Paper"):
    model = init_gemini()
    references = references_text.split("---")

    sections = {}
    for sec in ["Abstract", "Introduction", "Methodology", "Results", "Conclusion"]:
        sections[sec] = generate_with_plagiarism_control(
            model, sec, context, references
        )

    st.success("Paper generated successfully!")

    for k, v in sections.items():
        st.subheader(k)
        st.write(v)
