---
name: pdf_skill
description: PDF text extraction and information retrieval.
allowed-tools:
  - extract_text_from_pdf
  - extract_pages_from_pdf
  - get_pdf_info
  - convert_pdf_to_text_file
---

# PDF Skill

This skill enables the agent to extract text and metadata from PDF files.

## Tools

### extract_text_from_pdf
Extract all text from a PDF file.

- `file_path`: Absolute path to the PDF file.
- Returns the extracted text as a string.

### extract_pages_from_pdf
Extract text from specific pages of a PDF.

- `file_path`: Absolute path to the PDF file.
- `page_numbers`: List of page numbers (1‑based).
- Returns the concatenated text of those pages.

### get_pdf_info
Retrieve metadata and basic information about a PDF.

- `file_path`: Absolute path to the PDF file.
- Returns a dictionary with keys: num_pages, author, title, etc.

### convert_pdf_to_text_file
Convert a PDF to a plain text file.

- `file_path`: Absolute path to the PDF file.
- `output_path`: Path where the text file will be saved.
- Returns a success message.
