import fitz  # PyMuPDF

PDF_PATH = "data\DH-Chapter2 (1).pdf"

doc = fitz.open(PDF_PATH)
print("PDF opened ✅")
print("Pages:", doc.page_count)
print("First page preview:")
print(doc[0].get_text()[:500])
doc.close()