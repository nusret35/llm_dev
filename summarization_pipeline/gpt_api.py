import os
import openai
from article_parser import group_subsections, recursive_grouping, divide_article_into_sections

openai.api_key = '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'

# Returns the text of a section together with the text of its subsections
def section_text(section_name, sections_dict):
    # Convert section_name to lowercase for case-insensitive comparison
    section_name_lower = section_name.lower() 
    for key, value in sections_dict.items():
        # Convert each key to lowercase for case-insensitive comparison
        if section_name_lower == key.lower():
            # If the section exists and its value is a string, the function returns this string directly
            if isinstance(value, str):
                return value
            # If the section exists and its value is a dictionary,
            # the function concatenates all the string values from this dictionary
            else:  
                output = ''
                for item in value.values():
                    output += item + ' '  # Add a space for separation
                return output.strip()  # Remove trailing space
    return ''

def send_prompt(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": prompt}
        ]
    )
    message = completion.choices[0].message
    return message
  
with open('summarization_pipeline/data2.txt', 'r') as file:
      text = file.read()

# Divide article into sections and return a dictionary (section names as keys and texts as values)
sections_dict = divide_article_into_sections(text)
sections_dict = group_subsections(sections_dict)
print("Section names after grouping the subsections:")

critical_sections = ["introduction", "methodology", "conclusion", "discussion", "outcomes"]

critical_section_information = {}
for section_name in critical_sections:
    critical_section_information[section_name] = section_text(section_name, sections_dict)

"""
If at least two of the sections among "conclusion", "discussion", and "outcomes" are missing, 
then take the last two sections of the article (excluding keywords, acknowledgments, and references sections)
"""
check_for_absence = ""
critical_section_list = list(critical_section_information.items())
for key, value in critical_section_list[-3:]:
    if value == "": check_for_absence += '0'

if len(check_for_absence) >= 2:
    accepted = 0
    unwanted_sections = ["keywords", "acknowledgments", "references"]
    while (accepted < 2):
      sections_list = list(sections_dict.items())
      for key, value in sections_list[::-1]: # Reverse iteration of the sections_list
          section_name = key.lower()
          if section_name not in unwanted_sections:
              critical_section_information[section_name] = section_text(section_name, sections_dict)
              accepted += 1

summarized_sections = {}
for key, value in critical_section_information.items():
    if value != "":
      prompt = "Summarize the text: " + value
      summary = send_prompt(prompt)
      summarized_sections[key] = summary
    else : summarized_sections[key] = None
    print(key + ": " + value + "\nSummary: " + summary)
