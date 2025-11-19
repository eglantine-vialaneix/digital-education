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

# fallback to EN if not set
lang = st.session_state.get("prefered_language", "EN")

###################### TEXT LABELS ########################

title_labels = {
    "EN": "Post-test",
    "FR": "Post-test",
    "IT": "Post-test",
}

intro_labels = {
    "EN": "Please answer the following questions based on what you learned in the activity.",
    "FR": "Merci de répondre aux questions suivantes en te basant sur ce que tu as appris durant l’activité.",
    "IT": "Per favore rispondi alle seguenti domande in base a ciò che hai imparato durante l’attività.",
}

map_label = {
    "EN": "1. Mapping real-world metaphor → algorithmic components",
    "FR": "1. Mise en correspondance métaphore du monde réel → composantes de l’algorithme",
    "IT": "1. Mappatura della metafora del mondo reale → componenti algoritmici",
}

map_prompt = {
    "EN": (
        "Thinking back to the introductory context video, match each element of the real-world metaphor "
        "to the corresponding part of the gradient descent algorithm.\n\n"
        "**Left elements**:\n"
        "- A) Mountains\n"
        "- B) Point where you were on the mountain\n"
        "- C) Step size\n"
        "- D) Valley\n"
        "- E) Different possible path\n\n"
        "**Right elements**:\n"
        "- 1) Function f()\n"
        "- 2) $a_0$\n"
        "- 3) $\\eta$ (eta)\n"
        "- 4) Minimum\n"
        "- 5) Different possible choice of parameters\n\n"
        "Write your answers in the following form, for example: `(A,1), (B,2), (C,3)`."
    ),
    "FR": (
        "En repensant à la vidéo de contexte, associe chaque élément de la métaphore du monde réel "
        "à la partie correspondante de l’algorithme de descente de gradient.\n\n"
        "**Éléments de gauche** :\n"
        "- A) Montagnes\n"
        "- B) Point où tu te trouvais sur la montagne\n"
        "- C) Taille du pas\n"
        "- D) Vallée\n"
        "- E) Différents chemins possibles\n\n"
        "**Éléments de droite** :\n"
        "- 1) Fonction f()\n"
        "- 2) $a_0$\n"
        "- 3) $\\eta$ (eta)\n"
        "- 4) Minimum\n"
        "- 5) Différents choix possibles de paramètres\n\n"
        "Écris tes réponses dans la forme suivante, par exemple : `(A,1), (B,2), (C,3)`."
    ),
    "IT": (
        "Ripensando al video introduttivo, abbina ogni elemento della metafora del mondo reale "
        "alla parte corrispondente dell’algoritmo di discesa del gradiente.\n\n"
        "**Elementi di sinistra**:\n"
        "- A) Montagna\n"
        "- B) Punto in cui ti trovavi sulla montagna\n"
        "- C) Dimensione del passo\n"
        "- D) Valle\n"
        "- E) Diversi percorsi possibili\n\n"
        "**Elementi di destra**:\n"
        "- 1) Funzione f()\n"
        "- 2) $a_0$\n"
        "- 3) $\\eta$ (eta)\n"
        "- 4) Minimo\n"
        "- 5) Diversa scelta possibile dei parametri\n\n"
        "Scrivi le tue risposte nella seguente forma, ad esempio: `(A,1), (B,2), (C,3)`."
    ),
}

map_input_label = {
    "EN": "Your mapping:",
    "FR": "Tes associations :",
    "IT": "Le tue associazioni:",
}

neg_grad_label = {
    "EN": "2. Reason for moving in the negative gradient direction",
    "FR": "2. Raison de se déplacer dans la direction opposée au gradient",
    "IT": "2. Motivo per cui ci muoviamo nella direzione negativa del gradiente",
}

neg_grad_prompt = {
    "EN": "In your own words, why do we move in the **negative** direction of the gradient during gradient descent?",
    "FR": "Avec tes propres mots, pourquoi se déplace-t-on dans la **direction opposée** au gradient lors de la descente de gradient ?",
    "IT": "Con parole tue, perché nel Gradient Descent ci muoviamo nella **direzione negativa** del gradiente?",
}

