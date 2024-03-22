import streamlit as st

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
        .normal-font {
            font-size:10px !important;
        }
                
    </style>
    """, unsafe_allow_html=True)

def list_insights(insights):
    all_insights = ""
    for insight in insights:
        all_insights += f'<li class="insight">{insight}</li>'
    
    return all_insights