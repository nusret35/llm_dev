# Use a pipeline as a high-level helper
from transformers import pipeline
from summarizer import Summarizer
from article_parser import group_subsections, recursive_grouping, divide_article_into_sections
import threading
import torch
import re

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
    llama_exec_path = '/Users/selinceydeli/Desktop/llama/llama.cpp/main'
    #llama_exec_path = '/Users/nusretkizilaslan/Desktop/AIProject/llama2/llama.cpp/main'

    # Summarizer model
    summarizer = Summarizer(exec_path=llama_exec_path)

    #output = summarizer._send_prompt('Summarize this text: Climate change mitigation requires a multidimensional approach including GHG emission reduction, carbon capture, and adaptation strategies. Transitioning to renewable energy sources, improving energy efficiency, and modifying consumption patterns are crucial. Technological innovations for carbon capture and sequestration (CCS) can further aid in offsetting emissions. Furthermore, climate-resilient development practices can enhance adaptive capacity, particularly for the most vulnerable communities.')
    #print(output)
    # Read txt document
    with open('summarization_pipeline/data2.txt', 'r') as file:
        text = file.read()

    # Divide article into sections and return a dictionary (section names as keys and texts as values)
    sections_dict = divide_article_into_sections(text)

    print("Section names before grouping the subsections:")
    print(sections_dict)

    sections_dict = group_subsections(sections_dict)

    print("Section names after grouping the subsections:")
    print(sections_dict)

    #title = 'Climate Change: Trends, Consequences, and Mitigation Strategies'
    abstract = summarizer.section_text('Abstract',sections_dict)
    print("Abstract: " + abstract)

    #objective = summarizer.find_objective(title,sections_dict)
    #thesis = summarizer.find_thesis_statament(abstract)
    #print(thesis)

    critical_sections = ["introduction", "conclusion", "discussion", "methodology", "outcomes"]

    # take these critical sections
    # or take the last two sections of the article
    # also consider the descriptions under the figures -> take the important ones
    # aim: enriching the abstract to have a 700-800 worded summary of the article

    critical_section_information = {}
    for section in critical_sections:
        critical_section_information[section] = summarizer.section_text(section,sections_dict)

    summarized_sections = {}
    for key, value in critical_section_information.items(): 
        summary = summarizer.summarize(value)
        summarized_sections[key] = summary
        print(key + ": " + value + "\nSummary: " + summary)

    section_names = list(sections_dict.keys())
    numbered_section_names = ["{}. {}".format(i+1, section) for i, section in enumerate(section_names)]
    print(numbered_section_names)

    important_sections = summarizer.select_sections(numbered_section_names,thesis)
    print(important_sections)

    summaries = []
    
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