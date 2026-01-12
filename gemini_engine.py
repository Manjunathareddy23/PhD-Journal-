from plagiarism import plagiarism_check
from gemini_engine import generate_section   # if same file, remove this import

def generate_with_plagiarism_control(model, section, context, references):
    """
    Algorithm 1: Plagiarism-aware academic text generation

    Inputs:
        model      → Gemini LLM instance
        section    → Paper section name
        context    → Dataset + research context
        references → Extracted reference texts

    Output:
        Original, plagiarism-safe academic content
    """

    for iteration in range(3):   # bounded regeneration
        text = generate_section(model, section, context)

        flagged, score = plagiarism_check(text, references)

        if not flagged:
            return text

        # Adaptive prompt refinement
        context += (
            "\nRewrite with higher originality, "
            "use different sentence structure, "
            "avoid semantic overlap."
        )

    return text
