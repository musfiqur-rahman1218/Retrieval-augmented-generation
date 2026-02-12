import fitz  # PyMuPDF

PDF_PATH = "data\DH-Chapter2 (1).pdf"

def extract_pdf_text_by_page(pdf_path: str) -> list[dict]:
    """
    Returns a list of dicts like:
    [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}]
    """
    doc = fitz.open(pdf_path)
    pages = []

    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text("text")  # plain text extraction
        # light cleanup
        text = " ".join(text.split())
        pages.append({"page": i + 1, "text": text})

    doc.close()
    return pages

if __name__ == "__main__":
    pages = extract_pdf_text_by_page(PDF_PATH)

    print("Total pages:", len(pages))
    print("Page 1 length:", len(pages[0]["text"]))
    print("Page 1 preview:\n", pages[0]["text"][:800])