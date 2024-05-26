from utilities import hide_sidebar
import streamlit as st
import os

hide_sidebar()

_ = """
    To start the app, run ``` streamlit run streamlit_app.py ```
"""

REPLICATE_API_TOKEN = st.text_input("Enter Replicate API key")
if st.button("Save API Key"):
    os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN
    st.switch_page("gui/pages/0_Start_Page.py")
