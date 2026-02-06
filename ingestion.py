import fitz  # PyMuPDF
from docx import Document


def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def read_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)


def read_txt(file):
    return file.read().decode("utf-8")


def extract_text(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return read_pdf(uploaded_file)

    if name.endswith(".docx"):
        return read_docx(uploaded_file)

    if name.endswith(".txt"):
        return read_txt(uploaded_file)

    return ""
