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

# Initialization
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

def create_images_section():
    items = st.session_state.images_and_explanations
    for key,value in items:
        if value['image'] != None:
            st.image(image=value['image'])
        st.write(f"### {key}")
        st.write(value['explanation'])
        st.markdown('#')
        st.markdown('#')
        st.markdown('#')

def create_images_in_container():
    items = st.session_state.images_and_explanations
    if items:
        num_columns = 3
        # We'll use all the available space in the page for the columns.
        columns = st.columns(num_columns)
        index = 0
        for key,value in items:
            if value['image']:  # Ensure there's an image to display
                col = columns[index % num_columns]  # Dynamic column assignment
                with col:
                    st.write(f"### {key}")
                    st.write(value['explanation'])
                    st.image(image=value['image'], use_column_width=True)
            else:
                col = columns[index % num_columns]  # Dynamic column assignment
                with col:
                    st.write(f"### {key}")
                    st.write(value['explanation'])
            index += 1
        st.markdown('---')  # Add spacing or separation
    
def create_insights_and_title():
    title_place = st.empty()
    insights_place = st.empty()

    with insights_place:
        st.session_state.insights = st.write_stream(report.get_insights)

    with title_place:
        st.session_state.title = st.write_stream(report.get_title)
    
    st.session_state.images_and_explanations = report.get_images().items()
    st.write('##')
    st.markdown(
        """
        <span style="font-size: larger; font-weight: bold;">
            The images selected from the article and their explanations serve to deepen the comprehension of the insights provided. 
            Please consider reviewing these visual aids to gain a fuller understanding of the content.
        </span>
        """,
        unsafe_allow_html=True
    )
    st.write('##')
    create_images_in_container()

def load_insights_and_title():
    st.write(st.session_state.title)
    st.write(st.session_state.insights)
    st.write('##')
    create_images_in_container()
    
if "insights" not in st.session_state:
    create_insights_and_title()
else:
    load_insights_and_title()

pdf_file = report.generate_pdf()
st.download_button('Save PDF',pdf_file,file_name=f"report.pdf")

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

#if st.button("Regenerate"):
#    st.switch_page('pages/2_Regenerate_Page.py')

if st.button("Generate New Article"):
    Report.delete_instance()
    UploadedArticle.delete_instance()

    for key in st.session_state.keys():
        del st.session_state[key]

    st.switch_page('Hello.py')