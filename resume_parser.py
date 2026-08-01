from pathlib import Path

from docx import Document
from pypdf import PdfReader


MAX_FILE_SIZE_MB = 5


def _check_file_size(uploaded_file):
    # Streamlit upload objects behave like files, so seek/tell can be used to check size.
    uploaded_file.seek(0, 2)
    size_mb = uploaded_file.tell() / (1024 * 1024)
    uploaded_file.seek(0)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"File size should be below {MAX_FILE_SIZE_MB} MB")


def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text_parts = []
    for page in reader.pages:
        # Some PDF pages return None when they contain scanned images instead of selectable text.
        text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def extract_docx_text(uploaded_file):
    document = Document(uploaded_file)
    paragraphs = [para.text for para in document.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)


def extract_resume_text(uploaded_file):
    _check_file_size(uploaded_file)

    # The file extension decides which parser should handle the uploaded resume.
    file_name = uploaded_file.name.lower()
    suffix = Path(file_name).suffix

    if suffix == ".pdf":
        return extract_pdf_text(uploaded_file)
    if suffix == ".docx":
        return extract_docx_text(uploaded_file)

    raise ValueError("Only PDF and DOCX files are supported")
