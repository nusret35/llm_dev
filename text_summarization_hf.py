from bs4 import BeautifulSoup
import zipfile
from transformers import pipeline
import textwrap
import re

def format_text(text):
    sentences = re.split('\.\s*', text)
    sentences = [s.strip().capitalize() for s in sentences if s]
    formatted_text = '. '.join(sentences) + '.'
    return formatted_text

# Load the summarization pipeline
summarizer = pipeline('summarization')

# Function to read and parse HTML file
def read_html_file(file):
    soup = BeautifulSoup(file, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

# Initialize an empty string to store the summaries
summary = ""

# Read the zip file
#with zipfile.ZipFile("/Users/selinceydeli/Desktop/pages.zip", "r") as z:
with zipfile.ZipFile("./pages.zip", "r") as z:
    for filename in z.namelist():
        if ".html" in filename:
            with z.open(filename) as f:
                data = f.read()
                text = read_html_file(data)
                chunks = textwrap.wrap(text, 1024)
                for chunk in chunks:
                    # Calculate max_length as half of the input length
                    max_length = min(50, len(chunk.split()) // 2)
                    if max_length == 0:
                        max_length = 2
                    summarized_chunk = summarizer(chunk, max_length=max_length, min_length=0, do_sample=False)
                    summary += summarized_chunk[0]['summary_text']

# Format the summarized text
formatted_summary = format_text(summary)

# Print the formatted summary
print(formatted_summary),