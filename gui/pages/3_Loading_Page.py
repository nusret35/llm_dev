import streamlit as st
from structures import UploadedArticle
from utilities import *

hide_sidebar()

st.title("Preparing...")

with st.spinner('Generating section summaries...'):
    uploaded_article = UploadedArticle()
    report = uploaded_article.generate_report()
    print(report.get_section_summaries)

