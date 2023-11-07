from pdfminer.high_level import extract_pages 
from pdfminer.layout import LTTextContainer, LTChar, LTAnno
import fitz 
import article_parser

def clean_text(text):
    """
    Function to clean the extracted text.
    This function may need to be modified based on the specific 'noises' you encounter in your PDFs.
    """
    # Remove page numbers
    text = text[4].split('\n')
    text = [line for line in text if not line.isdigit()]
    # Joining text
    text = '\n'.join(text)
    return text

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file and clean it.
    """
    # Open the provided PDF file
    doc = fitz.open(pdf_path)
    full_text = ""
    # Iterate over each page
    for page_num in range(len(doc)):   
        # Get a page
        page = doc.load_page(page_num)
        # Extract text from the page
        blocks = page.get_text("blocks")
        for block in blocks:
            # Clean the extracted text
            text = clean_text(block)
            #print(text)
            # Append cleaned text
            full_text += text
    # Close the document
    doc.close()
    return full_text

def extract_pdf_and_divide_sections(path):
    extracted_text = extract_text_from_pdf(path)
    #print(extracted_text[20000:30000])
    parsed_sections = article_parser.divide_article_into_sections(extracted_text)
    return parsed_sections