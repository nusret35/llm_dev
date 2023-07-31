from transformers import pipeline
from summarizer import Summarizer
from article_parser import group_subsections, recursive_grouping, divide_article_into_sections
import torch
import re

"""
summarizer = pipeline(
    "summarization",
    "pszemraj/long-t5-tglobal-base-16384-book-summary",
    device=0 if torch.cuda.is_available() else -1,
)
"""

if __name__ == "__main__":

    exec_path = './alpaca-exec-s'
    #exec_path = './alpaca-exec-n'

    # Summarizer model
    summarizer = Summarizer(model_path=exec_path)

    # Read txt document
    with open('summarization_pipeline/data2.txt', 'r') as file:
        text = file.read()

    # Divide article into sections and return a dictionary (section names as keys and texts as values)
    sections_dict = divide_article_into_sections(text)

    sections_dict = group_subsections(sections_dict)
    print(sections_dict)

    title = 'Climate Change: Trends, Consequences, and Mitigation Strategies'

    objective = summarizer.find_objective(title,sections_dict)
    print(objective)
    
    sections_keys = list(sections_dict.keys())

    summaries = []

    for section in sections_dict.values():
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
