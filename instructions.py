# instructions.py

import streamlit as st
from src.utils import instructions_URL, assign_condition

# This page contains the instruction video 
# It automatically adapts on the condition of the user, givne by their key

st.markdown("## Watch a short video and learn about a fascinating subject! 🏔️📈")

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


st.markdown("What language do you prefer having the instructions in? 🌍")

# Default video is in english
if 'prefered_language' not in st.session_state:
    st.session_state.prefered_language = "EN"

coleng, colfr, colit = st.columns(3)   

with coleng:
    if st.button("English", width="stretch"):
        st.session_state.prefered_language = "EN"  

with colfr:
    if st.button("Français", width="stretch"):
        st.session_state.prefered_language = "FR"  

with colit:
    if st.button("Italiano", width="stretch"):
        st.session_state.prefered_language = "IT"  

if "PSI" in st.session_state:
    st.video(instructions_URL(st.session_state.PSI, st.session_state.prefered_language))