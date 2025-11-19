# instructions.py

import streamlit as st
from pages.src.utils import instructions_URL, assign_condition, embed_video

###################### STREAMLIT APP ######################

st.set_page_config(page_title="Cauchy in Matterhorn",
                   page_icon="src/assets/gd_icon.png",
                   layout = "wide",
                   )

############################################################


# This page contains the instruction video 
# It automatically adapts on the condition of the user, givne by their key

if "prefered_language" not in st.session_state:
    st.markdown("### What language do you prefer? 🌍")

    coleng, colfr, colit = st.columns(3)   

    with coleng:
        if st.button("English", width="stretch"):
            st.session_state.prefered_language = "EN"  
            st.rerun()

    with colfr:
        if st.button("Français", width="stretch"):
            st.session_state.prefered_language = "FR"  
            st.rerun()

    with colit:
        if st.button("Italiano", width="stretch"):
            st.session_state.prefered_language = "IT" 
            st.rerun() 

else: 
    video_labels = {"EN":"## Watch a short video and learn about a fascinating subject! 🏔️📈", 
                    "FR":"## Regarder cette courte vidéo sur un sujet absolument fascinant ! 🏔️📈", 
                    "IT":"## Guarda un breve video e scopri un argomento affascinante! 🏔️📈"}
    st.markdown(video_labels[st.session_state.prefered_language])

    if "PSI" not in st.session_state:
        if "user_key" not in st.session_state:
            labels = {"EN":"Please enter your personal key:", 
                      "FR":"Entre ta clé personnelle:", 
                      "IT":"Inserisci la tua chiave personale:"}
            user_key = st.text_input(label=labels[st.session_state.prefered_language],
                                    type="password",
                                    width="stretch",
                                    icon="🔐",
                                    max_chars=4
                                    )
        if user_key:
            st.session_state.user_key = user_key
            st.session_state.PSI = assign_condition(user_key)




    if "PSI" in st.session_state:
        if st.session_state.PSI:
            next_page="pages/posttest.py"
        else:
            next_page="pages/psactivity.py"
        embed_video(instructions_URL(st.session_state.PSI, st.session_state.prefered_language), next_page)