conv_label = {
    "EN": "3. Convergence of Gradient Descent",
    "FR": "3. Convergence de la descente de gradient",
    "IT": "3. Convergenza della discesa del gradiente",
}

conv_question = {
    "EN": "Does gradient descent always converge to a minimum?",
    "FR": "La descente de gradient converge-t-elle toujours vers un minimum ?",
    "IT": "La discesa del gradiente converge sempre a un minimo?",
}

conv_options = {
    "EN": [
        "A. Yes, gradient descent always converges to a global minimum for any function and any step size.",
        "B. No, gradient descent may fail to converge if the function is not convex or if the step size is not appropriate.",
        "C. Yes, gradient descent always converges as long as the gradient exists.",
        "D. No, gradient descent never converges unless the function is quadratic.",
    ],
    "FR": [
        "A. Oui, la descente de gradient converge toujours vers un minimum global pour toute fonction et toute taille de pas.",
        "B. Non, la descente de gradient peut ne pas converger si la fonction n’est pas convexe ou si la taille du pas n’est pas appropriée.",
        "C. Oui, la descente de gradient converge toujours tant que le gradient existe.",
        "D. Non, la descente de gradient ne converge jamais à moins que la fonction ne soit quadratique.",
    ],
    "IT": [
        "A. Sì, la discesa del gradiente converge sempre a un minimo globale per qualsiasi funzione e qualsiasi dimensione del passo.",
        "B. No, la discesa del gradiente potrebbe non convergere se la funzione non è convessa o se la dimensione del passo non è appropriata.",
        "C. Sì, la discesa del gradiente converge sempre finché esiste il gradiente.",
        "D. No, la discesa del gradiente non converge mai a meno che la funzione non sia quadratica.",
    ],
}

zero_label = {
    "EN": "4. Interpretation of zero gradient",
    "FR": "4. Interprétation d’un gradient nul",
    "IT": "4. Interpretazione del gradiente zero",
}

zero_question = {
    "EN": "Suppose the gradient of a convex function is zero at a certain point during the algorithm execution. What does this imply?",
    "FR": "Supposons que le gradient d’une fonction convexe soit nul en un certain point pendant l’exécution de l’algorithme. Qu’est-ce que cela implique ?",
    "IT": "Supponiamo che il gradiente di una funzione convessa sia zero in un certo punto durante l'esecuzione dell'algoritmo. Cosa implica questo?",
}

zero_options = {
    "EN": [
        "A. The point is a global maximum of the function.",
        "B. The algorithm has diverged.",
        "C. The point is a global or local minimum of the function.",
        "D. The function is non-differentiable at that point.",
    ],
    "FR": [
        "A. Le point est un maximum global de la fonction.",
        "B. L’algorithme a divergé.",
        "C. Le point est un minimum global ou local de la fonction.",
        "D. La fonction n’est pas différentiable en ce point.",
    ],
    "IT": [
        "A. Il punto è un massimo globale della funzione.",
        "B. L'algoritmo ha divergenza.",
        "C. Il punto è un minimo globale o locale della funzione.",
        "D. La funzione non è differenziabile in quel punto.",
    ],
}

# Loss function and loss curve interpretation (open)
loss_label = {
    "EN": "5. Loss function and loss curve interpretation",
    "FR": "5. Interprétation de la fonction de perte et de la courbe de perte",
    "IT": "5. Interpretazione della funzione di perdita e della curva di perdita",
}

loss_prompt = {
    "EN": (
        "Considering the loss curve(s) you saw (for example, one that overshoots with a learning rate $\\eta$ too large, "
        "or one that starts very high because $a_0$ is far and decreases very slowly because $\\eta$ is too small), "
        "describe what the curve reveals about the algorithm’s behavior."
    ),
    "FR": (
        "En te basant sur la ou les courbes de perte que tu as vues (par exemple, une courbe qui dépasse le minimum "
        "avec un $\\eta$ trop grand, ou une courbe qui part très haut car $a_0$ est loin et diminue très lentement "
        "car $\\eta$ est trop petit), décris ce que cette courbe révèle du comportement de l’algorithme."
    ),
    "IT": (
        "Considerando la curva (o le curve) di perdita che hai visto (ad esempio, una che supera il minimo perché $\\eta$ è troppo grande, "
        "oppure una che parte molto alta perché $a_0$ è lontano e diminuisce molto lentamente perché $\\eta$ è troppo piccolo), "
        "descrivi cosa rivela la curva sul comportamento dell'algoritmo."
    ),
}

