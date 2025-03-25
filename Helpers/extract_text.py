import sys
sys.stdout.reconfigure(encoding='utf-8')

import pymupdf

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text