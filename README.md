# digital-education
A digital learning tool to teach Gradient Descent. 

See web deployment at [Cauchy in Matterhorn](https://cauchy-in-matterhorn.streamlit.app/)



LEFT TODO:


- retrieve user data (from screening questionnaire, pretest, posttest and meta info like number of trials and time on task)(Eglantine)
  - create google docs file OR st form
  - test data retrieval into google sheets

- ~~Embed the video instructions before the simulations and all (Eglantine):n~~
  - ~~in instructions: conditional instructions video (IPS vs PSI AND language)~~
- ITA: https://youtu.be/LLaubZsj0i4
- ENG: https://youtu.be/jC6q_nrbnh0
- FR: https://youtu.be/Jw-PE9NrOKI
  - in home: conditional context video (PSI vs IPS) + language
  - do french PS-I video
  - put all the correct video links for PS-I instruction video

- ~~fix the new navigation sustem between pages~~
  - ~~conditional navigation based on PSIvsIPS~~

- refine PS activity
  - remove all (plotting and other) functions from psactivity.py file -> into utils
  - give hints of python functions for the 
  - force minimum number of characters for interpretation 
  - ideally make the labels disappear with the dots when going back in iterations
  - make labels clearer (in bold and bigger font)
  - make the computation of the gradient as a new parameter
    - only one exercice: have to write the function G + input a0 + input eta
  - make better global instructions: your goal is NOT to find the globa minimum only, it is to discover HOW you can always (of most of the time) find it. Your goal is to find the RULE behind finding the minimum.
  - ~~repair plotting with number of iterations~~
  - ~~merge with Thomaz version~~

- ~~Pop up that forces prediction before simulation and/or **interpretation** after (Eglantine)~~

- ~~Try a preliminary exercice about the algorithm itself, before the simulation part (Thomaz)~~

- ~~FIX THOMAZ-BRANCH MERGE~~
  - ~~add hard exo from digital-education/app.py into pages/psactivity.py~~
  -~~delete digital-education nested folde~~