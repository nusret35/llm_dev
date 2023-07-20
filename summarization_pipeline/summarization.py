from transformers import pipeline
import torch
import re

# Load the summarization pipeline
"""
summarizer = pipeline(
    "summarization",
    "pszemraj/long-t5-tglobal-base-16384-book-summary",
    device=0 if torch.cuda.is_available() else -1,
)
"""

summarizer = pipeline("summarization")

section_names = ['Climate Change:', 'Author:', 'Abstract:', 'Introduction:', 'Methodology:', 'Trends in Climate Change:', 'Consequences of Climate Change:', 'Mitigation Strategies:', 'Outcomes:', 'Conclusion:', 'Keywords:', 'Acknowledgements:', 'References:']

with open('summarization_pipeline/data.txt', 'r') as file:
    text = file.read()

sections = re.split('\d+\..+\n', text)  # Split on lines that start with "number.title"
sections = [section.strip() for section in sections if section.strip()]

print(len(sections))

summaries = []

for section in sections:
    section = section.strip()  # remove any leading/trailing whitespace
    if section not in section_names and section != "":
        # Deciding on the max_length and min_length parameters based on input length
        summaries.append(summarizer(section, max_length=50, min_length=25, do_sample=False)[0]['summary_text'])

print(len(summaries))

