import fitz  # PyMuPDF

PDF_PATH = "data\DH-Chapter2 (1).pdf"

def extract_pdf_text_by_page(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages = []

    for i in range(doc.page_count):
        page = doc.load_page(i)

        # Method 1: normal text
        text = page.get_text("text")

        # If it extracted almost nothing, try method 2: blocks (often better)
        if len(text.strip()) < 200:
            blocks = page.get_text("blocks")
            # blocks: list of tuples, where block[4] is the text
            text = " ".join((b[4] for b in blocks if isinstance(b[4], str)))

        # light cleanup
        text = " ".join(text.split())

        pages.append({"page": i + 1, "text": text})

    doc.close()
    return pages

if __name__ == "__main__":
    pages = extract_pdf_text_by_page(PDF_PATH)

    print("Total pages:", len(pages))
    print("Page 1 length:", len(pages[0]["text"]))
    print("Page 2 length:", len(pages[1]["text"]))
    print("Page 2 preview:\n", pages[1]["text"][:800])