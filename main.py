"""
6/10/2025
Gage Patty
This program is expected to recieve Spec sheets as a PDF and convert them into a spreadsheet
that tracks all neccessary submittals
"""

import re

import pdfplumber

def extract_text_from_pdf(file_path):
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n\n"
    return full_text

pdf_text = extract_text_from_pdf("2025.06.04 - Texas Aggies Corps of Cadets Association - Project Manual.pdf")


def split_and_filter_spec_sections(text):
    # Split at "SECTION xx xxxx"
    sections = re.split(r'(?=SECTION\s\d{2}\s\d{4})', pdf_text)
    
    filtered_sections = []
    
    for sec in sections:
        if 'submittal' in sec.lower():
            # Extract section number and title
            header_match = re.search(r'SECTION\s(\d{2}\s\d{4})\s*(.*)', sec)
            section_number = header_match.group(1) if header_match else "UNKNOWN"
            title = header_match.group(2).strip() if header_match else "NO TITLE"

            filtered_sections.append({
                'section_number': section_number,
                'title': title,
                'content': sec.strip()
            })

    return filtered_sections

print(split_and_filter_spec_sections(extract_text_from_pdf(pdf_text)))
