
import pymupdf
import pytesseract
import io

from pathlib import Path
from PIL import Image
from langchain_core.documents import Document


# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

DATA_DIR = Path("data/acts")


def extract_pdf_text(pdf_path):

    documents = []

    pdf = pymupdf.open(pdf_path)

    for page_number, page in enumerate(pdf, start=1):

        # Extract embedded text
        text = page.get_text("text").strip()

        # OCR fallback for scanned pages
        if len(text) < 50:

            pix = page.get_pixmap(dpi=250)

            image = Image.open(
                io.BytesIO(pix.tobytes("png"))
            )

            text = pytesseract.image_to_string(
                image,
                lang="eng"
            ).strip()

        if not text:
            print(
                f"Warning: No text extracted from "
                f"{pdf_path.name}, page {page_number}"
            )
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": pdf_path.name,
                    "page": page_number,
                    "document_type": "consumer_law"
                }
            )
        )

    pdf.close()

    return documents


def load_legal_documents():

    all_documents = []

    for pdf_path in DATA_DIR.glob("*.pdf"):

        print(f"\nProcessing: {pdf_path.name}")

        pages = extract_pdf_text(pdf_path)

        all_documents.extend(pages)

        print(f"Pages extracted: {len(pages)}")

    print(f"\nTotal extracted pages: {len(all_documents)}")

    return all_documents
