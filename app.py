import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder,speech_to_text

TIME = 5
state=st.session_state
word = []


if 'text_received' not in state:
    state.text_received=[]

c1,c2=st.columns(2)

with c1:
    st.write("Convert speech to text:")
with c2:
    text=speech_to_text(language='en',start_prompt="⏺️", stop_prompt="⏹️", use_container_width=True,just_once=True,key='STT')

if text:       
    state.text_received.append(text)
    st.write(state.text_received)
    

def word_to_braille(text):
    converted_phrase = []
    for word in text:
        braille_instructions = pybraille.convertText(word)
        converted_phrase.append(braille_instructions)
    return converted_phrase





if st.button("Convert to Braille"):
    braille_instructions = word_to_braille(state.text_recieved)
    print(f"Braille instructions for ''{state.text_recieved}'' are: {braille_instructions}")

    

