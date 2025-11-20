import streamlit as st

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

# Submission state
if "pretest_submitted" not in st.session_state:
    st.session_state.pretest_submitted = False

st.markdown(f"## {title_labels[lang]}")
st.write(intro_labels[lang])

# Only display form if not yet submitted
if not st.session_state.pretest_submitted:
    with st.form("pretest_form"):

        # Q1
        st.markdown(f"### {q1_labels[lang]}")
        q1_answer = st.radio(
            label="",
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
            label="",
            options=q3_options[lang],
            help=q3_help[lang],
        )

        # Q4
        st.markdown(f"### {q4_labels[lang]}")
        q4_answer = st.text_area(q4_prompt[lang])

        # Q5
        st.markdown(f"### {q5_labels[lang]}")
        q5_answer = st.text_area(q5_prompt[lang])

        submitted = st.form_submit_button(submit_labels[lang])

    if submitted:
        
        # Validate: all must be non-empty
        missing = (
            q1_answer is None
            or q1_answer == ""
            or not q2_answer.strip()
            or len(q3_answer) == 0
            or not q4_answer.strip()
            or not q5_answer.strip()
        )

        if missing:
            st.error(error_labels[lang])
        else:
            # Save everything in session_state
            st.session_state.pretest_answers = {
                "recursive_algorithm_mc": q1_answer,
                "recursive_computation_a3": q2_answer,
                "minimum_strategies": q3_answer,
                "gradient_concept": q4_answer,
                "loss_curve_interpretation": q5_answer,
            }
            st.session_state.pretest_submitted = True
            st.success(success_labels[lang])
            
            if "PSI" in st.session_state:
                if st.session_state.PSI:
                    st.switch_page("pages/psactivity.py")
                else:
                    st.switch_page("pages/instructions.py")
            
            

else:
    st.success(success_labels[lang])
