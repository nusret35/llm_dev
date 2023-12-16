import fitz
from PIL import Image
import os
import re

# Creates the regex pattern for figures and tables for pages
def regex_for_figure_and_table():
    figure_patterns = ["Fig\.", "Figure"]
    table_patterns = ["Table"]

    # Combine the patterns into regex patterns
    figure_pattern = "|".join(figure_patterns)
    table_pattern = "|".join(table_patterns)

    figure_title_pattern = f"({figure_pattern})\s*(\d+)\.\s*(.*?)\."
    table_title_pattern = f"({table_pattern})\s*(\d+)\s*\\n?\s*(.*?)\."

    return figure_title_pattern, table_title_pattern


def response_regex_for_figure_and_table():
    # Define the possible representations of figure and table names
    figure_patterns = ["Fig\."]
    table_patterns = ["Table"]

    # Combine the patterns into regex patterns
    figure_pattern = "|".join(figure_patterns)
    table_pattern = "|".join(table_patterns)

    # Create a regex pattern to capture the figure and table titles
    figure_title_pattern = f"({figure_pattern}\s*\d+)\.\s*(.*?) \(Page:(\d+)\) - (.*)"
    table_title_pattern = f"({table_pattern}\s*\d+)\.\s*(.*?) \(Page:(\d+)\) - (.*)"

    return figure_title_pattern, table_title_pattern


# Creates the regex pattern for response figure and table titles
def match_figure_and_table(block_text,figure_title_pattern, table_title_pattern):
    # Find all matches in the extracted_text for figures and tables
    titles = []
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


# Extracts images and their titles from PDF page
def extract_image_title_pairs(page, page_index):
    image_list = page.get_image_info()
    text_blocks = page.get_text("blocks")

    figure_title_pattern, table_title_pattern = regex_for_figure_and_table()

    proximity_threshold = 150  # Adjust this value based on your requirements

    titles = []
    image_paths = []

    img_index = 0
    for img in image_list:
        bbox = img['bbox']
        left, top, right, bottom = bbox[0], bbox[1], bbox[2], bbox[3]

        # Get the image data from the bounding box
        image = page.get_pixmap(matrix=fitz.Matrix(1, 1).prescale(2, 2), clip=(left, top, right, bottom))

        # Convert the image data to a Pillow image
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        directory_path = "./images/" + 'page' + str(page_index+1)
        os.makedirs(directory_path, exist_ok=True)

        img_path = directory_path + '/output_image' + str(img_index) + '.png'
        image_paths.append(img_path)

        # Save or process the image as needed
        pil_image.save(img_path)

        # Search for text near the image
        for block in text_blocks:
            block_bbox = block[0:4]
            block_left, block_top, block_right, block_bottom = block_bbox

            # Check if the text block is within proximity of the image
            if (left - proximity_threshold <= block_right <= right + proximity_threshold) and \
               (top - proximity_threshold <= block_bottom <= bottom + proximity_threshold):

                # Check if the first word of the text block is in the list of keywords
                block_text = block[4]
                figure_title_pattern, table_title_pattern = regex_for_figure_and_table()
                titles = titles + match_figure_and_table(block_text,figure_title_pattern,table_title_pattern)

    
    image_data = dict(zip(titles, image_paths))
    return image_data


# Extracts all the titles (Figure, Table, etc.) from PDF page
def extract_titles_from_page(page):

    figure_title_pattern, table_title_pattern = regex_for_figure_and_table()

    text_blocks = page.get_text("blocks")

    # Initialize lists to store figure and table titles
    titles = []
    
    for block in text_blocks:
        block_text = block[4]
        figure_title_pattern, table_title_pattern = regex_for_figure_and_table()
        titles = titles + match_figure_and_table(block_text,figure_title_pattern,table_title_pattern)

    return titles


def convert_response_to_list(response_text):
    figure_title_pattern, table_title_pattern = response_regex_for_figure_and_table()

    titles = []

    # Find all matches in the extracted_text for figures and tables
    figure_matches = re.findall(figure_title_pattern, response_text)
    table_matches = re.findall(table_title_pattern, response_text)

    # Process and store the matched titles and numberings from the figures
    for match in figure_matches:
        image_name, image_title, image_page_number, explanation = match
        if image_name != "":
            if ('A' <= image_name[0] and image_name[0] <= "Z") or ('0' <= image_name[0] and image_name[0] <= '9'):
                titles.append((f"{image_name}. {image_title}", explanation, image_page_number))

    # Process and store the matched titles and numberings from the tables
    for match in table_matches:
        image_name, image_title, image_page_number, explanation = match
        if image_name != "":
            if ('A' <= image_name[0] and image_name[0] <= "Z") or ('0' <= image_name[0] and image_name[0] <= '9'):
                titles.append((f"{image_name}. {image_title}", explanation, image_page_number))

    # Return an list of 3 variable tuples (title, explanation, page_number)

    return titles


# image_title_pairs: dictionary of the images that are extracted
# important_images: list of important image titles. List of tuples.
# Returns the extracted important images
def get_important_image_paths(image_title_pairs, important_images):
    # Check whether the important image is extracted
    found_important_images_paths = {}
    for title, explanation, page_number in important_images:
        if title in image_title_pairs.keys():
            found_important_images_paths.update({title:image_title_pairs[title]})
                
    return found_important_images_paths


##TEST##

if __name__ == "__main__":
    # File path
    #file = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/1-s2.0-S0148296323004216-main.pdf"
    file = '/Users/nusretkizilaslan/Downloads/selo-article.pdf'
    file1 = '/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/buss_article.pdf'
    file2 = '/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/buss_article_2.pdf'

    # Open the file
    pdf_file = fitz.open(file)

    image_title_pairs = {}
    titles = []
    # Iterate over PDF pages
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        page_image_title_pairs = extract_image_title_pairs(page,page_index)
        page_image_titles = extract_titles_from_page(page)
        image_title_pairs.update(page_image_title_pairs)
        for title in page_image_titles:
            title += " (Page:" + str(page_index+1) + ")"
            titles.append(title)
    
    print(image_title_pairs)
    print()
    print(titles)

    pdf_file.close()