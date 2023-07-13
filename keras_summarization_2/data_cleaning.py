import re
import string
from nltk.corpus import stopwords

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

# Functions to conduct data cleaning
def make_case_insensitive(text):
    return re.sub('[^a-zA-Z]',' ',text)

def remove_html(text):
    html = re.compile(r"<.*?>")
    return html.sub(r"",text)

def remove_URL(text):
    url = re.compile(r"https?://\S+|www\.\S+")
    return url.sub(r"",text)

def remove_punct(text):
    table = str.maketrans("","",string.punctuation)
    return text.translate(table)

stop = set(stopwords.words("english"))

def remove_stopwords(text):
    text = [word.lower() for word in text.split() if word.lower() not in stop]
    return " ".join(text) 

def clean_data(documents):
    clean_documents = []
    for course in documents:
        clean_course = []
        for weekly_content in course:
            cleaned_text = remove_html(weekly_content)
            cleaned_text = remove_punct(cleaned_text)
            cleaned_text = remove_URL(cleaned_text)
            cleaned_text = remove_stopwords(cleaned_text)
            cleaned_text = make_case_insensitive(cleaned_text)
            cleaned_text = format_text(cleaned_text)
            clean_course.append(cleaned_text)
        clean_documents.append(clean_course)
    return clean_documents