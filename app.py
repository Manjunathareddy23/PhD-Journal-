import streamlit as st
from dotenv import load_dotenv
from gemini_engine import init_gemini, generate_with_plagiarism_control
from plagiarism import plagiarism_check

load_dotenv()

st.set_page_config(page_title="AI Journal Generator", layout="centered")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("AI-Assisted Academic Document Generator")

dataset = st.file_uploader("Upload Dataset (CSV)")
refs = st.file_uploader("Upload Reference Papers", accept_multiple_files=True)

if st.button("Generate Research Paper"):
    model = init_gemini()

    context = "Dataset insights and research problem description"
    references = ["sample extracted reference text"]

    sections = {}
    for sec in ["Abstract","Introduction","Methodology","Results","Conclusion"]:
        sections[sec] = generate_with_plagiarism_control(
            model, sec, context, references
        )

    st.success("Paper generated successfully!")
    for k,v in sections.items():
        st.subheader(k)
        st.write(v)
st.success("Made by Manjunathareddy💻")
