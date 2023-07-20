from transformers import pipeline
import torch

# Load the summarization pipeline
summarizer = pipeline(
    "summarization",
    "pszemraj/long-t5-tglobal-base-16384-book-summary",
    device=0 if torch.cuda.is_available() else -1,
)

section_names = ['Climate Change', 'Author', 'Abstract', 'Introduction', 'Methodology', 'Trends in Climate Change', 'Consequences of Climate Change', 'Mitigation Strategies', 'Outcomes', 'Conclusion', 'Keywords', 'Acknowledgements', 'References']

with open('summarization_pipeline/data.txt', 'r') as file:
    lines = file.readlines()

summary = ""

for line in lines:
    line = line.strip()  # remove any leading/trailing whitespace
    if line not in section_names and line != "":
        summary += summarizer(line, max_length=50, min_length=25, do_sample=False)[0]['summary_text']

# Note that summarizer returns a list of dictionaries. So, to get the actual summary text, we need to access the 'summary_text' key of the first element in the list.



#summarizer(chunk, max_length=max_length, min_length=0, do_sample=False)
