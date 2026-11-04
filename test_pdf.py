from rag.document_processor import process_pdf

print("=" * 50)
print("       NOVA PDF PROCESSING TEST")
print("=" * 50)

pdf_path = input("\nEnter PDF file path: ").strip().strip('"')

try:

    chunks, metadata = process_pdf(pdf_path)

    print("\nPDF processed successfully!")

    print("Total chunks:", len(chunks))

    print("\nFirst chunk:")
    print(chunks[0])

    print("\nFirst chunk metadata:")
    print(metadata[0])

    print("\nNOVA PDF processing is working!")

except Exception as error:

    print("\nError:", error)