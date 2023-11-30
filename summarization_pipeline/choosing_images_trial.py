import replicate
import re
from pdf_section_extractor import extract_pdf_and_divide_sections, extract_pdf, capture_image_titles
from article_parser import divide_article_into_sections
from image_processing import extract_titles_from_page, extract_image_title_pairs, get_important_image_paths
import fitz

def send_prompt(prompt, sys_prompt):
    rp_client = replicate.Client(api_token='r8_QGFyCH7vMasCAK7pCW0XvSeXNjd8s5j0oL1CG')
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
    choose_images_sys_prompt = "From the given article insights, choose the most important 3 image titles and give an explanation for each of your choice. Output should be in the following format: Image title (Page: Page number) - Explanation"
    prompt = "Extracted insights: " + insights + "Image titles: " + image_titles
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


def convert_response_to_list(response_text):
    # Define the possible representations of figure and table names
    figure_patterns = ["Fig\."]
    table_patterns = ["Table"]

    # Combine the patterns into regex patterns
    figure_pattern = "|".join(figure_patterns)
    table_pattern = "|".join(table_patterns)

    # Create a regex pattern to capture the figure and table titles
    figure_title_pattern = f"({figure_pattern}\s*\d+):\s*(.*?) \(Page:(\d+)\) - (.*)"
    table_title_pattern = f"({table_pattern}\s*\d+):\s*(.*?) \(Page:(\d+)\) - (.*)"


    titles = []

    # Find all matches in the extracted_text for figures and tables
    figure_matches = re.findall(figure_title_pattern, response_text)
    table_matches = re.findall(table_title_pattern, response_text)

    # Process and store the matched titles and numberings from the figures
    for match in figure_matches:
        image_name, image_title, image_page_number, explanation = match
        if image_name != "":
            if ('A' <= image_name[0] and image_name[0] <= "Z") or ('0' <= image_name[0] and image_name[0] <= '9'):
                titles.append((f"{image_name}. {image_title}.", explanation, image_page_number))

    # Process and store the matched titles and numberings from the tables
    for match in table_matches:
        image_name, image_title, image_page_number, explanation = match
        if image_name != "":
            if ('A' <= image_name[0] and image_name[0] <= "Z") or ('0' <= image_name[0] and image_name[0] <= '9'):
                titles.append((f"{image_name}. {image_title}.", explanation, image_page_number))

    # Return an list of 3 variable tuples (title, explanation, page_number)

    return titles


    


business_pdf1_path = "/Users/nusretkizilaslan/Downloads/selo-article.pdf"
#pdf_path = "/Users/selinceydeli/Desktop/sabancı/OPIM407/Individual Assignment-3/Predicting_Freshman_Student_Attrition_Article.pdf"
#business_pdf1_path = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/buss_article.pdf"
#business_pdf1_path = "/Users/nusretkizilaslan/Downloads/buss_article.pdf"
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
image_title_pairs = {}
# Iterate over PDF pages
for page_index in range(len(pdf_file)):
    page = pdf_file[page_index]
    page_image_title_pairs = extract_image_title_pairs(page,page_index)
    page_image_titles = extract_titles_from_page(page)
    image_title_pairs.update(page_image_title_pairs)
    for title in page_image_titles:
        title += " (Page:" + str(page_index+1) + ")"
        titles.append(title)

pdf_file.close()


image_titles = ""
for title in titles:
    image_titles += title + "\n"


#response = choose_images(insights, image_titles)

# API token ran out. Here is the hard coded response of the LLM
response = " Here are the three most important image titles and their explanations:\n\n1. Fig. 1: Relationships among perceived usability, perceived aesthetics, and user preference based on previous studies’ findings - This figure illustrates the relationships between perceived usability, perceived aesthetics, and user preference, which is the foundation of the study's research question. It shows how these factors influence each other and how they impact user preference.\n2. Table 7: User preference after actual use by conditions (Page:2) - This table shows the results of the study's experiment, specifically the user preferences after actual use of the systems. It highlights the differences in user preference between the high aesthetics and low aesthetics conditions, which is the primary focus of the study.\n3. Fig. 5: Interaction plot of usability level and actual use for perceived usability (Page:11) - This figure displays the interaction effect between usability level and actual use on perceived usability. It shows how the relationship between usability and actual use varies across different levels of usability, providing insights into how to optimize system design for improved user experience."

important_images_list = convert_response_to_list(response)


# Check whether the important image is extracted
found_images = get_important_image_paths(image_title_pairs,important_images_list)

print(found_images)



