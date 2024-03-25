#from pdfminer.high_level import extract_pages 
from pdfminer.layout import LTTextContainer, LTChar, LTAnno
import fitz 
from summarization_pipeline.article_parser import divide_article_into_sections
import re

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

def capture_image_titles(extracted_text):
    # Define the possible representations of figure and table names
    figure_patterns = ["Fig\.", "Figure"]
    table_patterns = ["Table"]

    # Combine the patterns into regex patterns
    figure_pattern = "|".join(figure_patterns)
    table_pattern = "|".join(table_patterns)

    # Create a regex pattern to capture the figure and table titles
    figure_title_pattern = f"({figure_pattern})\s*(\d+)\.\s*(.*?)\."
    table_title_pattern = f"({table_pattern})\s*(\d+)\s*\\n?\s*(.*?)\."

    # Find all matches in the extracted_text for figures and tables
    figure_matches = re.findall(figure_title_pattern, extracted_text)
    table_matches = re.findall(table_title_pattern, extracted_text)

    # Initialize lists to store figure and table titles
    titles = []

    # Process and store the matched titles and numberings from the figures
    for match in figure_matches:
        title_type, title_number, title_text = match
        if title_text != "":
            if ('A' <= title_text[0] and title_text[0] <= "Z") or ('0' <= title_text[0] and title_text[0] <= '9'):
                titles.append(f"{title_type} {title_number}. {title_text}")

    # Process and store the matched titles and numberings from the tables
    for match in table_matches:
        title_type, title_number, title_text = match
        if title_text != "":
            if ('A' <= title_text[0] and title_text[0] <= "Z") or ('0' <= title_text[0] and title_text[0] <= '9'):
                titles.append(f"{title_type} {title_number}. {title_text}")

    return titles

"""
The PDF article is extracted as a whole, without being divided into sections
"""
def extract_pdf(path):
    extracted_text = extract_text_from_pdf(path)
    return extracted_text

"""
The PDF article is extracted and divided into sections
"""
def extract_pdf_and_divide_sections(path):
    extracted_text = extract_text_from_pdf(path)
    parsed_sections = divide_article_into_sections(extracted_text)
    return parsed_sections