import streamlit as st
import streamlit.components.v1 as components

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
                         ("FR", False): "https://youtu.be/Jw-PE9NrOKI",
                         ("IT", False): "https://youtu.be/LLaubZsj0i4",
                         ("EN", True): "",
                         ("FR", True): "",
                         ("IT", True): ""}

def instructions_URL(PSI, language="EN"):
    if (language, PSI) not in language_to_video_URL:
        st.error(f"The given arguments PSI={PSI} and language={language} are not valid. Please enter the PSI condition of the user (True for PSI, False for IPS), and their prefered language among 'EN', 'IT', and 'FR'.")
        return None
    return language_to_video_URL[(language, PSI)]


def embed_video(video_id, next_page):
        
    # Initialize session state for tracking button click
    if 'video_next_clicked' not in st.session_state:
        st.session_state.video_next_clicked = False    
        
    video_html = f"""
    <div id="video-container" style="display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 100%;">
        <div style="position: relative; width: 100%; padding-bottom: 56.25%; max-width: 1200px;">
            <iframe id="video-player" 
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                    src="https://www.youtube.com/embed/{video_id}?enablejsapi=1" 
                    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
            </iframe>
        </div>
        <div id="next-button-container" style="display:none; margin-top:10px; width: 100%; max-width: 1200px; text-align: right;">
            <button onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: true}}, '*')" 
                    style="padding:10px 20px; font-size:16px; cursor:pointer;">
                Next
            </button>
        </div>
    </div>

    <script>
        var player;
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        
        window.onYouTubeIframeAPIReady = function() {{
            player = new YT.Player('video-player', {{
                events: {{
                    'onStateChange': onPlayerStateChange,
                    'onReady': function(event) {{
                        console.log('Player ready');
                    }}
                }}
            }});
        }}
        
        function onPlayerStateChange(event) {{
            console.log('Player state changed:', event.data);
            if (event.data == YT.PlayerState.ENDED) {{
                console.log('Video ended, showing button');
                document.getElementById('next-button-container').style.display = 'block';
            }}
        }}
    </script>
    """

    video_finished = components.html(video_html, height=700)

    # Check if button was clicked (only when it returns 'clicked')
    if video_finished == 'clicked':
        st.session_state.video_next_clicked = True
        st.rerun()
    
    # Navigate to next page if button was clicked
    if st.session_state.video_next_clicked:
        st.switch_page(next_page)