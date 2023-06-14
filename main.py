import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

os.environ["OPENAI_API_KEY"] = "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" #API key is used for connection with ChatGPT 

import textract
doc = textract.process("/Users/selinceydeli/Desktop/sabancı/CS301/CS301-Syllabus-2022-2023-Spring-v4.pdf")

with open('CS301-Syllabus-2022-2023-Spring-v4.txt', 'w') as f:
    f.write(doc.decode('utf-8'))

with open('CS301-Syllabus-2022-2023-Spring-v4.txt', 'r') as f:
    text = f.read()

textSplitter = CharacterTextSplitter(chunk_size=2000, separator="\n")

doc.extend(textSplitter_split.text(sets))

