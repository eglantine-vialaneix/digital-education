# app.py
import streamlit as st
from pages.src.GradientDescent import GradientDescent
import random
import numpy as np
import time
from pages.src.utils import assign_condition


###################### CONSTANTS AND UTILS ######################
if 'X_MIN' not in st.session_state:
    st.session_state.X_MIN = -2.5
    
if 'X_MAX' not in st.session_state:
    st.session_state.X_MAX = 2.5
    
if 'ETA_MIN' not in st.session_state:
    st.session_state.ETA_MIN = 0.001
    
if 'ETA_MAX' not in st.session_state:
    st.session_state.ETA_MAX = 100.0

if 'simulation_counter' not in st.session_state:
    st.session_state.simulation_counter = 0
    
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

TIME_LIMIT_MINUTES = 15
###################### STREAMLIT APP ######################

st.set_page_config(page_title="Cauchy in Matterhorn",
                   page_icon="src/assets/gd_icon.png",
                   layout = "wide",
                   )

############################################################


# Asking key if not already existing
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



# Enters the activity if key provided
if "PSI" in st.session_state and st.session_state.PSI is not None:
        
    # Initialize time variables 
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "activity_done" not in st.session_state:
        st.session_state.activity_done = False

    # --- Check time limit ---
    elapsed = (time.time() - st.session_state.start_time) / 60  # in minutes
    if elapsed >= TIME_LIMIT_MINUTES:
        st.session_state.activity_done = True

    if st.session_state.PSI:
        NEXT_PAGE = "pages/instructions.py"
    else:
        NEXT_PAGE = "pages/posttest.py"
    
    ####################### Activity is over #############################
    if st.session_state.activity_done:
    # Full-width "overlay" style block
        st.markdown(
            """
            <style>
            .overlay-box {
                background-color: rgba(0,0,0,0.85);
                color: white;
                padding: 100px 0;
                text-align: center;
                font-size: 1.5em;
                border-radius: 10px;
                margin-top: 100px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="overlay-box">⏰ <b>Time’s up!</b><br><br>Your 15 minutes are over.<br>Please continue to the next step.</div>',
            unsafe_allow_html=True
        )

        st.balloons()

        if st.button("➡️ Go to Next Step"):
            st.switch_page(NEXT_PAGE)

        st.stop()



    ####################### Activity is not over yet###################
    else:

        st.title("Find your way down the mountain!") 
        
        ############# USER INPUTS AND CURRENT FUNCTION #################
        
        GD = GradientDescent(st.session_state.X_MIN, st.session_state.X_MAX, st.session_state.simulation_counter)
        
        colsetup1, colsetup2 = st.columns([0.6, 0.4], vertical_alignment="center")
        
        with colsetup2:
            st.markdown("##### You are currently on the mountain represented by the function:")
            st.latex('''f(x)=''' + GD.f_in_latex)
            f_fig = GD.plot_naked_function()
            st.plotly_chart(f_fig, use_container_width=True)
        

        ############# USER INPUTS #################

        with colsetup1:
            ############# FORMULA #################
            st.markdown("#### You come up with this brilliant formula that you decide to call **Gradient Descent**:")
            colintro1, colintro2 = st.columns(2)
            with colintro1:

                st.latex(r'''
                \begin{cases} 
                a_0 \in \R \\
                a_{n+1} = a_n - \eta \nabla f(a_n)
                \end{cases}
                ''')

            with colintro2:
                st.markdown("- $a_0$ is your starting point coordinates \n- $\\eta$ is the size of your steps \n- Your goal is to find the minimum of f")

            st.markdown("However, you are not entirely sure if your formula always works… 😥 You must try different settings of the 2 parameters, and understand their effects! The floor is yours!")
            
            st.subheader("Explore your method: when and why does it work❓")
            ########### initial term ###########
            if 'init_value' not in st.session_state:
                st.session_state.init_value = -1.5

            # Create columns with a narrow first column for the label
            colinit0, colinit1, colinit2, colinit3, colinit4, colinit5, colinit6 = st.columns([0.6, 0.8, 1, 1, 1, 1, 1])

            with colinit0:
                colinit0.markdown("#### a₀ =", width="content")
                
            with colinit1:
                st.text_input(
                    "Value", 
                    value=str(st.session_state.init_value),
                    disabled=True,
                    label_visibility="collapsed"
                )
                
            with colinit2:
                if st.button("-1.5", key="btn_neg15", width="stretch"):
                    st.session_state.init_value = -1.5

            with colinit3:
                if st.button("-0.7", key="btn_neg07", width="stretch"):
                    st.session_state.init_value = -0.7
                    
            with colinit4:
                if st.button("0.7", key="btn_pos07", width="stretch"):
                    st.session_state.init_value = 0.7

            with colinit5:
                if st.button("1.5", key="btn_pos15", width="stretch"):
                    st.session_state.init_value = 1.5

            with colinit6:
                if st.button("Random", key="rand_a0", width="content"):
                    st.session_state.init_value = round(
                        random.uniform(st.session_state.X_MIN, st.session_state.X_MAX), 1
                    )
                    st.rerun()
                    

            ######### learning rate ##########
            if 'eta_value' not in st.session_state:
                st.session_state.eta_value = 1.0

            # Create columns with a narrow first column for the label
            coleta3, coleta4, coleta5 = st.columns([0.35, 2.7, 1])

            with coleta3:
                st.markdown("#### η =")
                
            with coleta4:
                # Create logarithmically spaced options
                log_min = np.log10(st.session_state.ETA_MIN)  
                log_max = np.log10(st.session_state.ETA_MAX)    
                num_steps = round(2 * (np.abs(log_min) + np.abs(log_max)) + 1)
                
                log_options = np.linspace(log_min, log_max, num_steps)
                options = [round(10 ** x, 4) for x in log_options]
                
                # Find closest option to current value
                closest_value = min(options, key=lambda x: abs(x - st.session_state.eta_value))
                
                eta_value = st.select_slider(
                    "Learning rate",
                    options=options,
                    value=closest_value,
                    label_visibility="collapsed"
                )
                
                st.session_state.eta_value = eta_value

            with coleta5:
                if st.button("Random", key="random_eta"):
                    # Generate random value on logarithmic scale
                    random_log = random.uniform(log_min, log_max)
                    random_value = 10 ** random_log
                    # Find closest option
                    st.session_state.eta_value = min(options, key=lambda x: abs(x - random_value))
                    st.rerun()

            # Ask the student to predict what will happend given their parameters
            user_text = st.text_area(label="What do you think will happen?",
                                        width="stretch",
                                        placeholder="Your prediction here… (at least 75 characters)")
            
        colsimbutton, colinfomessage = st.columns([0.3, 1], vertical_alignment="center")

        #Simulation button
        with colsimbutton:
            # Disable button if text is less than 50 characters
            run_simulation = st.button("Let's try this!", 
                                        type="primary", 
                                        disabled=len(user_text) < 50,
                                        width="stretch")
        with colinfomessage:
            if not run_simulation:
                # Show character count and requirement message
                char_count = len(user_text)
                if char_count < 50:
                    st.info(f"Please write at least 75 characters to run the simulation. Current: {char_count}/75")
                else:
                    st.success(f"Great! Let's see how it goes. Click the button to run the simulation of your algorithm!")
        
        # Ask for interpretation afterwards
        if run_simulation:
            reflection_text = st.text_area(label="Was your prediction correct? Why?",
                                        width="stretch",
                                        placeholder="Your interpretation here… (at least 75 characters)")

        ############# SIMULATION #################
        if run_simulation:
            try:
                GD.set_a_0(st.session_state.init_value)
                GD.set_eta(st.session_state.eta_value)
                df_gd = GD.gradient_descent()
                
                # Display the plot
                gd_fig = GD.plot_iterations_and_loss()
                st.plotly_chart(gd_fig, use_container_width=True)
                st.session_state.simulation_counter += 1
                #print(st.session_state.simulation_counter)
                
                
            except Exception as e:
                st.error(f"Error: {str(e)}")













###################### GUESSING THE FORMULA #############################


# match_elements = {
#     'aₙ': 'a_n', 
#     '∇f(': 'self.grad_f(', 
#     'f(': 'self.f(', 
#     ')': ')', 
#     'η': 'self.eta', 
#     '+': '+', 
#     '-': '-', 
#     '÷': '/', 
#     '⨉': '*'
# }

# def extract_guessed_formula(string_formula):
#     assert len(string_formula.split('(')) == len(string_formula.split(')')), \
#         "Be careful! Your formula has unmatched parenthesis."
    
#     elements = string_formula.split()
#     matched = [match_elements[element] for element in elements]
    
#     return ' '.join(matched)


# # Initialize session state for formula if it doesn't exist
# if 'formula' not in st.session_state:
#     st.session_state.formula = ""

# # Initial value input
# col1, col2 = st.columns([3, 1])
# with col1:
#     init_value = st.number_input(
#         "a₀ = ", 
#         min_value=st.session_state.X_MIN, 
#         max_value=st.session_state.X_MAX, 
#         value=1.5, 
#         step=0.1
#     )
# with col2:
#     if st.button("Random"):
#         init_value = round(random.uniform(st.session_state.X_MIN, st.session_state.X_MAX), 1)
#         st.rerun()

# # Use random value if set
# #if 'random_init' in st.session_state:
# #    init_value = st.session_state.random_init

# # Formula display
# st.text_area(
#     "aₙ₊₁ = ",
#     value=st.session_state.formula,
#     height=60,
#     key="formula_display",
#     disabled=True,
#     placeholder="Try and find the formula for gradient descent..."
# )

# # Word buttons
# st.write("Build your formula:")
# words = ["aₙ", "∇f(", "f(", ")", "η", "+", "-", "÷", "⨉"]

# # Create buttons in rows
# cols = st.columns(len(words))
# for idx, word in enumerate(words):
#     with cols[idx]:
#         if st.button(word, key=f"btn_{word}"):
#             st.session_state.formula += word + " "
#             st.rerun()


# # Control buttons
# col1, col2 = st.columns(2)
# with col1:
#     if st.button("⌫ Erase all", type="secondary"):
#         st.session_state.formula = ""
#         st.rerun()

# with col2:
#     run_simulation = st.button("Let's try this one!", type="primary")

# # Run simulation
# if run_simulation and st.session_state.formula:
#     try:
#         guess_formula = extract_guessed_formula(st.session_state.formula)
        
#         GD = GradientDescent(st.session_state.X_MIN, st.session_state.X_MAX)
#         GD.set_a_0(init_value)
#         GD.set_eta(st.session_state.eta)
#         df_gd = GD.gradient_descent(guess_formula)
        
#         # Display the plot
#         fig = GD.plot_iterations_and_loss()
#         st.plotly_chart(fig, use_container_width=True)
        
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
# elif run_simulation:
#     st.warning("Please build a formula first!")

#########################################################################



