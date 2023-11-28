import fitz
import io
from PIL import Image
import os

def extract_image_from_page(page,page_index):
    image_list = page.get_image_info()

    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)

    img_index = 0
    for img in image_list:
        bbox = img['bbox']
        left, top, right, bottom = bbox[0], bbox[1], bbox[2], bbox[3]

        # Get the image data from the bounding box
        image = page.get_pixmap(matrix=fitz.Matrix(1, 1).prescale(2, 2), clip=(left, top, right, bottom))

        # Convert the image data to a Pillow image
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        directory_path = "./images/"+ 'page' +str(page_index) 
        os.makedirs(directory_path, exist_ok=True)

        img_name =  directory_path +'/output_image' + str(img_index) + '.png'
        # Save or process the image as needed
        pil_image.save(img_name)

# File path
#file = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/1-s2.0-S0148296323004216-main.pdf"
file = '/Users/nusretkizilaslan/Downloads/selo-article.pdf'

# Output folder
output_folder = "/Users/selinceydeli/Desktop/AIResearch/llm_dev/summarization_pipeline/extracted_images"

# Open the file
pdf_file = fitz.open(file)

import fitz  # PyMuPDF
from PIL import Image



# Iterate over PDF pages
for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    extract_image_from_page(page,page_index)
    

pdf_file.close()