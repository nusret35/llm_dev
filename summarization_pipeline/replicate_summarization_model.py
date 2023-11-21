
import replicate
import re
from pdf_section_extractor import extract_pdf_and_divide_sections
from article_parser import divide_article_into_sections

def send_prompt(prompt, sys_prompt):
    rp_client = replicate.Client(api_token='r8_VbKuL8aKGq6NNTtMVRRRfHWP6VnCZAl3G2Kum')
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
business_pdf1_path = "/Users/selinceydeli/Desktop/AIResearch/business-article-inputs/1-s2.0-S0148296323004216-main.pdf"
sections_dict = extract_pdf_and_divide_sections(business_pdf1_path)

"""
business_txt_path = "/Users/selinceydeli/Desktop/AIResearch/llm_dev/summarization_pipeline/bus_article1.txt"
with open(business_txt_path, 'r') as file:
    article = file.read()
sections_dict = divide_article_into_sections(article)
"""

abstract = sections_dict.get('abstract', "")

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

summarized_sections = {}
for section_name, section_text in critical_section_information.items():
    if section_text != "" and section_name != "introduction" and section_name != "managerial implications": 
        summary = summarize(section_name, section_text)
        summarized_sections[section_name] = summary
        print("Summary of " + section_name + ": \n" + summary)
    else : summarized_sections[section_name] = None

text = '''
Introduction: This article discusses the importance of relationship marketing (RM) in business-to-business (B2B) settings, particularly during economic downturns. The authors argue that while RM has been shown to be effective in fostering long-term relationships and improving firm performance, there is a need to explore how it can help firms navigate economic contractions and recoveries. They note that during times of economic uncertainty, firms may need to adapt their RM strategies to address changing customer needs and maintain relationships. The authors review existing literature on RM and economic fluctuations, highlighting the lack of research on the topic in emerging economies and B2B settings. They propose a framework that links RM process mechanisms to firm performance during economic contractions and expansions, and identify three key relationship tenets: communication openness, technical involvement, and customer value anticipation. These tenets have direct and indirect effects on supplier performance and can help firms manage BCs. The article also examines the difference in modeled relationship mechanisms between economic contraction and expansion, providing actionable strategies for managing BCs. Finally, the authors consider three outcome variables - selling price, cost-to-serve, and expectation of relationship continuity - at the customer level, making their findings more concrete and relevant to practitioners. Overall, the study aims to contribute to the RM literature and provide insights into managing BCs in emerging economies and B2B settings.

Managerial implications: The section discusses the managerial implications of the proposed resilience mechanisms (RM) for companies during times of economic crisis and recovery. The authors suggest a 2x3 matrix with six quadrants, each representing a different combination of RM strategies to achieve firm goals: increasing price, reducing cost-to-serve, and enhancing expectation of continuity. The quadrants are named based on the empirical results and include "Value anticipation based on distant communication," "Cost-oriented joint collaboration," "Dyadic top management consensus," "Generative hard work," "Controlled technical deescalating," and "Integrated optimal balance." The authors recommend specific RM strategies for each quadrant, such as establishing high levels of communication without increasing technical collaboration, exploiting top management consensus, and leveraging technical involvement with customers. The study suggests that during times of economic recovery, suppliers should primarily focus on collaborating with customers, while carefully deescalating INV to avoid saving resources but maintaining a minimal level of satisfaction.

Theoretical implications: This section discusses the theoretical implications of the study's findings on business-to-business (B2B) relationships during economic downturns. The authors argue that their findings have important implications for theory, as they provide insights into how B2B relationships can be managed during times of economic uncertainty. They extend existing research streams by showing how a BC brings profitability opportunities for B2B suppliers through nurturing mechanisms from long-term dyadic exchange. Additionally, they contribute to the dark side of B2B relationships’ theoretical underpinnings by demonstrating how the inherent tension created in a BC can be managed by relationship marketing (RM) mechanisms. Finally, they extend BC marketing literature outside of the often-used US environment by investigating buyer-seller relationships through a BC in an emerging economy, Chile.
'''

section_input = create_section_input(summarized_sections)
insights = extract_insights(section_input)
print("Extracted insights:\n" + insights)

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

title = generate_title(insights)
print(title)