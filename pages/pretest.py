import streamlit as st
from pages.src.utils import embed_video
from PIL import Image

###################### PRETEST PAGE ######################

lang = st.session_state.get("prefered_language", "EN")

error_labels = {
    "EN": "Please answer **all** questions before continuing.",
    "FR": "Merci de répondre à **toutes** les questions avant de continuer.",
    "IT": "Per favore rispondi a **tutte** le domande prima di continuare.",
}


title_labels = {
    "EN": "Pre-test",
    "FR": "Pré-test",
    "IT": "Pre-test",
}

intro_labels = {
    "EN": "Please answer the following questions as best as you can.",
    "FR": "Merci de répondre aux questions suivantes du mieux que tu peux.",
    "IT": "Per favore rispondi alle seguenti domande al meglio delle tue possibilità.",
}

# Q1
q1_labels = {
    "EN": "1. What is a recursive algorithm?",
    "FR": "1. Qu’est-ce qu’un algorithme récursif ?",
    "IT": "1. Cos'è un algoritmo ricorsivo?",
}

q1_options = {
    "EN": [
        "A. An algorithm that solves a problem by calling itself until a simple stopping condition is reached.",
        "B. An algorithm that changes its structure during execution to adapt to the input data.",
        "C. An algorithm that processes the entire input in a single step without breaking it down.",
    ],
    "IT": [
        "A. Un algoritmo che risolve un problema richiamando se stesso fino al raggiungimento di una semplice condizione di arresto.",
        "B. Un algoritmo che modifica la sua struttura durante l'esecuzione per adattarsi ai dati di input.",
        "C. Un algoritmo che elabora l'intero input in un unico passaggio senza scomporlo.",
    ],
    "FR": [
        "A. Un algorithme qui résout un problème en s’appelant lui-même jusqu’à ce qu’une condition simple soit remplie.",
        "B. Un algorithme qui change sa structure pendant son exécution pour s’adapter à la donnée fournie.",
        "C. Un algorithme qui traite l’intégralité des données fournies en une seule étape sans les décomposer.",
    ],
}

# Q2
q2_labels = {
    "EN": "2. Recursive computation",
    "FR": "2. Calcul récursif",
    "IT": "2. Calcolo ricorsivo",
}

q2_prompt = {
    "EN": "Given the following recursive algorithm, compute and enter the value of $a_3$.\n\n"
          "$$f(x) = 2x^2, \\quad a_0 = 4, \\quad a_n = f(a_{n-1})$$",
    "FR": "Soit l’algorithme récursif suivant, calcule et entre la valeur de $a_3$.\n\n"
          "$$f(x) = 2x^2, \\quad a_0 = 4, \\quad a_n = f(a_{n-1})$$",
    "IT": "Dato il seguente algoritmo ricorsivo, calcola e inserisci il valore di $a_3$.\n\n"
          "$$f(x) = 2x^2, \\quad a_0 = 4, \\quad a_n = f(a_{n-1})$$",
}

q2_input_label = {
    "EN": "Your answer for $a_3$:",
    "FR": "Ta réponse pour $a_3$ :",
    "IT": "La tua risposta per $a_3$:",
}

# Q3
q3_labels = {
    "EN": "3. Which of the following are valid strategies for finding the minimum of a function? (You can choose multiple options)",
    "FR": "3. Laquelle (ou lesquelles) des stratégies suivantes peut (ou peuvent) permettre de trouver le minimum d’une fonction ? (Tu peux choisir plusieurs réponses)",
    "IT": "3. Quali delle seguenti sono strategie valide per trovare il minimo di una funzione? (Puoi scegliere più opzioni)",
}

q3_options = {
    "EN": [
        "A. Check where the first derivative is zero and evaluate the second derivative at that point.",
        "B. Perform a grid search by evaluating the function at regularly spaced points over a chosen interval.",
        "C. Increase the input values until the function becomes constant.",
        "D. Choose a point where the derivative is undefined and assume it is a minimum.",
    ],
    "IT": [
        "A. Verificare dove la derivata prima è zero e calcolare la derivata seconda in quel punto.",
        "B. Eseguire una ricerca su griglia valutando la funzione in punti regolarmente distanziati su un intervallo scelto.",
        "C. Aumentare i valori di input fino a quando la funzione diventa costante.",
        "D. Scegliere un punto in cui la derivata è indefinita e supporre che sia un minimo.",
    ],
    "FR": [
        "A. Vérifier où est-ce que la première dérivée est nulle et évaluer la dérivée seconde en ce ou ces point(s).",
        "B. Effectuer une recherche en grille en évaluant la fonction à des points régulièrement espacés sur un intervalle choisi.",
        "C. Augmenter les valeurs en entrée jusqu’à ce que la fonction devienne constante.",
        "D. Choisir un point où la dérivée est non-définie et assumer qu’il s’agit d’un minimum.",
    ],
}

q3_help = {
    "EN": "Select all strategies that you think could work.",
    "FR": "Sélectionne toutes les stratégies qui te semblent fonctionner.",
    "IT": "Seleziona tutte le strategie che pensi possano funzionare.",
}

# Q4
q4_labels = {
    "EN": "4. Gradient concept (open-ended)",
    "FR": "4. Concept de gradient (réponse ouverte)",
    "IT": "4. Concetto di gradiente (risposta aperta)",
}

