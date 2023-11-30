import replicate
import re
from pdf_section_extractor import extract_pdf_and_divide_sections, extract_pdf, capture_image_titles
from article_parser import divide_article_into_sections
from image_titles import extract_titles_from_page
import fitz

def send_prompt(prompt, sys_prompt):
    rp_client = replicate.Client(api_token='r8_XPMMEL0KhlcfRy3nRopduYp3d64X39v0S6SDI')
    output = rp_client.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
        "debug": False,
        "top_k": 50,
        "top_p": 1,
        "prompt": prompt,
        "temperature": 0.75,
        "system_prompt": sys_prompt,
        "max_new_tokens": 1000,
        "min_new_tokens": -1
    })
    response = ""
    for item in output:
        # https://replicate.com/meta/llama-2-70b-chat/versions/02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/api#output-schema
        # print(item, end="")
        response += item
    return response

def summarize(section_name, section_text):
    summarize_sys_prompt = 'You are a tool that summarizes the given text. The given text is a section of an article. Give a concise summary of the section text to include only the most important information.'
    prompt = section_name + ": " + section_text
    output = send_prompt(prompt, summarize_sys_prompt)
    return output

def extract_insights(text):
    insights_sys_prompt = 'You are a tool that extracts key insights from an article. You will be provided with article sections. As an output, you should provide concise insights about the given article in bulletpoints.'
    prompt = text
    output = send_prompt(prompt, insights_sys_prompt)
    return output

def generate_title(insights):
    find_title_sys_prompt = "From the given insights, provide a title."
    prompt = "Extracted insights: " + insights + "Title: "
    output = send_prompt(prompt, find_title_sys_prompt)
    return output

def choose_images(insights, image_titles):
    choose_images_sys_prompt = "Given the image title, choose the most important 3 images of the article based on the insights extracted from the article."
    prompt = "Extracted insights: " + insights + "Image titles: " + image_titles + "Important sections: "
    output = send_prompt(prompt, choose_images_sys_prompt)
    return output

# Function for preparing the input prompt for insights extraction process using the summarized sections
def create_section_input(summarized_sections):
    # Initialize an empty string to store the formatted output
    section_input = ""

    # Iterate over each key-value pair in the dictionary
    for key, value in summarized_sections.items():
        # Append the key and value to the string with the specified format
        section_input += f"{key}: {value} \n"

    return section_input

#pdf_path = "/Users/nusretkizilaslan/Downloads/selo-article.pdf"
#pdf_path = "/Users/selinceydeli/Desktop/sabancı/OPIM407/Individual Assignment-3/Predicting_Freshman_Student_Attrition_Article.pdf"
business_pdf1_path = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/buss_article.pdf"
sections_dict = extract_pdf_and_divide_sections(business_pdf1_path)
extracted_pdf = extract_pdf(business_pdf1_path)

insights = '''
* Relationship marketing (RM) is crucial for business-to-business (B2B) companies to navigate economic downturns and recoveries.
* During economic uncertainty, firms need to adapt their RM strategies to address changing customer needs and maintain relationships.
* A framework linking RM process mechanisms to firm performance during economic contractions and expansions has been proposed, which includes three key relationship tenets: communication openness, technical involvement, and customer value anticipation.
* These tenets have direct and indirect effects on supplier performance and can help firms manage business-to-business relationships (BCs).
* The study provides actionable strategies for managing BCs during economic contractions and expansions, including establishing high levels of communication without increasing technical collaboration, exploiting top management consensus, and leveraging technical involvement with customers.
* The findings have important implications for theory, extending existing research streams and providing insights into how B2B relationships can be managed during times of economic uncertainty.
* The study contributes to the dark side of B2B relationships’ theoretical underpinnings by demonstrating how the inherent tension created in a BC can be managed by RM mechanisms.
* The study extends BC marketing literature outside of the often-used US environment by investigating buyer-seller relationships through a BC in an emerging economy, Chile.
'''

# Open the file
pdf_file = fitz.open(business_pdf1_path)

titles = []

# Iterate over PDF pages
for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    page_image_titles = extract_titles_from_page(page)
    for title in page_image_titles:
        title += " (Page:" + str(page_index+1) + ")"
        titles.append(title)

pdf_file.close()

image_titles = ""
for title in titles:
    image_titles += title + "\n"
important_images = choose_images(insights, image_titles)
print(important_images)

#Preprocessing
#Delete the first 3 characters (1. )
#Take the figure titles including up until the (Page:1)
#Also return the corresponding images
