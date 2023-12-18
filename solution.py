from summarization_pipeline.pdf_section_extractor import extract_pdf_and_divide_sections
from summarization_pipeline.orchestration import Extractor
from summarization_pipeline.image_processing import extract_image_title_pairs, extract_titles_from_page, convert_response_to_list, get_important_image_paths
import fitz

# Initializing the Extractor class for sending prompts to the LLaMA 2 70B model

extractor_70B_model = Extractor(model='70B')
extractor_13B_model = Extractor(model='13B')


# Getting and preprocessing PDF input

business_pdf1_path = "/Users/nusretkizilaslan/Downloads/buss_article_2.pdf"
sections_dict = extract_pdf_and_divide_sections(business_pdf1_path)

# Extracting section texts of important sections 

abstract = sections_dict.get('abstract', "")
print("Abstract: " + abstract + "\n")

critical_sections = ["introduction", "conclusion", "discussion", "methodology"]

critical_section_information = {}
for section_name in critical_sections:
  critical_section_information[section_name] = sections_dict.get(section_name, "")

"""
If at least two of the sections among "conclusion", "discussion", and "outcomes" are missing, 
then take the last four sections (we keep each subsection seperately in the current formulation of sections_dict) 
of the article (excluding keywords, acknowledgments, and references sections)
"""
check_for_absence = ""
critical_section_list = list(critical_section_information.items())
for section_name, section_text in critical_section_list[-3:]:
    if section_text == "": check_for_absence += '0'

if len(check_for_absence) >= 2:
    accepted = 0
    unwanted_sections = ["keywords", "acknowledgments", "references"]
    sections_list = list(sections_dict.items())
    for section_name, section_text in sections_list[::-1]: # Reverse iteration of the sections_list
        section_name = section_name.lower()
        section_text = sections_dict.get(section_name, "")
        if section_name not in unwanted_sections and section_text != "":
            critical_section_information[section_name] = section_text
            accepted += 1
            if accepted >= 4:
                break

print("Important section titles:")
for key, value in critical_section_information.items():
    print(key)

# Summarizing important sections
    
summarized_sections = {}
for section_name, section_text in critical_section_information.items():
    if section_text != "": 
        summary = extractor_70B_model.summarize(section_name, section_text)
        summarized_sections[section_name] = summary
        print("Summary of " + section_name + ": \n" + summary)
    else : summarized_sections[section_name] = None


# Converting the section text information from dictionary to string
# to feed it to the model as input

def create_section_input(summarized_sections):
    # Initialize an empty string to store the formatted output
    section_input = ""

    # Iterate over each key-value pair in the dictionary
    for key, value in summarized_sections.items():
        # Append the key and value to the string with the specified format
        section_input += f"{key}: {value} \n"

    return section_input

section_input = create_section_input(summarized_sections)

section_input_abstract = "abstract: " + abstract + section_input
print(section_input_abstract + "\n")

insights = extractor_70B_model.extract_insights(section_input_abstract)
print("Extracted insights:\n" + insights)


title = extractor_13B_model.generate_title(insights)
print(title)

# Open the file
pdf_file = fitz.open(business_pdf1_path)
titles = []
image_title_pairs = {}
# Iterate over PDF pages
for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    page_image_title_pairs = extract_image_title_pairs(page,page_index)
    page_image_titles = extract_titles_from_page(page)
    image_title_pairs.update(page_image_title_pairs)
    for title in page_image_titles:
        title += " (Page:" + str(page_index+1) + ")"
        print(title)
        titles.append(title)

pdf_file.close()

image_titles = ""
for title in titles:
    image_titles += title + "\n"
    
important_images = extractor_13B_model.choose_images(insights, image_titles)
print(important_images)


# Displaying the fetched figures/tables that match the selected images

important_images_list = convert_response_to_list(important_images)

# Check whether the important image is extracted
found_images = get_important_image_paths(image_title_pairs, important_images_list)
print(found_images)

extractor_13B_model.close()
extractor_70B_model.close()