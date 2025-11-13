import streamlit as st
from pages.src.utils import assign_condition

if "PSI" not in st.session_state:
    if "user_key" not in st.session_state:
        user_key = st.text_input(label="Please enter your personal key:",
                                type="password",
                                width="stretch",
                                icon="🔐",
                                max_chars=4
                                )
    if user_key:
        st.session_state.user_key = user_key
        st.session_state.PSI = assign_condition(user_key)

