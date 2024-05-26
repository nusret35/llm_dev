import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from utilities import *

st.set_page_config(page_title="Regenerate Report",layout="wide")
hide_sidebar()

st.title("Regenerate Report")

st.markdown("#### Please let us know why you're requesting a regeneration of the insights extracted from the scholarly article. Your feedback is valuable in helping us improve.")

reason = st.selectbox(
    "Select the option that best describes your reason",
    [
        "",
        "Too short – The insights didn't provide enough detail.",
        "Too long – The insights were more detailed than necessary, making it hard to extract useful information.",
        "Too broad – The insights were not specific enough to the topic of interest.",
        "Not actionable – The insights didn't provide clear next steps or actionable information.",
        "Lacked depth or complexity – The insights did not delve deeply into the topic or missed critical nuances.",
        "Other - Please specify"
    ],
)

other_reason = ""
if reason == "Other - Please specify":
    other_reason = st.text_area(label="Specify the reason for regeneration")

is_disabled = True
if reason == "":
    pass
else:
    if reason != "Other - Please specify":
        is_disabled = False
    else:
        if other_reason != "":
            is_disabled = False

st.button(
    "Regenerate",
    disabled=is_disabled
)