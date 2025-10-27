# app.py
import streamlit as st
from src.utils import GradientDescent
import random

###### CONSTANTS AND UTILS ######
st.session_state.X_MIN = -2.0
st.session_state.X_MAX = 2.0
st.session_state.eta = 0.1

match_elements = {
    'aₙ': 'a_n', 
    '∇f(': 'self.grad_f(', 
    'f(': 'self.f(', 
    ')': ')', 
    'η': 'self.eta', 
    '+': '+', 
    '-': '-', 
    '÷': '/', 
    '⨉': '*'
}

def extract_guessed_formula(string_formula):
    assert len(string_formula.split('(')) == len(string_formula.split(')')), \
        "Be careful! Your formula has unmatched parenthesis."
    
    elements = string_formula.split()
    matched = [match_elements[element] for element in elements]
    
    return ' '.join(matched)

###### STREAMLIT APP ######

st.title("Find an algorithm to go down the mountain!")

# Initialize session state for formula if it doesn't exist
if 'formula' not in st.session_state:
    st.session_state.formula = ""

# Initial value input
col1, col2 = st.columns([3, 1])
with col1:
    init_value = st.number_input(
        "a₀ = ", 
        min_value=st.session_state.X_MIN, 
        max_value=st.session_state.X_MAX, 
        value=1.5, 
        step=0.1
    )
with col2:
    if st.button("Random"):
        init_value = round(random.uniform(st.session_state.X_MIN, st.session_state.X_MAX), 1)
        st.rerun()

# Use random value if set
#if 'random_init' in st.session_state:
#    init_value = st.session_state.random_init

# Formula display
st.text_area(
    "aₙ₊₁ = ",
    value=st.session_state.formula,
    height=60,
    key="formula_display",
    disabled=True,
    placeholder="Try and find the formula for gradient descent..."
)

# Word buttons
st.write("Build your formula:")
words = ["aₙ", "∇f(", "f(", ")", "η", "+", "-", "÷", "⨉"]

# Create buttons in rows
cols = st.columns(len(words))
for idx, word in enumerate(words):
    with cols[idx]:
        if st.button(word, key=f"btn_{word}"):
            st.session_state.formula += word + " "
            st.rerun()

# Control buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("⌫ Erase all", type="secondary"):
        st.session_state.formula = ""
        st.rerun()

with col2:
    run_simulation = st.button("Let's try this one!", type="primary")

# Run simulation
if run_simulation and st.session_state.formula:
    try:
        guess_formula = extract_guessed_formula(st.session_state.formula)
        
        GD = GradientDescent(st.session_state.X_MIN, st.session_state.X_MAX)
        GD.set_a_0(init_value)
        GD.set_eta(st.session_state.eta)
        df_gd = GD.gradient_descent(guess_formula)
        
        # Display the plot
        fig = GD.plot_iterations_and_loss()
        #st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
elif run_simulation:
    st.warning("Please build a formula first!")