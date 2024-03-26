import streamlit as st
import pandas as pd
from io import StringIO
from utilities import *
from structures import UploadedArticle


st.set_page_config(
    page_title="Insight Extractor",
    layout="wide",
)

_ = """
    To start the app, run ``` streamlit run Hello.py ```
"""


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

uploaded_article = UploadedArticle(pdf_file)


col1, col2 = st.columns(2)

col1.selectbox(
    "Choose the occupation",
    ["Academic Researcher","Business Professional","Student","Entrepreneur"]
)

col2.selectbox(
     "Choose usage",
    ["Academic Research","Business Strategy Development","Personal Knowledge Enhancement","Educational Purposes"]
)

if st.button("Let's get started"):
    st.switch_page('pages/3_Loading_Page.py')


