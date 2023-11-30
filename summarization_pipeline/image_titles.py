import fitz
import re

def extract_titles_from_page(page):
    
    # Define the possible representations of figure and table names
    figure_patterns = ["Fig\.", "Figure"]
    table_patterns = ["Table"]

    # Combine the patterns into regex patterns
    figure_pattern = "|".join(figure_patterns)
    table_pattern = "|".join(table_patterns)

    # Create a regex pattern to capture the figure and table titles
    figure_title_pattern = f"({figure_pattern})\s*(\d+)\.\s*(.*?)\."
    table_title_pattern = f"({table_pattern})\s*(\d+)\s*\\n?\s*(.*?)\."

    text_blocks = page.get_text("blocks")

    # Initialize lists to store figure and table titles
    titles = []
    
    for block in text_blocks:
        block_text = block[4]
        
        # Find all matches in the extracted_text for figures and tables
        figure_matches = re.findall(figure_title_pattern, block_text)
        table_matches = re.findall(table_title_pattern, block_text)

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


# File path

#file = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/1-s2.0-S0148296323004216-main.pdf"
file = '/Users/nusretkizilaslan/Downloads/selo-article.pdf'
file1 = '/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/buss_article.pdf'
file2 = '/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/buss_article_2.pdf'

# Open the file
pdf_file = fitz.open(file)

titles = []

# Iterate over PDF pages
for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    page_image_titles = extract_titles_from_page(page)
    for title in page_image_titles:
        title += " (Page:" + str(page_index+1) + ")"
        titles.append(title)

pdf_file.close()

