import os
import time
import streamlit as st

from utils.base import base
from utils.constants import CONFIG_FP

base()


def update_token():
    if (token:=st.session_state['token']) and len(token)>10:
        with open(CONFIG_FP, 'w') as f:
            f.write(token)
    else:
        st.warning("Can't Update the token.")


with st.sidebar as s_bar:
    st.session_state['token'] = st.text_input(
        "Enter ACCESS TOKEN:",
        type='password'
    )
    
    st.button("Update", on_click=update_token)


