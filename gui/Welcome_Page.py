from utilities import hide_sidebar
import streamlit as st
import os

hide_sidebar()

_ = """
    To start the app, run ``` streamlit run Welcome_Page.py ```
"""

REPLICATE_API_KEY = st.text_input("Enter Replicate API key")
if st.button("Save API Key"):
    os.environ['REPLICATE_API_KEY'] = REPLICATE_API_KEY
    st.switch_page("pages/0_Start_Page.py")
