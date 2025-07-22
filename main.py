"""
6/10/2025
Gage Patty
This program is expected to receive Spec sheets as a PDF and convert them into a spreadsheet
that tracks all necessary submittals.
"""

import re
import pdfplumber

def clean_text_spacing(text):
    # Space between lowercase and uppercase: workItems → work Items
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)

    # Space between letters and digits, and vice versa: Mix3 → Mix 3
    text = re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', text)
    text = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', text)

    # Space between lowercase + capital word mashups: SectionIncludes → Section Includes
    text = re.sub(r'([a-z])(?=[A-Z][a-z])', r'\1 ', text)

    # Space between acronym and TitleCase: ASTMTestResults → ASTM TestResults
    text = re.sub(r'([A-Z]{2})([A-Z][a-z])', r'\1 \2', text)

    # ✅ Add space after possessive 's or ’s ONLY when followed by a capital letter (Owner’sContingency → Owner’s Contingency)
    text = re.sub(r"(’s|'s)(?=[A-Za-z])", r"\1 ", text)

    # ✅ Add space after every colon
    text = re.sub(r":(?!\s)", ": ", text)

    # Collapse long spaces just in case
    text = re.sub(r'\s{2,}', ' ', text)

    text = re.sub(r",(?!\s)", ", ", text)

    text = re.sub(r".(?!\s)", ". ", text)

    return text

from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

# 🔄 Replace this function
def extract_text_from_pdf(file_path):
    print("Running OCR...")
    
    # If necessary, set tesseract path
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    pages = convert_from_path(file_path, dpi=300)
    all_text = ""

    for i, page in enumerate(pages):
        print(f"🖼️ Processing page {i + 1}...")
        text = pytesseract.image_to_string(page)
        if text.strip():
            all_text += text + "\n\n"
        else:
            print(f"⚠️ OCR found no text on page {i + 1}")

    return all_text

# ✂️ Splits into SECTION blocks and filters ones mentioning "submittal"
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

# 🚀 Main entry point
def main():
    file_path = r"C:\Github Projects\Spec-Sheet-2-Submittal-Log\2025.06.04 - Texas Aggies Corps of Cadets Association - Project Manual.pdf"
    pdf_text = extract_text_from_pdf(file_path)

    if not pdf_text.strip():
        print("❌ No extractable text found. PDF may be image-based.")
        return

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

# ✅ Standard script entry
if __name__ == "__main__":
    main()