multi_intro = {
    "EN": (
        "In the following questions, you will select **one or more** correct answers.\n"
        "Unlike typical multiple-choice questions, there may be multiple correct options, "
        "and not all options carry the same meaning. Read carefully and select **all** the answers that you think are correct."
    ),
    "FR": (
        "Dans les questions suivantes, tu devras sélectionner **une ou plusieurs** réponses correctes.\n"
        "Contrairement aux QCM classiques, il peut y avoir plusieurs réponses correctes, "
        "et toutes n’ont pas exactement la même signification. Lis attentivement et sélectionne **toutes** les réponses que tu juges correctes."
    ),
    "IT": (
        "Nelle seguenti domande, dovrai selezionare **una o più** risposte corrette.\n"
        "A differenza delle tipiche domande a risposta multipla, potrebbero esserci più opzioni corrette "
        "e non tutte hanno lo stesso significato. Leggi attentamente e seleziona tutte le risposte che ritieni corrette."
    ),
}

a0_label = {
    "EN": "6. In gradient descent, what does the parameter $a_0$ (initial value / starting point) influence?",
    "FR": "6. En descente de gradient, qu’est-ce que le paramètre $a_0$ (valeur initiale / point de départ) influence ?",
    "IT": "6. Nel Gradient Descent, cosa influenza il parametro $a_0$ (valore iniziale / punto di partenza)?",
}

a0_options = {
    "EN": [
        "A. It may determine whether the algorithm converges to a global minimum or becomes trapped in a local minimum (for non-convex loss surfaces).",
        "B. It affects the number of iterations required to reach convergence, even if the final solution is the same.",
        "C. It can lead the algorithm to converge to a saddle point instead of a minimum.",
        "D. It influences the value of the gradient evaluated at the first iteration and therefore affects all subsequent updates.",
    ],
    "FR": [
        "A. Il peut déterminer si l’algorithme converge vers un minimum global ou reste bloqué dans un minimum local (pour des surfaces de perte non convexes).",
        "B. Il influence le nombre d’itérations nécessaires pour atteindre la convergence, même si la solution finale est la même.",
        "C. Il peut amener l’algorithme à converger vers un point selle plutôt qu’un minimum.",
        "D. Il influence la valeur du gradient évalué à la première itération et affecte donc toutes les mises à jour suivantes.",
    ],
    "IT": [
        "A. Può determinare se l'algoritmo converge a un minimo globale o rimane intrappolato in un minimo locale (per funzioni non convesse).",
        "B. Influisce sul numero di iterazioni necessarie per raggiungere la convergenza, anche se la soluzione finale è la stessa.",
        "C. Può portare l'algoritmo a convergere a un punto di sella anziché a un minimo.",
        "D. Influenza il valore del gradiente valutato alla prima iterazione e quindi influenza tutti gli aggiornamenti successivi.",
    ],
}

eta_label = {
    "EN": "7. In gradient descent, what does the parameter $\\eta$ (learning rate / step size) control?",
    "FR": "7. En descente de gradient, que contrôle le paramètre $\\eta$ (taux d’apprentissage / taille du pas) ?",
    "IT": "7. Nel Gradient Descent, cosa controlla il parametro $\\eta$ (velocità di apprendimento / dimensione del passo)?",
}

