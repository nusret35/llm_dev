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
    images = []

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


        images.append(pil_image)

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

    image_data = dict(zip(titles, images))
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


def response_regex_for_figure_and_table():
    # Define the possible representations of figure and table names
    figure_patterns = ["Fig\\."]
    table_patterns = ["Table"]

    # Combine the patterns into regex patterns
    figure_pattern = "|".join(figure_patterns)
    table_pattern = "|".join(table_patterns)

    # Create a regex pattern to capture the figure and table titles along with their explanations
    # The pattern is designed to capture the numbering and make the newline at the end optional
    entry_pattern = f"(({figure_pattern}|{table_pattern})\\s*(\\d+))\\.\\s*(.*?) \\(Page:\\s*(\\d+)\\) - (.*?)(\\n|$)"

    return entry_pattern


def convert_response_to_dict(response_text):
    entry_pattern = response_regex_for_figure_and_table()
    entries = {}

    # Find all matches in the response_text for figures and tables with explanations
    matches = re.findall(entry_pattern, response_text, re.DOTALL)

    # Process and store the matched titles, page numbers, and explanations
    for match in matches:
        # Deconstruct the match to get the needed parts
        # This includes the figure/table identifier with numbering
        full_identifier, _, number, image_title, image_page_number, explanation, _ = match
        key = f"{full_identifier}. {image_title} (Page:{image_page_number})"
        entries[key] = explanation.strip()

    return entries


# image_title_pairs: dictionary of the images that are extracted
# important_images: list of important image titles. List of tuples.
# Returns the extracted important images
def get_important_image_paths(image_title_pairs, important_images):
    # Check whether the important image is extracted
    found_important_images_paths = {}
    for title in important_images:
        if title in image_title_pairs.keys():
            found_important_images_paths.update({title:image_title_pairs[title]})
                
    return found_important_images_paths