import streamlit as st
import pandas as pd
from io import StringIO
from utilities import *
from structures import UploadedArticle, Report


########  INITIALIZATON  ########
uploaded_article = UploadedArticle()
report = Report()

uploaded_article.delete_article()
report.delete_report()

########  FUNCTIONS  ########
st.set_page_config(
    page_title="Insight Extractor",
    layout="wide",
)


hide_sidebar()

st.title("EXTRACT BUSINESS INSIGHTS")
st.markdown(
    """
        In the rapidly advancing landscape of data-driven decision-making, 
        our team is pioneering an innovative project aimed at extracting tailored 
        business insights from scholarly articles using Generative AI. 
        Our solution is designed to cater to individual user expectations and application areas, 
        transforming complex academic data into actionable business intelligence.
        
    """,
    unsafe_allow_html=True
)

pdf_file = st.file_uploader("Choose a PDF file", accept_multiple_files=False, type='pdf')


if pdf_file:
    print(pdf_file)
    uploaded_article.set_pdf_file(pdf_bytes=pdf_file.getvalue())

col1, col2 = st.columns(2)

occupation = col1.selectbox(
    "Choose the occupation",
    ["Academic Researcher","Business Professional","Student","Entrepreneur"]
)

usage = col2.selectbox(
     "Choose usage",
    ["Academic Research","Business Strategy Development","Personal Knowledge Enhancement","Educational Purposes"]
)

uploaded_article.set_occupation(occupation=occupation)
uploaded_article.set_usage(usage=usage)

if st.button("Let's get started",disabled= pdf_file == None):
    st.switch_page('gui/pages/3_Loading_Page.py')