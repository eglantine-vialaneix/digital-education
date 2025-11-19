import streamlit as st
from pages.src.utils import assign_condition, init_supabase, save_user_data_to_supabase

###################### STREAMLIT APP ######################

st.set_page_config(page_title="Cauchy in Matterhorn",
                   page_icon="src/assets/gd_icon.png",
                   layout = "wide",
                   )

############################################################

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

st.markdown("Congratulations! You arrived home and your oven is safely off. Most importantly you learnt (we hope!) about Gradient Descent, and helped us running our experiment, so thanks a lot!")

if st.button("FIN"):
    supabase = init_supabase()
    save_user_data_to_supabase(supabase)