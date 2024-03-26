import streamlit as st
from structures import UploadedArticle
from utilities import *

hide_sidebar()

with st.spinner('Generating summaries...'):
    report = UploadedArticle.generate_report()


if report:
    st.switch_page('pages/1_Report_Page.py')

