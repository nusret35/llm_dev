from bs4 import BeautifulSoup
import zipfile
from transformers import pipeline
from datasets import load_dataset
import textwrap
import re
from pathlib import Path
import os
import string
from nltk.corpus import stopwords
import nltk
from collections import Counter
from sklearn.model_selection import train_test_split

# Function to format text
def format_text(text):
    new_text = ''
    for char in text:
        if char != r'\n':
            new_text += char
    sentences = re.split('\.\s*', new_text)
    sentences = [s.strip().capitalize() for s in sentences if s]
    formatted_text = '. '.join(sentences) + '.'
    return formatted_text

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

# Functions to conduct data cleaning
def remove_html(text):
    html = re.compile(r"<.*?>")
    return html.sub(r"",text)

def remove_URL(text):
    url = re.compile(r"https?://\S+|www\.\S+")
    return url.sub(r"",text)

def remove_punct(text):
    table = str.maketrans("","",string.punctuation)
    return text.translate(table)

# Initialize an empty array to append the documents as texts
texts = [] 

# Read the zip file
z =  Path('pages/')

for directory in z.iterdir():
    if directory.is_dir(): 
        for file in directory.iterdir():
            if ".html" in file.name:
                full_path = file.resolve()
                with open(full_path) as f:
                    data = f.read()
                    text = read_html_file(data)
                    texts.append(text)

# Conduct data cleaning
stop = set(stopwords.words("english"))

def remove_stopwords(text):
    text = [word.lower() for word in text.split() if word.lower() not in stop]
    return " ".join(text) 

clean_texts = []
for text in texts :
    cleaned_text = remove_html(text)
    cleaned_text = remove_punct(cleaned_text)
    cleaned_text = remove_URL(cleaned_text)
    cleaned_text = remove_stopwords(cleaned_text)
    cleaned_text = format_text(cleaned_text)
    clean_texts.append(cleaned_text)


print(len(clean_texts))
print(clean_texts[0])

# Data Partitioning
# Split the texts into training and testing sets
train_docs, test_docs = train_test_split(texts, test_size=0.2, random_state=42)

# Basic NLP

# Function to count unique words
def count_unique_words(documents):
    counter = Counter()
    for doc in documents:
        # Tokenize the document into words
        words = nltk.word_tokenize(doc)
        # Update the counter with the words
        counter.update(words)
    return dict(counter)

unique_word_counts = count_unique_words(train_docs)
print(len(unique_word_counts))