import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder,speech_to_text

TIME = 5
state=st.session_state
word = []

       
def recognize(state):
    if 'text_received' not in state:
        state.text_received=[]

    c1,c2=st.columns(2)

    with c1:
        st.write("Convert speech to text:")
    with c2:
        text=speech_to_text(language='en',start_prompt="⏺️", stop_prompt="⏹️", use_container_width=True,just_once=True,key='STT')

    if text:       
        state.text_received.append(text)
        st.write(state.text_recieved)
        return state.text_recieved

def word_to_braille(text):
    converted_phrase = []
    for word in text:
        braille_instructions = pybraille.convertText(word)
        converted_phrase.append(braille_instructions)
    return converted_phrase



if st.button("Speak"):
    returnedtext = recognize(state)
    st.write("We think you said: ")
    word = st.session_state.STT_output
    print(word)

if st.button("Convert to Braille"):
    brailletext = word
    braille_instructions = word_to_braille(brailletext)
    print(f"Braille instructions for ''{word}'' are: {braille_instructions}")

    

