import streamlit as st
import time
from supabase import create_client

# We store all valid keys and their corresponding group
# True = PS-I (treatment), False = I-PS (control)
key_to_condition = {"3199":True,
                    "7537":False,
                    "2223":True,
                    "2267":False,
                    "6040":True,
                    "7799":False,
                    "8107":True,
                    "7784":False,
                    "4539":True,
                    "6528":False,
                    "4936":True,
                    "4750":False,
                    "6579":True,
                    "7829":False,
                    "6445":True,
                    "8953":False,
                    "6285":True,
                    "8287":False,
                    "5252":True,
                    "1104":False,
                    "xpsi":True,  # These last 2 keys 
                    "xips":False} # are for developers only

def assign_condition(key):
    if key not in key_to_condition:
        st.error(f"The key you entered is not a valid key. Please enter a valid key, or refer to the instructors.")
        return None
    return key_to_condition[key]

# We match the user prefered language adn their PSI condition to the right intruction video
# True = PS-I (treatment), False = I-PS (control)
language_to_video_URL = {("EN", False): "https://youtu.be/jC6q_nrbnh0",
                         ("FR", False): "https://youtu.be/H4ZVQ2oDp1Y", 
                         ("IT", False): "https://youtu.be/LLaubZsj0i4",
                         ("EN", True): "https://youtu.be/DiSFW9hD4RE",
                         ("FR", True): "https://youtu.be/DeGOvEPvlbI", 
                         ("IT", True): "https://youtu.be/LLaubZsj0i4"}

def instructions_URL(PSI, language="EN"):
    if (language, PSI) not in language_to_video_URL:
        st.error(f"The given arguments PSI={PSI} and language={language} are not valid. Please enter the PSI condition of the user (True for PSI, False for IPS), and their prefered language among 'EN', 'IT', and 'FR'.")
        return None
    return language_to_video_URL[(language, PSI)]


def embed_video(video_url, next_page, waiting_time = 3):
    # Initialize session state
    if 'video_start_time' not in st.session_state:
        st.session_state.video_start_time = time.time()
    
    if 'video_next_clicked' not in st.session_state:
        st.session_state.video_next_clicked = False
    
    # Display the video
    st.video(video_url)
    
    # Calculate elapsed time
    elapsed_time = time.time() - st.session_state.video_start_time
    
    # Check if 60 seconds have passed
    if elapsed_time >= waiting_time:
        # Green enabled button
        if st.button("Next", type="primary", use_container_width=False):
            st.session_state.video_next_clicked = True
            st.switch_page(next_page)
    else:
        # Disabled gray button with countdown
        remaining = int(waiting_time - elapsed_time)#int(60 - elapsed_time)
        st.button(f"Next (wait {remaining}s)", disabled=True, use_container_width=False)
        # Auto-refresh every second to update the countdown
        time.sleep(1)
        st.rerun()
        
lang_str_to_key = {"English":"EN", "Français":"FR", "Italiano": "IT"} 
def assign_language(lang_str):
    if lang_str not in lang_str_to_key:
        st.error(f"The language you entered is not a valid choice. You have been assigned to English by default")
        return "EN"
    return lang_str_to_key[lang_str]


def save_prediction_and_clear_text(some_args):
    """Calling this function when clicking on the simulation button in the PS activity
    should save the user's input in the session_state and clear the current input"""
    # TODO
    raise NotImplementedError 


@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)



all_data = {
    # --- Metadata ---
    "user_key",
    "PSI",
    "preferred_language",
    "sex",
    "age",
    "study_domain",
    "study_level",

    # --- Screening scores ---
    "pre_function",
    "pre_derivative",
    "pre_gradient",
    "pre_recursion",

    # --- Pre-test survey ---
    "preq1",
    "preq2",
    "preq3",
    "preq4",
    "preq5",
    "prescore",

    # --- Time spent (INTERVAL) ---
    "time_on_pretest",
    "time_on_context",
    "time_on_instructions",
    "time_on_task",
    "time_on_posttest",

    # --- Simulation data ---
    "sim_counter",
    "answers",  # dict of predictions at each simulation

    # --- Post-test survey ---
    "postq1",
    "postq2",
    "postq3",
    "postq4",
    "postq5",
    "postq6",
    "postq7",
    "postscore",

    # --- Post-test scores ---
    "post_function",
    "post_derivative",
    "post_gradient",
    "post_recursion",
}

def save_user_data_to_supabase(supabase):
    """ This function saves all user data at the end of the experiment in our supabase table"""
    exported_data = {}
    for data in all_data:
        if data in st.session_state:
            exported_data[data] = st.session_state[data]
        else:
            exported_data[data] = None
            
    try:
        response = supabase.table("experiment_data").insert(exported_data).execute()

        st.success("User data saved successfully!")
        return response

    except Exception as e:
        # This catches all Supabase & PostgREST errors
        st.error(f"Error saving user data: {e.message}")
        return None