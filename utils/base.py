import streamlit as st

def base(): 
    st.set_page_config(
        page_title='Earthquake Localization and Direction', 
        layout="wide",
        initial_sidebar_state = "expanded",
    )

    title="""
        <h1 style='text-align: center; color: Green;'>
            Earthquake Detections
        </h1>
    """
    st.markdown(title, unsafe_allow_html=True)