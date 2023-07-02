import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nlp
import random
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from bs4 import BeautifulSoup

def read_html_file(file):
    soup = BeautifulSoup(file, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


with zipfile.ZipFile("./pages.zip", "r") as z:
    for filename in z.namelist():
        if ".html" in filename:
            with z.open(filename) as f:
                data = f.read()
                text = read_html_file(data)
                chunks = textwrap.wrap(text, 1024)
                
text = read_html_file()