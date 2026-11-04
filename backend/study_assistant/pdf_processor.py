import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path_or_buffer) -> tuple[str, int]:
    """
    Extracts text and page count from a PDF using PyMuPDF (fitz).
    Returns (extracted_text, total_pages).
    """
    try:
        import fitz  # PyMuPDF
        if hasattr(file_path_or_buffer, 'read'):
            doc = fitz.open(stream=file_path_or_buffer.read(), filetype="pdf")
        else:
            doc = fitz.open(file_path_or_buffer)

        total_pages = len(doc)
        text_parts = []
        for page_num in range(total_pages):
            page = doc[page_num]
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")

        extracted = "\n\n".join(text_parts)
        doc.close()
        return extracted, total_pages
    except Exception as e:
        logger.error(f"PyMuPDF extraction error: {e}")
        return f"Document content processed. Error details: {e}", 1
