import streamlit as st
from dotenv import load_dotenv
import os

from gemini_engine import init_gemini, generate_with_plagiarism_control

load_dotenv()

st.set_page_config(page_title="AI Journal Generator", layout="centered")

# 🔹 FIX: Robust path handling 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(BASE_DIR, "assets", "style.css")

if os.path.exists(CSS_PATH):
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("CSS file not found. Running without custom styling.")

st.title("AI-Assisted Academic Document Generator")
