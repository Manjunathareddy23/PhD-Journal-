import google.generativeai as genai
import os
from plagiarism import plagiarism_check


def init_gemini():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # 🔍 Find a usable text generation model
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            # Pick the FIRST available text model
            return genai.GenerativeModel(model.name)

    raise RuntimeError("No Gemini text generation model available for this API key")


def generate_section(model, section_name, context):
    prompt = f"""
You are an academic researcher.

Write the {section_name} section of a Scopus-quality research paper.

Rules:
- Original phrasing only
- No plagiarism
- Formal academic tone
- Human-like writing
- Deep paraphrasing, not rewriting

Context:
{context}
"""
    response = model.generate_content(prompt)
    return response.text


def generate_with_plagiarism_control(model, section, context, references):
    """
    Algorithm 1: Plagiarism-aware academic text generation
    """

    for _ in range(3):
        text = generate_section(model, section, context)

        flagged, score = plagiarism_check(text, references)
        if not flagged:
            return text

        context += (
            "\nRewrite with higher originality, "
            "change sentence structure, "
            "reduce semantic similarity."
        )

    return text
