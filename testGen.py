from PyPDF2 import PdfReader, PdfWriter

def create_test_pdf(input_path, output_path, start=20, end=80):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i in range(start, min(end, len(reader.pages))):
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)

# Use your real file path here
create_test_pdf(
    r"C:\Github Projects\Spec-Sheet-2-Submittal-Log\2025.06.04 - Texas Aggies Corps of Cadets Association - Project Manual.pdf",
    r"C:\Github Projects\Spec-Sheet-2-Submittal-Log\TEST_AggieShort.pdf",
    start=20,
    end=80
)
