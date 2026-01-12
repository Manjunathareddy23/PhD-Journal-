import google.generativeai as genai
import os

def init_gemini():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemini-pro")

def generate_section(model, section_name, context):
    prompt = f"""
    You are an academic researcher.

    Write the {section_name} section of a Scopus-quality research paper.
    Constraints:
    - Original phrasing only
    - No plagiarism
    - Formal academic tone
    - Human-like writing
    - Avoid copying references directly

    Context:
    {context}
    """
    response = model.generate_content(prompt)
    return response.text
