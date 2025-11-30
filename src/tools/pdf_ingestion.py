"""PDF ingestion tool for extracting text from policy documents."""

from typing import Dict, Any
import PyPDF2
import io


def extract_text_from_pdf(pdf_content: bytes) -> Dict[str, Any]:
    """
    Extract text content from PDF file.
    
    Args:
        pdf_content: PDF file as bytes
        
    Returns:
        Dictionary with status and extracted text
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        
        return {
            "status": "success",
            "text": text,
            "page_count": len(pdf_reader.pages)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to extract text from PDF: {str(e)}"
        }


def parse_policy_structure(policy_text: str) -> Dict[str, Any]:
    """
    Parse policy text into structured sections.
    
    Args:
        policy_text: Raw text from policy document
        
    Returns:
        Dictionary with parsed sections and requirements
    """
    # Simple parser - in production, use more sophisticated NLP
    sections = {}
    current_section = None
    
    for line in policy_text.split('\n'):
        line = line.strip()
        if line.startswith('SECTION'):
            current_section = line
            sections[current_section] = []
        elif current_section and line:
            sections[current_section].append(line)
    
    return {
        "status": "success",
        "sections": sections,
        "total_sections": len(sections)
    }