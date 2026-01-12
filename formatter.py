from docx import Document

def generate_docx(sections):
    doc = Document()
    for title, content in sections.items():
        doc.add_heading(title, level=1)
        doc.add_paragraph(content)
    return doc
