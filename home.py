#home.py
import streamlit as st
from pages.src.utils import assign_condition, embed_video


# This page is intended to contain the context video
# It will be used to ask the participants their private key, 
# which not only assigns them to their condition (PS-I or I-PS)
# but also acts as a password to direct them to the correct page (instructions first or PS activity first)
# The key also allow us to same the user data in a pseudonymized fashion.

if "PSI" not in st.session_state or st.session_state.PSI is None:
    user_key = st.text_input(label="Please enter your personal key:",
                             type="password",
                             width="stretch",
                             icon="🔐",
                             max_chars=4
                             )
    if user_key:
        st.session_state.user_key = user_key
        st.session_state.PSI = assign_condition(st.session_state.user_key)  

if "PSI" in st.session_state and st.session_state.PSI is not None:

    # Initialize form submission state if it doesn't exist
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
        
    # Only show the form if it hasn't been submitted
    if not st.session_state.form_submitted:
        with st.form("screening_and_pretest"):
            
            # Basic info
            st.write("Please answer these few questions about yourself:")
            sex = st.selectbox(
                "Sex:",
                options=["Male", "Female", "Prefer not to say"]
            )
            age = st.number_input(
                "Age:",
                min_value=16,
                max_value=100,
                step=1
            )
            study_domain = st.text_input("Field of study:")
            study_level = st.selectbox(
                "Study level:",
                options=["Bachelor - Year 1", "Bachelor - Year 2", "Bachelor - Year 3",
                        "Master - Year 1", "Master - Year 2", "PhD", "Other"]
            )
            
            # Screening for prerequisite knowledge
            st.write("The following questions are not graded. They are only for us, to better understand the background you come with before our experiment. Remember that our tool is a learning tool, so we are here to teach you about a specific notion. This notion is very related with a few other that we might also teach you about during the experiment. We would simply like to assess that as well.")
            
            function = st.slider(
                "How familiar are you with functions? (Do you know what a function is and some of their representations like graphs?)",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Not familiar at all, 5 = Very familiar"
            )
            derivative = st.slider(
                "How familiar would you consider yourself regarding derivatives?",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Not familiar at all, 5 = Very familiar"
            )
            gradient = st.slider(
                "How familiar would you consider yourself regarding gradients ($\\nabla f$)?",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Not familiar at all, 5 = Very familiar"
            )
            recursion = st.slider(
                "How familiar are you with recursion and recursive formulas/algorithms?",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Not familiar at all, 5 = Very familiar"
            )
            
            screening_and_pretest = st.form_submit_button("Submit my info. (You won't be able to change them anymore)")

        # Check if form was submitted
        if screening_and_pretest:
            # Store the form data in session state
            st.session_state.sex = sex
            st.session_state.age = age
            st.session_state.study_domain = study_domain
            st.session_state.study_level = study_level
            st.session_state.function = function
            st.session_state.derivative = derivative
            st.session_state.gradient = gradient
            st.session_state.recursion = recursion
            
            # Mark form as submitted
            st.session_state.form_submitted = True
            
            # Rerun to update the UI
            st.rerun()
            
# TODO: write the result of the screening questionnaire and pretest in the excel sheets
# URL: https://docs.google.com/spreadsheets/d/1cioGHPbZ3bIyVZ7Hzy8dgdfcIZK6r7shRgpvgSajpdE/edit?gid=132239610#gid=132239610

# does this work? idk need to try
# st.write("gratitude word")
# with open("file.csv", "w") as f:
#     print("xxx", file=f)
                   
            
    else:
        # Form has been submitted, moving on to context
        st.success("Thank you! Your information has been submitted.")

        st.markdown("## Let's start! With a little bit of context… 👯")
        if "PSI" not in st.session_state:
            st.error(f"No PSI condition has been assigned yet.")
        elif st.session_state.PSI:
            # display context video for PSI then move on to the PS activity
            embed_video("https://youtu.be/suYJGx3ailE", 'pages/app.py')
        else:
            # display context video for IPS then move on to the instructions
            embed_video("https://youtu.be/fd5T80Pc4FY", 'pages/instructions.py')

            

pages=[
    st.Page("home.py", title="Login and tell us about yourself"),
    st.Page("pages/instructions.py", title="Learn about Gradient Descent"),
    st.Page("pages/app.py", title="Problem-Solving"),
    st.Page("pages/posttest.py", title="How much did you learn today?"),
]

#pg = st.navigation(pages, position="top")
