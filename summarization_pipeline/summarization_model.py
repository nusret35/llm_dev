from transformers import pipeline
from summarizer import Summarizer
from article_parser import group_subsections, recursive_grouping, divide_article_into_sections
import threading
import torch
import re

"""
summarizer = pipeline(
    "summarization",
    "pszemraj/long-t5-tglobal-base-16384-book-summary",
    device=0 if torch.cuda.is_available() else -1,
)
"""

"""
The function takes a nested dictionary, where the nesting represents the subsections in a section, 
and returns the summary of each section recursively. 
If the number of words in a section is less than 25, then no need to call the summarize function. The text is taken as it is. 
"""
def summarize_section(section, summarizer):
    if isinstance(section,dict):
        summary = ''
        for sub_section in section.values():
            summary += summarize_section(sub_section, summarizer) + " "
    else:
        text = section.strip() # Remove any leading/trailing whitespace
        if len(section.split()) > 50 :
            summary = summarizer.summarize(text)
        else :
            summary = text
    return summary


if __name__ == "__main__":

    exec_path = './alpaca-exec-s'
    #exec_path = './alpaca-exec-n'

    # Summarizer model
    summarizer = Summarizer(model_path=exec_path)

    # Read txt document
    with open('summarization_pipeline/data3.txt', 'r') as file:
        text = file.read()

    # Divide article into sections and return a dictionary (section names as keys and texts as values)
    sections_dict = divide_article_into_sections(text)

    sections_dict = group_subsections(sections_dict)

    title = 'Climate Change: Trends, Consequences, and Mitigation Strategies'
    abstract = summarizer.section_text('Abstract',sections_dict)

    #objective = summarizer.find_objective(title,sections_dict)
    thesis = summarizer.find_thesis_statament(abstract)
    print(thesis)
    
    section_names = list(sections_dict.keys())
    numbered_section_names = ["{}. {}".format(i+1, section) for i, section in enumerate(section_names)]
    print(numbered_section_names)

    important_sections = summarizer.select_sections(numbered_section_names,thesis)
    print(important_sections)

    summaries = []

    """
    # Summarizing the entirity of the article
    for section in sections_dict.values():
        section = section.strip()  # Remove any leading/trailing whitespace

        # Hugging face pipeline summarization
        #summaries.append(summarizer(section, max_length=50, min_length=20, do_sample=False)[0]['summary_text'])

        # Alpaca model summarization
        summary = summarizer.summarize(section)
        print(summary)
        summaries.append(summary)
    """

    # Summarizing the important sections of the article
    for key, value in sections_dict.items():
        if key in important_sections: 
            # Alpaca model summarization
            summary = summarize_section(value,summarizer)
            print(summary)
            summaries.append(summary)

    final_summary = recursive_grouping(summaries,summarizer)

    print()
    print(final_summary)
