import fitz  # PyMuPDF
from io import BytesIO

def extract_text_from_pdf(uploaded_file):
    pdf_data = uploaded_file.read()
    pdf_stream = BytesIO(pdf_data)

    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")

    # Debug: Print out the first 500 characters to inspect the text
    print(f"Extracted text: {text[:500]}")  # Adjust the length for your needs
    return text
