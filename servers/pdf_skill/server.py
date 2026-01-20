import json
import os
import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pdf_skill", log_level="ERROR")

# Try to import PyPDF2, fallback to pdfplumber or error
try:
    import PyPDF2

    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import pdfplumber

    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

if not HAS_PYPDF2 and not HAS_PDFPLUMBER:
    mcp.logger.error(
        "Neither PyPDF2 nor pdfplumber is installed. PDF skill will not work."
    )


@mcp.tool()
def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract all text from a PDF file.

    Args:
        file_path: Absolute path to the PDF file.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"

    try:
        if HAS_PDFPLUMBER:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        elif HAS_PYPDF2:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        else:
            return (
                "Error: No PDF library available. Please install PyPDF2 or pdfplumber."
            )
    except Exception as e:
        return f"Error extracting text: {e}"


@mcp.tool()
def extract_pages_from_pdf(file_path: str, page_numbers: str) -> str:
    """
    Extract text from specific pages of a PDF.

    Args:
        file_path: Absolute path to the PDF file.
        page_numbers: JSON list of page numbers (1‑based).
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"

    try:
        pages = json.loads(page_numbers)
        if not isinstance(pages, list):
            return "Error: page_numbers must be a list."

        if HAS_PDFPLUMBER:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for i, page in enumerate(pdf.pages, start=1):
                    if i in pages:
                        text += page.extract_text() + "\n"
                return text.strip()
        elif HAS_PYPDF2:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for i, page in enumerate(reader.pages, start=1):
                    if i in pages:
                        text += page.extract_text() + "\n"
                return text.strip()
        else:
            return "Error: No PDF library available."
    except json.JSONDecodeError:
        return "Error: Invalid JSON for page_numbers."
    except Exception as e:
        return f"Error extracting pages: {e}"


@mcp.tool()
def get_pdf_info(file_path: str) -> str:
    """
    Retrieve metadata and basic information about a PDF.

    Args:
        file_path: Absolute path to the PDF file.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"

    try:
        info = {}
        if HAS_PDFPLUMBER:
            with pdfplumber.open(file_path) as pdf:
                info["num_pages"] = len(pdf.pages)
                # pdfplumber doesn't expose metadata directly, fallback to PyPDF2
                pass
        if HAS_PYPDF2:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                info["num_pages"] = len(reader.pages)
                if reader.metadata:
                    info["author"] = reader.metadata.get("/Author", "")
                    info["title"] = reader.metadata.get("/Title", "")
                    info["subject"] = reader.metadata.get("/Subject", "")
                    info["creator"] = reader.metadata.get("/Creator", "")
                    info["producer"] = reader.metadata.get("/Producer", "")
                    info["creation_date"] = reader.metadata.get("/CreationDate", "")
                    info["modification_date"] = reader.metadata.get("/ModDate", "")
        if not info:
            return "Error: No PDF library available."
        return json.dumps(info, ensure_ascii=False)
    except Exception as e:
        return f"Error reading PDF info: {e}"


@mcp.tool()
def convert_pdf_to_text_file(file_path: str, output_path: str) -> str:
    """
    Convert a PDF to a plain text file.

    Args:
        file_path: Absolute path to the PDF file.
        output_path: Path where the text file will be saved.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"

    try:
        text = ""
        if HAS_PDFPLUMBER:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        elif HAS_PYPDF2:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        else:
            return "Error: No PDF library available."

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return f"Successfully saved text to {output_path}"
    except Exception as e:
        return f"Error converting PDF: {e}"


if __name__ == "__main__":
    mcp.run()
