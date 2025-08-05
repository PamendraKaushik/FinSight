
import pdfplumber
from tools.vector_store import build_store

def extract_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def process_document(text):
    build_store([text])
    return "Document processed."