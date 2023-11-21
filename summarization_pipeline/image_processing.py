import fitz
import io
from PIL import Image

# File path
file = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/1-s2.0-S0148296323004216-main.pdf"

# Output folder
output_folder = "/Users/selinceydeli/Desktop/AIResearch/llm_dev/summarization_pipeline/extracted_images"

# Open the file
pdf_file = fitz.open(file)

# Iterate over PDF pages
for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    image_list = page.get_images()

    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)

    for img_index, img in enumerate(image_list, start=1):
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        # Create an image object and save it
        image = Image.open(io.BytesIO(image_bytes))
        image_save_path = f"{output_folder}/image_page_{page_index}_{img_index}.{image_ext}"
        image.save(image_save_path)

pdf_file.close()