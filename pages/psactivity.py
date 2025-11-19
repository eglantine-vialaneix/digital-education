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
    # Asking key if not already existing
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
            times_up_labels = {"EN":'<div class="overlay-box">⏰ <b>Time’s up!</b><br><br>Your 15 minutes are over.<br>Please continue to the next step.</div>', 
                               "FR":'<div class="overlay-box">⏰ <b>Temps écoulé !</b><br><br>Tes 15 minutes sont terminées.<br>Continue vers la prochaine étape.</div>', 
                               "IT":'<div class="overlay-box">⏰ <b>Il tempo è scaduto!</b><br><br>I tuoi 15 minuti sono scaduti.<br>Continua con il passaggio successivo.</div>'}
            st.markdown(
                times_up_labels[st.session_state.prefered_language],
                unsafe_allow_html=True
            )

            st.balloons()

            switch_label = {"EN":"➡️ Go to Next Step", 
                            "FR":"➡️ Va à la prochaine étape", 
                            "IT":"➡️ Vai al passaggio successivo"}
            if st.button(switch_label[st.session_state.prefered_language]):
                st.switch_page(NEXT_PAGE)

            st.stop()



        ####################### Activity is not over yet###################
        else:
            
            title_labels = {"EN":"Find your way down the mountain!", 
                            "FR":"Trouve ton chemin vers le bas de la montagne !", 
                            "IT":"Trova la strada per scendere dalla montagna!"}
            st.title(title_labels[st.session_state.prefered_language]) 
            
            ############# USER INPUTS AND CURRENT FUNCTION #################
            
            GD = GradientDescent(st.session_state.X_MIN, st.session_state.X_MAX, st.session_state.simulation_counter)
            
            colsetup1, colsetup2 = st.columns([0.6, 0.4], vertical_alignment="center")
            
            with colsetup2:
                fct_labels = {"EN":"##### You are currently on the mountain represented by the function:", 
                              "FR":"##### Tu es actuellement sur la montagne représentée par la fonction:", 
                              "IT":"##### Ti trovi attualmente sulla montagna rappresentata dalla funzione:"}
                st.markdown(fct_labels[st.session_state.prefered_language])
                st.latex('''f(x)=''' + GD.f_in_latex)
                f_fig = GD.plot_naked_function()
                st.plotly_chart(f_fig, use_container_width=True)
            

            ############# USER INPUTS #################

            with colsetup1:
                ############# FORMULA #################
                brilliant_labels = {"EN":"#### You come up with this brilliant formula that you decide to call **Gradient Descent**:", 
                                    "FR":"#### Une brillante formule te vient à l'esprit! Tu décides de l'appeler **Gradient Descent**:",
                                    "IT":"#### Ti viene in mente questa brillante formula che decidi di chiamare **Gradient Descent**:"}
                st.markdown(brilliant_labels[st.session_state.prefered_language])
                colintro1, colintro2 = st.columns(2)
                with colintro1:

                    st.latex(r'''
                    \begin{cases} 
                    a_0 \in \R \\
                    a_{n+1} = a_n - \eta \nabla f(a_n)
                    \end{cases}
                    ''')

                with colintro2:
                    param_labels = {"EN":"- $a_0$ is your starting point coordinates \n- $\\eta$ is the size of your steps \n- Your goal is to find the minimum of $f$", 
                                    "FR":"- $a_0$ est la coordonée de ton point de départ \n- $\\eta$ est la taille de tes pas \n- Ton but est de trouver le minimum de $f$", 
                                    "IT":"- $a_0$ sono le coordinate del tuo punto di partenza \n- $\\eta$ è la lunghezza dei tuoi passi \n- Il tuo obiettivo è trovare il minimo di $f$"}
                    st.markdown(param_labels[st.session_state.prefered_language])

                doubts_labels = {"EN":"However, you are not entirely sure if your formula always works… 😥 You must try different settings of the 2 parameters, and understand their effects! The floor is yours!", 
                                 "FR":"Cependant, tu n'es pas entièrement sûr.e que ta formule fonctionne toujours… 😥 Tu dois essayer différentes configurations de tes 2 paramètres et comprendre leurs effets ! À toi de jouer !", 
                                 "IT":"Tuttavia, non sei del tutto sicuro che la tua formula funzioni sempre… 😥 Devi provare diverse impostazioni dei 2 parametri e comprenderne gli effetti! Ora tocca a te!"}
                st.markdown(doubts_labels[st.session_state.prefered_language])
                
                explore_labels = {"EN":"Explore your method: when and why does it work❓", 
                                  "FR":"Explore ta méthode: quand et pourquoi fonctionne-t-elle ❓", 
                                  "IT":"Esplora il tuo metodo: quando e perché funziona❓"}
                st.subheader(explore_labels[st.session_state.prefered_language])
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
                prediction_labels = {"EN":"What do you think will happen?", 
                                     "FR":"Que penses-tu qu'il va se passer ?", 
                                     "IT":"Cosa pensi che accadrà?"}
                prediction_placeholders = {"EN":"Your prediction here… (at least 75 characters)", 
                                           "FR":"Écris ta prédiction ici… (minimum 75 caractères)", 
                                           "IT":"Inserisci qui la tua previsione... (almeno 75 caratteri)"}
                user_text = st.text_area(label=prediction_labels[st.session_state.prefered_language],
                                            width="stretch",
                                            placeholder=prediction_placeholders[st.session_state.prefered_language])
                
            colsimbutton, colinfomessage = st.columns([0.4, 1], vertical_alignment="center")

            #Simulation button
            with colsimbutton:
                # Disable button if text is less than 50 characters
                try_labels = {"EN":"⬇️ Let's try this! See simulation below ! ⬇️", 
                              "FR":"⬇️ Essayons comme ça ! Regarde la simulation ci-dessous ! ⬇️", 
                              "IT":"⬇️ Proviamo! Vedi la simulazione sotto! ⬇️"}
                run_simulation = st.button(try_labels[st.session_state.prefered_language], 
                                            type="primary", 
                                            disabled=len(user_text) < 50,
                                            width="stretch")
            with colinfomessage:
                if not run_simulation:
                    # Show character count and requirement message
                    char_count = len(user_text)
                    if char_count < 50:
                        info_labels = {"EN":f"Please write at least 75 characters to run the simulation. Current: {char_count}/75", 
                                       "FR":f"Tu dois écrire au moins 75 caractères pour pouvoir lancer la simulation. Tu es à: {char_count}/75", 
                                       "IT":f"Scrivi almeno 75 caratteri per eseguire la simulazione. Attuale:{char_count}/75"}
                        st.info(info_labels[st.session_state.prefered_language])
                    else:
                        success_labels = {"EN":"Great! Let's see how it goes. Click the button to run the simulation of your algorithm!", 
                                          "FR":"Super ! Voyons ce que ça donne. Click sur le bouton pour lancer la simulation de ton algorithme !", 
                                          "IT":"Fantastico! Vediamo cosa succede. Clicca sul pulsante per eseguire la simulazione del tuo algoritmo!"}
                        st.success(success_labels[st.session_state.prefered_language])

            # Ask for interpretation afterwards
            if run_simulation:
                reflect_labels = {"EN":"Was your prediction correct? Why?", 
                                  "FR":"Ta prédiction était-elle correcte ? Pourquoi ?", 
                                  "IT":"La tua previsione era corretta? Perché?"}
                reflect_placeholders = {"EN":"Your interpretation here… ", 
                                        "FR":"Écris ton interprétation ici… ", 
                                        "IT":"Inserisci qui la tua interpretazione…"}
                reflection_text = st.text_area(label=reflect_labels[st.session_state.prefered_language],
                                            width="stretch",
                                            placeholder=reflect_placeholders[st.session_state.prefered_language])

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