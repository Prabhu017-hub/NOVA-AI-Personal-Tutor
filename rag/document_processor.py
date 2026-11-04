import re
from pathlib import Path

from pypdf import PdfReader


# ==========================================
# 1. EXTRACT TEXT FROM PDF
# ==========================================

def extract_text_from_pdf(pdf_file):

    """
    Extract text from every page of a PDF.

    Accepts:
    - A PDF file path
    - A file-like object, such as Streamlit UploadedFile

    Returns:
    - List of dictionaries containing page text and metadata.
    """

    try:

        if isinstance(pdf_file, (str, Path)):
            reader = PdfReader(str(pdf_file))
            source_name = Path(pdf_file).name

        else:
            pdf_file.seek(0)
            reader = PdfReader(pdf_file)
            source_name = getattr(
                pdf_file,
                "name",
                "uploaded_document.pdf"
            )

        documents = []

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text() or ""

            text = clean_text(text)

            if text.strip():

                documents.append({
                    "text": text,
                    "metadata": {
                        "source": source_name,
                        "page": page_number
                    }
                })

        if not documents:
            raise ValueError(
                "No extractable text found in this PDF."
            )

        return documents

    except Exception as error:

        raise RuntimeError(
            f"PDF extraction failed: {error}"
        ) from error


# ==========================================
# 2. CLEAN PDF TEXT
# ==========================================

def clean_text(text):

    """
    Remove unnecessary whitespace and formatting.
    """

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


# ==========================================
# 3. SPLIT TEXT INTO CHUNKS
# ==========================================

def split_text_into_chunks(
    text,
    chunk_size=1000,
    overlap=150
):

    """
    Split text into smaller overlapping chunks.

    chunk_size: Maximum characters per chunk.
    overlap: Number of overlapping characters.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    text = clean_text(text)

    chunks = []

    start = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        # Try to end at a word boundary
        if end < len(text):

            boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# ==========================================
# 4. PROCESS PDF DOCUMENT
# ==========================================

def process_pdf(
    pdf_file,
    chunk_size=1000,
    overlap=150
):

    """
    Complete PDF processing pipeline.

    PDF -> Text Extraction -> Cleaning -> Chunking

    Returns:
    - List of text chunks
    - Corresponding metadata
    """

    pages = extract_text_from_pdf(pdf_file)

    all_chunks = []

    all_metadata = []

    for page in pages:

        page_chunks = split_text_into_chunks(
            page["text"],
            chunk_size,
            overlap
        )

        for chunk_number, chunk in enumerate(
            page_chunks,
            start=1
        ):

            all_chunks.append(chunk)

            metadata = page["metadata"].copy()

            metadata["chunk"] = chunk_number

            all_metadata.append(metadata)

    return all_chunks, all_metadata