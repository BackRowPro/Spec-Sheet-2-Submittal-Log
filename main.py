"""
6/10/2025
Gage Patty
This program is expected to receive Spec sheets as a PDF and convert them into a spreadsheet
that tracks all necessary submittals.
"""

import re
import os
import tempfile
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# 📄 Text cleaning function
def clean_text_spacing(text):
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', text)
    text = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', text)
    text = re.sub(r'([a-z])(?=[A-Z][a-z])', r'\1 ', text)
    text = re.sub(r'([A-Z]{2})([A-Z][a-z])', r'\1 \2', text)
    text = re.sub(r"(’s|'s)(?=[A-Za-z])", r"\1 ", text)
    text = re.sub(r":(?!\s)", ": ", text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r",(?!\s)", ", ", text)
    text = re.sub(r".(?!\s)", ". ", text)
    return text

# 🧠 Memory-safe OCR using Tesseract output to file
def run_safe_ocr(image):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
        image.save(temp_img.name)
        temp_img_path = temp_img.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_txt:
        temp_txt_path = temp_txt.name

    base_txt_path = temp_txt_path.rsplit(".", 1)[0]
    pytesseract.run_tesseract(
        temp_img_path,
        base_txt_path,
        extension='txt'
    )

    with open(base_txt_path + ".txt", "r", encoding='utf-8') as f:
        text = f.read()

    os.remove(temp_img_path)
    os.remove(base_txt_path + ".txt")
    return text

# 🔄 Convert PDF to image and extract text from each page
def extract_text_from_pdf(file_path):
    print("Running OCR...")
    
    pages = convert_from_path(
        file_path,
        dpi=300,
        poppler_path=r"C:\\Program Files\\poppler-24.08.0\\Library\\bin"
    )

    print("Converting...")
    all_text = ""

    for i, page in enumerate(pages):
        print(f"🖼️ Processing page {i + 1}...")
        text = run_safe_ocr(page)
        if text.strip():
            all_text += text + "\n\n"
        else:
            print(f"⚠️ OCR found no text on page {i + 1}")

    return all_text

# ✂️ Split by SECTION and filter for “submittal”
def split_and_filter_spec_sections(text):
    print("Splitting and filtering...")
    sections = re.split(r'(?=SECTION\s+\d{2}\s+\d{4})', text, flags=re.IGNORECASE)
    filtered_sections = []

    for sec in sections:
        if re.search(r'\bsubmittals?\b', sec, re.IGNORECASE):
            header_match = re.search(r'SECTION\s(\d{2}\s\d{4})\s*(.*)', sec)
            section_number = header_match.group(1) if header_match else "UNKNOWN"
            title = header_match.group(2).strip() if header_match else "NO TITLE"

            filtered_sections.append({
                'section_number': section_number,
                'title': title,
                'content': sec.strip()
            })

    print(f"✅ Found {len(filtered_sections)} section(s) mentioning 'submittal'")
    return filtered_sections

# 🚀 Main
def main():
    file_path = r"C:\\Github Projects\\Spec-Sheet-2-Submittal-Log\\2025.06.04 - Texas Aggies Corps of Cadets Association - Project Manual.pdf"
    pdf_text = extract_text_from_pdf(file_path)

    if not pdf_text.strip():
        print("❌ No extractable text found. PDF may be image-based.")
        return

    ocr_words = pdf_text.split()
    preview = " ".join(ocr_words[:500])
    print("\n🧠 First 500 OCR-extracted words (raw):\n")
    print(preview)

    cleaned_text = clean_text_spacing(pdf_text)
    filtered_sections = split_and_filter_spec_sections(cleaned_text)

    output_path = "filtered_submittals_log.txt"
    with open(output_path, "w", encoding="utf-8") as file:
        print("Writing results to file...")
        for sec in filtered_sections:
            file.write(f"SECTION {sec['section_number']}: {sec['title']}\n")
            file.write("-" * 40 + "\n")
            file.write(sec['content'] + "\n\n")

    print(f"✅ Output written to: {output_path}")

# 🧩 Run it
if __name__ == "__main__":
    main()
