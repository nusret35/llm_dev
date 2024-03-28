import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
import threading
import time
import numpy as np
from utilities import *
from structures import Report,UploadedArticle


st.set_page_config(page_title="Report",layout="wide")

hide_sidebar()


report = Report()
uploaded_article = UploadedArticle()


st.markdown(
    """
        <style>
            .insight {
                font-size: 50px;
                margin-bottom:20px;
            }
        </style>
    """, unsafe_allow_html=True
)

title_place = st.empty()

insights_place = st.empty()

with insights_place:
    st.write_stream(report.get_insights)


with title_place:
    st.write_stream(report.get_title)
    


"""
st.image(report.images_and_explanations['Fig. 1 Some Picture']['image'])
"""


st.button("Save as PDF")

col1, _ = st.columns([1,2])

insights_rating = col1.slider(
        "Are you happy with the insights?",
        help="1 is not happy at all, 5 is very happy",
        value=(3),
        max_value=5,
        min_value=1
)

st.markdown(
    """<style>
div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 24px;
}
    </style>
    """, unsafe_allow_html=True)



if st.button("Regenerate"):
    st.switch_page('pages/2_Regenerate_Page.py')

if st.button("Generate New Article"):
    st.switch_page('Hello.py')
