import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder,speech_to_text

TIME = 5
state=st.session_state

def recognize_speech():
  
    c1,c2=st.columns(2)
    with c1:
        st.write("Convert speech to text:")
    with c2:
        text=speech_to_text(language='en',use_container_width=True,just_once=True,key='STT')
        st.write(text)   
        state.recognized_text = text


def word_to_braille(text):
    converted_phrase = []
    for word in text:
        braille_instructions = pybraille.convertText(word)
        converted_phrase.append(braille_instructions)
    return converted_phrase


if st.button("Speak"):
  text = recognize_speech()
  print(state.recognized_text)
  print("We translated:", text)
  
if st.button("Convert to Braille"):
    text = text.strip()
    braille_instructions = word_to_braille(text)
    print(f"Braille instructions for ''{word}'' are: {braille_instructions}")
