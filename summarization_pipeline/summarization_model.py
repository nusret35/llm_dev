from transformers import pipeline
from summarizer import Summarizer
import torch
import re

"""
summarizer = pipeline(
    "summarization",
    "pszemraj/long-t5-tglobal-base-16384-book-summary",
    device=0 if torch.cuda.is_available() else -1,
)
"""

# Define a function to handle the iterative grouping of summaries
def recursive_grouping(summaries, summarizer, max_length=70):
    # Base case: if there's only one summary, return it
    if len(summaries) == 1:
        return summaries[0]

    # If more than one summary, group them by two and generate new summaries
    new_summaries = []
    for i in range(0, len(summaries), 2):
        text = summaries[i]
        if i + 1 < len(summaries):  # Check to ensure we don't exceed the list index
            text += " " + summaries[i + 1]
        # Hugging face pipeline
        # new_summaries.append(summarizer(text, max_length=max_length, min_length=20, do_sample=False)[0]['summary_text'])

        # Alpaca model summarization
        summary = summarizer.summarize(text)
        new_summaries.append(summary)

    return recursive_grouping(new_summaries, summarizer, max_length + 10)  # Increase max_length for each new round

def divide_article_into_sections(article):
    sections = {}
    section_titles = re.findall(r'\d+\..+?\n', article)  # Find all lines that start with "number.title"
    
    # Use zip to pair section titles with their corresponding text
    for title, next_title in zip(section_titles, section_titles[1:] + ['']):
        # Get the start and end positions of each section
        start_pos = article.find(title)
        end_pos = article.find(next_title)
        
        # Extract the section text and remove the section title
        section_text = article[start_pos + len(title):end_pos].strip()
        
        # Store the section in the dictionary with the title as the key
        sections[title[:-2].strip()] = section_text

    return sections

def parse_article(article_text):
    sections = {}
    current_section = None
    current_subsection = None

    # Define regular expressions for section and subsection headings
    section_pattern = re.compile(r'^(\d+)\.(.*)$')
    subsection_pattern = re.compile(r'^(\d+\.\d+)\s+(.*)$')

    lines = article_text.splitlines()
    for line in lines:
        line = line.strip()
        if line:
            # Check if the line matches the section pattern
            match_section = section_pattern.match(line)
            if match_section:
                section_number = match_section.group(1)
                section_name = match_section.group(2).strip()
                sections[section_number] = {'name': section_name, 'text': ''}
                current_section = section_number
                current_subsection = None  # Reset current_subsection when a new section is encountered
            else:
                # Check if the line matches the subsection pattern
                match_subsection = subsection_pattern.match(line)
                if match_subsection and current_section:
                    subsection_number = match_subsection.group(1)
                    subsection_name = match_subsection.group(2).strip()
                    sections[current_section][subsection_number] = {'name': subsection_name, 'text': ''}
                    current_subsection = subsection_number
                elif current_section and current_subsection:
                    # If not a subsection, add the line to the current section's text
                    sections[current_section][current_subsection]['text'] += line + '\n'
                elif current_section:
                    # If in a subsection, add the line to the current subsection's text
                    sections[current_section]['text'] += line + '\n'

    return sections



if __name__ == "__main__":

    #exec_path = './alpaca-exec-s'
    exec_path = './alpaca-exec-n'

    # Summarizer model
    summarizer = Summarizer(model_path=exec_path)

    # Read txt document
    with open('summarization_pipeline/data2.txt', 'r') as file:
        text = file.read()

    # Divide article into sections and return a dictionary (section names as keys and texts as values)
    sections = parse_article(text)

    print(sections)

    absract = list(sections.values())[0]

    thesis_statement = summarizer.find_thesis_statament(text=absract)

    print(thesis_statement)

    sections_keys = list(sections.keys())

    sections_output = summarizer.select_sections(sections_keys,thesis_statement)

    print(sections_output)
    summaries = []

    for section in sections.values():
        section = section.strip()  # Remove any leading/trailing whitespace

        # Hugging Face pipeline summarization
        #summaries.append(summarizer(section, max_length=50, min_length=20, do_sample=False)[0]['summary_text'])

        # Alpaca model summarization
        summary = summarizer.summarize(section)
        print(summary)
        summaries.append(summary)


    final_summary = recursive_grouping(summaries,summarizer)

    print()
    print(final_summary)
