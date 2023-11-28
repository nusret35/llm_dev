import fitz
from PIL import Image
import os


def extract_image_from_page(page, page_index):
    image_list = page.get_image_info()
    text_blocks = page.get_text("blocks")

    keywords = ['table', 'figure', 'fig.', 'chart']
    proximity_threshold = 50  # Adjust this value based on your requirements

    image_titles = []
    image_paths = []

    img_index = 0
    for img in image_list:
        bbox = img['bbox']
        left, top, right, bottom = bbox[0], bbox[1], bbox[2], bbox[3]

        # Get the image data from the bounding box
        image = page.get_pixmap(matrix=fitz.Matrix(1, 1).prescale(2, 2), clip=(left, top, right, bottom))

        # Convert the image data to a Pillow image
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        directory_path = "./images/" + 'page' + str(page_index)
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
                first_word = block_text.strip().split()[0].lower()
                if first_word in keywords:
                    image_titles.append(block_text.strip())
    
    image_data = dict(zip(image_titles, image_paths))
    return image_data
    

# File path

#file = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/1-s2.0-S0148296323004216-main.pdf"
file = '/Users/nusretkizilaslan/Downloads/selo-article.pdf'

# Output folder
output_folder = "/Users/selinceydeli/Desktop/AIResearch/llm_dev/summarization_pipeline/extracted_images"

# Open the file
pdf_file = fitz.open(file)

# Iterate over PDF pages
for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    page_image_data = extract_image_from_page(page,page_index)
    print(page_image_data)
    
    

pdf_file.close()