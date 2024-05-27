from utilities import hide_sidebar
import streamlit as st
import os

hide_sidebar()

_ = """
    To start the app, run ``` streamlit run streamlit_app.py ```
"""

REPLICATE_API_TOKEN = st.text_input("Enter Replicate API key")
if st.button("Save API Key"):
    if REPLICATE_API_TOKEN == "":
        st.warning('Please enter an API key', icon="🚨")
    else:
        os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN
        st.switch_page("pages/0_Start_Page.py")

