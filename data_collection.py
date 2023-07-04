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
def convert_pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        file_name = pdf_path.stem
        txt_path = f"{file_name}.txt"
        whole_text = ''
        with open(txt_path, 'w') as txt_file:
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                if page != None:
                    text = page.extract_text()
                    txt_file.write(text)
                    whole_text += text
        return whole_text
                

# Function to get the week number of the directory
def get_week_number(key):
    pattern = r"week-(\d+)"
    match = re.search(pattern, key)
    if match:
        return int(match.group(1))
    else:
        return -1  # default value if week number extraction fails

def output_text(z):
    courses = []
    outcomes = []
    for directory in z.iterdir():
        if directory.is_dir():
            course = {}
            for file in directory.iterdir():
                if "learning_outcome.txt" in file.name:
                    full_path = file.resolve()
                    with open(full_path, 'r') as file:
                        data = file.read()
                        outcomes.append(data)
                if ".pdf" in file.name:
                    full_path = file.resolve()
                    if file.name == 'week-5.pdf':
                        print('hello')
                    text = convert_pdf_to_text(full_path)
                    course[file.name] = text
            course = [value for key, value in sorted(course.items(), key=lambda x:get_week_number(x[0]))]
            courses.append(course)
    return courses, outcomes
