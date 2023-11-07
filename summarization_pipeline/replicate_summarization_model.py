
import replicate
import re
from pdf_section_extractor import extract_pdf_and_divide_sections

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
        response += item + "\n"
    return response

def summarize(section_name, section_text):
    summarize_sys_prompt = 'You are a tool that summarizes the given text. The given text is a section of an article. Give a concise summary of the section text to include only the most important information.'
    prompt = section_name + ": " + section_text
    output = send_prompt(prompt, summarize_sys_prompt)
    return output

#pdf_path = "/Users/nusretkizilaslan/Downloads/selo-article.pdf"
#pdf_path = "/Users/selinceydeli/Desktop/sabancı/OPIM407/Individual Assignment-3/Predicting_Freshman_Student_Attrition_Article.pdf"
business_pdf1_path = "/Users/selinceydeli/Desktop/business-article-inputs/1-s2.0-S0148296323004216-main.pdf"

sections_dict = extract_pdf_and_divide_sections(business_pdf1_path)

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
    if section_text != "": 
        summary = summarize(section_name, section_text)
        summarized_sections[section_name] = summary
        print("Summary of" + section_name + ": \n" + summary)
    else : summarized_sections[section_name] = None

