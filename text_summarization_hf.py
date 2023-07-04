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
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.initializers import Constant
from keras.optimizers import Adam
import json
import PyPDF2

# Function to convert pdf to text
def convert_pdf_to_text(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        with open(txt_path, 'w') as txt_file:
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text = page.extract_text()
                txt_file.write(text)

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

# Function to read and parse JSON file
def read_json_file(file):
    data = json.load(file)
    return data

# Function to get the week number of the directory
def get_week_number(key):
    pattern = r"week-(\d+)"
    match = re.search(pattern, key)
    if match:
        return int(match.group(1))
    else:
        return -1  # default value if week number extraction fails

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

# Initialize an empty dictionary to append the documents as texts
texts = {} 

'''
# Read the HTML documents
z =  Path('pages/')

for directory in z.iterdir():
    if directory.is_dir():
        for file in directory.iterdir():
            if ".html" in file.name:
                full_path = file.resolve()
                with open(full_path) as f:
                    data = f.read()
                    text = read_html_file(data)
                    texts[directory.name] = text

texts = [value for key, value in sorted(texts.items(), key=lambda x:get_week_number(x[0]))]

print(texts)
'''

# Read the JSON documents
z =  Path('pages/')

texts = {}

for directory in z.iterdir():
    if directory.is_dir():
        for file in directory.iterdir():
            if ".json" in file.name:
                full_path = file.resolve()
                with open(full_path, 'r') as f:
                    text = read_json_file(f)
                    texts[directory.name] = text

texts = [value for key, value in sorted(texts.items(), key=lambda x:get_week_number(x[0]))]

print(texts[0])

# Conduct data cleaning
stop = set(stopwords.words("english"))

def remove_stopwords(text):
    text = [word.lower() for word in text.split() if word.lower() not in stop]
    return " ".join(text) 

clean_texts = []
for text in texts :
    cleaned_text = remove_html(text['content'])
    cleaned_text = remove_punct(cleaned_text)
    cleaned_text = remove_URL(cleaned_text)
    cleaned_text = remove_stopwords(cleaned_text)
    cleaned_text = format_text(cleaned_text)
    clean_texts.append(cleaned_text)

print(len(clean_texts))
print(clean_texts[0])

# Data Partitioning
# Split the texts into training and testing sets
train_docs, test_docs = train_test_split(clean_texts, test_size=0.2, random_state=42)

print(train_docs)

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
num_words = len(unique_word_counts)

# Max number of words in a sequence. We need to have the same sequence length when using TensorFlow
max_length = len(max(train_docs,key=len))

tokenizer = Tokenizer(num_words)
tokenizer.fit_on_texts(train_docs)
word_index = tokenizer.word_index
print(word_index)

# Padding train sequences
train_sequences = tokenizer.texts_to_sequences(train_docs)
train_padded = pad_sequences(train_sequences,maxlen=max_length,padding='post',truncating='post')

print(train_docs[0])
print(train_sequences[0])
print(train_padded[0])

# Padding test sequences
test_sequences = tokenizer.texts_to_sequences(test_docs)
test_padded = pad_sequences(test_sequences,maxlen=max_length,padding='post',truncating='post')

reverse_word_index = {v: k for k, v in word_index.items()}

def decode(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])

print(decode(train_sequences[0]))

print(f"Shape of train {train_padded.shape}")
print(f"Shape of test {test_padded.shape}")

model = Sequential()

model.add(Embedding(num_words, 32, input_length=max_length))
model.add(LSTM(64, dropout=0.1))
model.add(Dense(1, activation="sigmoid"))

optimizer = Adam(learning_rate=3e-4)

model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy"])

model.summary()