#home.py
import streamlit as st
from pages.src.utils import assign_condition, init_supabase, save_user_data_to_supabase

###################### STREAMLIT APP ######################

st.set_page_config(page_title="Cauchy in Matterhorn",
                   page_icon="src/assets/gd_icon.png",
                   layout = "wide",
                   )

############################################################

# This page is intended to contain the context video
# It will be used to ask the participants their private key, 
# which not only assigns them to their condition (PS-I or I-PS)
# but also acts as a password to direct them to the correct page (instructions first or PS activity first)
# The key also allow us to same the user data in a pseudonymized fashion.

if "prefered_language" not in st.session_state:
    st.markdown("### What language do you prefer having the experience in? 🌍")

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
    
    if "PSI" not in st.session_state or st.session_state.PSI is None:
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
            st.session_state.PSI = assign_condition(st.session_state.user_key)  

    if "PSI" in st.session_state and st.session_state.PSI is not None:

        # Initialize form submission state if it doesn't exist
        if 'screening_test_submitted' not in st.session_state:
            st.session_state.screening_test_submitted = False
            
        # Only show the form if it hasn't been submitted
        if not st.session_state.screening_test_submitted:
            with st.form("screening_test", enter_to_submit=False):
                
                # Basic info
                intro_screening_test = {"EN":"Please answer these few questions about yourself:", 
                                        "FR":"Réponds à ces quelques questions à propos de toi:", 
                                        "IT":"Rispondi alle seguenti domande su di te:"}
                
                st.write(intro_screening_test[st.session_state.prefered_language])
                
                sex_label = {"EN":"Sex:", 
                            "FR":"Sexe:", 
                            "IT":"Sesso:"}
                
                
                sex_options = {"EN":["", "Female", "Male", "Prefer not to say"],
                               "FR":["", "Femme", "Homme", "Préfère ne pas dire"],
                               "IT":["", "Donna", "Uomo", "Preferisco non dirlo"]
                                }
                
                sex = st.selectbox(
                    sex_label[st.session_state.prefered_language],
                    options=sex_options[st.session_state.prefered_language]
                )
                
                age_labels = {"EN":"Age", "FR":"Âge", "IT":"Età"}
                age = st.number_input(
                    age_labels[st.session_state.prefered_language],
                    min_value=16,
                    max_value=100,
                    step=1,
                    value=None
                )
                
                study_labels = {"EN":"Field of study:", 
                                "FR":"Domaine d'études:", 
                                "IT":"Ambito di Studio:"}
                study_domain = st.text_input(study_labels[st.session_state.prefered_language])
                
                level_labels = {"EN":"Study level:", 
                                "FR":"Niveau d'études:", 
                                "IT":"Livello di istruzione"}
                level_options = {"EN":["", "Bachelor - Year 1", "Bachelor - Year 2", "Bachelor - Year 3",
                                        "Master - Year 1", "Master - Year 2", "PhD", "Other"], 
                                 "FR":["", "Bachelor - 1ère année", "Bachelor - 2ème année", "Bachelor - 3ème année",
                                        "Master - 1ère année", "Master - 2ème année", "Doctorat", "Autre"], 
                                 "IT":["", "Triennale - Primo anno", "Triennale - Secondo anno", "Triennale - Terzo anno",
                                        "Magistrale - Primo anno", "Magistrale  - Secondo anno", "Dottorato", "Altro"]}
                study_level = st.selectbox(
                    level_labels[st.session_state.prefered_language],
                    options=level_options[st.session_state.prefered_language]
                )

                # Screening for prerequisite knowledge
                disclaimers = {"EN":"The following questions are not graded. They are only for us to know better your background. 😊",
                               "FR":"Les questions qui suivent ne sont pas notées. Elles sont simplement là pour que nous en sachions plus sur tes connaissances préalables. 😊", 
                               "IT":"Le seguenti domande non verranno prese in considerazione durante la valutazione dell’esperimento. Servono solo a noi per conoscerti meglio e sapere il tuo background. 😊"}
                st.write(disclaimers[st.session_state.prefered_language])
                
                function_labels = {"EN":"How familiar are you with functions? (Do you know what a function is and some of their representations like graphs?)", 
                                   "FR":"À quel point es-tu à l'aise avec la notion de fonction ? (Sais-tu ce qu'est une fonction and comment les représentater en graphes ?)", 
                                   "IT":"Quanto ti consideri esperto con le funzioni? (Sai ​​cos'è una funzione e conosci delle sue rappresentazioni come ad esempio i grafici?)"} 
                help_labels = {"EN":"1 = Not familiar at all, 5 = Very familiar", 
                               "FR":"1 = Pas à l'aise du tout, 5 = Très à l'aise", 
                               "IT":"1 = Non sono esperto per niente, 5 = Molto esperto"} 
                function = st.slider(
                    function_labels[st.session_state.prefered_language],
                    min_value=1,
                    max_value=5,
                    value=None,
                    help=help_labels[st.session_state.prefered_language]
                )
                derivative_labels = {"EN":"How familiar would you consider yourself regarding derivatives?", 
                                     "FR":"À quel point es-tu à l'aise avec la notion de dérivée ?", 
                                     "IT":"Quanto ti consideri esperto di derivate?"}
                derivative = st.slider(
                    derivative_labels[st.session_state.prefered_language],
                    min_value=1,
                    max_value=5,
                    value=None,
                    help=help_labels[st.session_state.prefered_language]
                )
                gradient_labels = {"EN":"How familiar would you consider yourself regarding gradients ($\\nabla f$)?", 
                                   "FR":"À quel point es-tu à l'aise avec la notion de gradient ($\\nabla f$) ?", 
                                   "IT":"Quanto ti consideri esperto di gradienti ($\\nabla f$)?"}
                gradient = st.slider(
                    gradient_labels[st.session_state.prefered_language],
                    min_value=1,
                    max_value=5,
                    value=None,
                    help=help_labels[st.session_state.prefered_language]
                )
                recursion_labels = {"EN":"How familiar are you with recursion and recursive formulas/algorithms?", 
                                    "FR":"À quel point es-tu à l'aise avec la notion de récursion et d'algorithme et de formule récursive ?", 
                                    "IT":"Quanto ti consideri esperto di ricorsione e formule/algoritmi ricorsivi?"}
                recursion = st.slider(
                    recursion_labels[st.session_state.prefered_language],
                    min_value=1,
                    max_value=5,
                    value=None,
                    help=help_labels[st.session_state.prefered_language]
                )
                
                submission_labels = {"EN":"Submit my info. (You won't be able to change them anymore)", 
                                     "FR":"Soumettre mes informations. (Tu ne pourras plus les changer)", 
                                     "IT":"Invia le mie informazioni. (Non potrai più modificarle)"}
                screening_test = st.form_submit_button(submission_labels[st.session_state.prefered_language])

            # Check if form was submitted
            if screening_test:
                # Store the form data in session state
                st.session_state.sex = sex
                st.session_state.age = age
                st.session_state.study_domain = study_domain
                st.session_state.study_level = study_level
                st.session_state.pre_function = function
                st.session_state.pre_derivative = derivative
                st.session_state.pre_gradient = gradient
                st.session_state.pre_recursion = recursion
                
                # Mark form as submitted
                st.session_state.screening_test_submitted = True
                
          
        else:
            # Saving submitted form
            ty_labels = {"EN":"Thank you! Your information has been submitted.", 
                        "FR":"Merci! Tes informations ont bien été enregistrées.", 
                        "IT":"Grazie! Le tue informazioni sono state inviate."}
            supabase = init_supabase()
            save_user_data_to_supabase(supabase, success_message=ty_labels[st.session_state.prefered_language])

            # Form has been submitted, moving on to context
            if st.button("Next"):
                st.switch_page("pages/pretest.py")

                

pages=[
    st.Page("app.py", title="Login and tell us about yourself"),
    st.Page("pages/pretest.py", title="Pre-test"),
    st.Page("pages/instructions.py", title="Learn about Gradient Descent"),
    st.Page("pages/psactivity.py", title="Problem-Solving"),
    st.Page("pages/posttest.py", title="How much did you learn today?"),
]