eta_options = {
    "EN": [
        "A. A large $\\eta$ can cause oscillations or divergence instead of convergence.",
        "B. A small $\\eta$ increases the number of iterations needed to converge.",
        "C. Different values of $\\eta$ can cause different convergence trajectories on the same loss function.",
        "D. $\\eta$ determines the direction in which the parameter moves at each iteration.",
    ],
    "FR": [
        "A. Un $\\eta$ élevé peut provoquer des oscillations ou une divergence au lieu d’une convergence.",
        "B. Un petit $\\eta$ augmente le nombre d’itérations nécessaires pour converger.",
        "C. Des valeurs différentes de $\\eta$ peuvent entraîner des trajectoires de convergence différentes sur la même fonction de perte.",
        "D. $\\eta$ détermine la direction dans laquelle le paramètre se déplace à chaque itération.",
    ],
    "IT": [
        "A. Un $\\eta$ elevato può causare oscillazioni o divergenza anziché convergenza.",
        "B. Un piccolo $\\eta$ aumenta il numero di iterazioni necessarie per convergere.",
        "C. Valori diversi di $\\eta$ possono causare traiettorie di convergenza diverse sulla stessa funzione di perdita.",
        "D. $\\eta$ determina la direzione in cui si muove il parametro a ogni iterazione.",
    ],
}

submit_labels = {
    "EN": "Submit my post-test answers",
    "FR": "Soumettre mes réponses au post-test",
    "IT": "Invia le mie risposte al post-test",
}

success_labels = {
    "EN": "Thank you! Your post-test answers have been saved.",
    "FR": "Merci ! Tes réponses au post-test ont été enregistrées.",
    "IT": "Grazie! Le tue risposte al post-test sono state salvate.",
}

congrats_text = {
    "EN": "Congratulations! You arrived home and your oven is safely off. Most importantly, you learnt (we hope!) about Gradient Descent and helped us run our experiment – thank you so much! 💙",
    "FR": "Félicitations ! Tu es bien rentré·e chez toi et ton four est éteint en toute sécurité. Surtout, tu as (on l’espère !) appris des choses sur la descente de gradient et tu nous as aidé·es à mener notre expérience – merci beaucoup ! 💙",
    "IT": "Congratulazioni! Sei arrivato/a a casa e il tuo forno è spento in sicurezza. Soprattutto, hai (speriamo!) imparato qualcosa sulla discesa del gradiente e ci hai aiutato a svolgere il nostro esperimento – grazie mille! 💙",
}

###################### FORM LOGIC #########################

if "posttest_submitted" not in st.session_state:
    st.session_state.posttest_submitted = False

st.markdown(f"## {title_labels[lang]}")
st.write(intro_labels[lang])

if not st.session_state.posttest_submitted:
    with st.form("posttest_form"):

        # Q1
        st.markdown(f"### {map_label[lang]}")
        st.markdown(map_prompt[lang])
        map_answer = st.text_input(map_input_label[lang])

        # Q2
        st.markdown(f"### {neg_grad_label[lang]}")
        neg_grad_answer = st.text_area(neg_grad_prompt[lang])

        # Q3
        st.markdown(f"### {conv_label[lang]}")
        st.write(conv_question[lang])
        conv_answer = st.radio(
            label="",
            options=conv_options[lang],
            index=None,
        )

        # Q4
        st.markdown(f"### {zero_label[lang]}")
        st.write(zero_question[lang])
        zero_answer = st.radio(
            label="",
            options=zero_options[lang],
            index=None,
        )

        # Q5
        st.markdown(f"### {loss_label[lang]}")
        loss_answer = st.text_area(loss_prompt[lang])

        st.markdown("---")
        st.markdown(multi_intro[lang])

        # Q6
        st.markdown(f"### {a0_label[lang]}")
        a0_answer = st.multiselect(
            label="",
            options=a0_options[lang],
        )

        # Q7
        st.markdown(f"### {eta_label[lang]}")
        eta_answer = st.multiselect(
            label="",
            options=eta_options[lang],
        )

        submitted = st.form_submit_button(submit_labels[lang])

    if submitted:
        st.session_state.posttest_answers = {
            "mapping_metaphor": map_answer,
            "negative_gradient_reason": neg_grad_answer,
            "convergence_mcq": conv_answer,
            "zero_gradient_mcq": zero_answer,
            "loss_curve_interpretation": loss_answer,
            "a0_influence": a0_answer,
            "eta_control": eta_answer,
        }
        st.session_state.posttest_submitted = True
        st.success(success_labels[lang])
        st.markdown(congrats_text[lang])
else:
    st.success(success_labels[lang])
    st.markdown(congrats_text[lang])

##############

if st.button("FIN"):
    supabase = init_supabase()
    save_user_data_to_supabase(supabase)