q4_prompt = {
    "EN": "In your own words, what does the gradient of a function represent? What information does it provide?",
    "FR": "En utilisant tes propres mots, que représente le gradient d’une fonction ? Quelles informations peut-il donner ?",
    "IT": "Con parole tue, cosa rappresenta il gradiente di una funzione? Quali informazioni fornisce?",
}

# Q5
q5_labels = {
    "EN": "5. Loss function and loss curve interpretation (open-ended)",
    "FR": "5. Interprétation de la fonction de perte (loss function) et de la courbe de perte (loss curve)",
    "IT": "5. Interpretazione della funzione di perdita (loss function) e della curva di perdita (loss curve)",
}

q5_prompt = {
    "EN": (
        "A loss function measures how well an algorithm performs by quantifying the error between predictions "
        "and the desired output. A loss curve shows how this error changes over time (for example, over iterations "
        "of training or optimization).\n\n"
        "Considering the loss curve that you see, describe what the curve reveals about the algorithm’s behavior."
    ),
    "FR": (
        "Une fonction de perte mesure l'efficacité d'un algorithme en quantifiant l'erreur entre les prédictions "
        "et la sortie désirée. Une courbe de perte montre comment cette erreur varie dans le temps "
        "(par exemple, au fil des itérations d’apprentissage ou d’optimisation).\n\n"
        "En considérant la courbe de perte que tu vois, décris ce que la courbe révèle sur le comportement de l’algorithme."
    ),
    "IT": (
        "Una funzione di perdita misura l'efficacia di un algoritmo quantificando l'errore tra le previsioni "
        "e l'output desiderato. Una curva di perdita mostra come questo errore varia nel tempo "
        "(ad esempio, durante le iterazioni di addestramento o ottimizzazione).\n\n"
        "Considerando la curva di perdita che vedi, descrivi cosa rivela la curva sul comportamento dell'algoritmo."
    ),
}

submit_labels = {
    "EN": "Submit my pre-test answers",
    "FR": "Soumettre mes réponses au pré-test",
    "IT": "Invia le mie risposte al pre-test",
}

success_labels = {
    "EN": "Thank you! Your pre-test answers have been saved.",
    "FR": "Merci ! Tes réponses au pré-test ont été enregistrées.",
    "IT": "Grazie! Le tue risposte al pre-test sono state salvate.",
}

only_one_answer = {
    "EN": "Only one answer possible:",
    "FR": "Une seule réponse possible:",
    "IT": "Solo una risposta possibile:"} 

multiple_answers = {
    "EN": "One or more answers possible:",
    "FR": "Une ou plusieurs réponses possibles:",
    "IT": "Una o più risposte possibili:"} 

# Submission state
if "pretest_submitted" not in st.session_state:
    st.session_state.pretest_submitted = False

# Only display form if not yet submitted
if not st.session_state.pretest_submitted:
    with st.form("pretest_form", enter_to_submit=False):

        st.markdown(f"## {title_labels[lang]}")
        st.write(intro_labels[lang])

        # Q1
        st.markdown(f"### {q1_labels[lang]}")
        q1_answer = st.radio(
            label=only_one_answer[lang],
            options=q1_options[lang],
            index=None,
        )

        # Q2
        st.markdown(f"### {q2_labels[lang]}")
        st.markdown(q2_prompt[lang])
        q2_answer = st.text_input(q2_input_label[lang])

        # Q3
        st.markdown(f"### {q3_labels[lang]}")
        q3_answer = st.multiselect(
            label=multiple_answers[lang],
            options=q3_options[lang],
            help=q3_help[lang],
        )

        # Q4
        st.markdown(f"### {q4_labels[lang]}")
        q4_answer = st.text_area(q4_prompt[lang])

        # Q5
        st.markdown(f"### {q5_labels[lang]}")
        img = Image.open("pages/src/assets/loss_curves.png")
        st.image(img, width="stretch")
        q5_answer = st.text_area(q5_prompt[lang])

        submitted = st.form_submit_button(submit_labels[lang])

    if submitted:
        # Save everything in session_state
        st.session_state.preq1 = q1_answer
        st.session_state.preq2 = q2_answer
        st.session_state.preq3 = q3_answer
        st.session_state.preq4 = q4_answer
        st.session_state.preq5 = q5_answer
        st.session_state.pretest_submitted = True      
            

else:
    st.success(success_labels[lang])

    context_labels = {"EN":"## Let's start! With a little bit of context… 👯", 
                        "FR":"## C'est parti ! Commençons avec un peu de contexte… 👯", 
                        "IT":"## Cominciamo! Con un po' di contesto... 👯"}
    st.markdown(context_labels[st.session_state.prefered_language])
    
    if "PSI" not in st.session_state:
        st.error(f"No PSI condition has been assigned yet.")
    elif st.session_state.PSI:
        # display context video for PSI then move on to the PS activity
        links_PSI_context = {"EN":"https://youtu.be/suYJGx3ailE", 
                             "FR":"https://youtu.be/Dl2LnkoVPh4", 
                             "IT":"https://youtu.be/gB9jlNKStK8"}
        embed_video(links_PSI_context[st.session_state.prefered_language], 'pages/psactivity.py')
    else:
        # display context video for IPS then move on to the instructions
        links_IPS_context = {"EN":"https://youtu.be/fd5T80Pc4FY", 
                             "FR":"https://youtu.be/lSq03w5jUZA", 
                             "IT":"https://youtu.be/T6zZYfNv8Fs"}
        embed_video(links_IPS_context[st.session_state.prefered_language], 'pages/instructions.py')

