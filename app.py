import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder, speech_to_text

TIME = 5
state = st.session_state
word = []

def callback():
    if st.session_state.STT_output:
        st.write(st.session_state.STT_output)

def recognize(state):
    if 'text_received' not in state:
        state.text_received = []

    c1, c2 = st.columns(2)

    with c1:
        st.write("Convert speech to text:")
    with c2:
        text = speech_to_text(language='en', start_prompt="⏺️", stop_prompt="⏹️", use_container_width=True, just_once=True,key='STT',callback=callback)

    if text:
        state.text_received.append(text)
    return state.text_received

def word_to_braille(text):
    converted_phrase = []
    for word in text.split():
        braille_instructions = pybraille.convertText(word)
        converted_phrase.append(braille_instructions)
    return converted_phrase

if st.button("Speak"):
    returned_text = recognize(state)
    callback()
    st.write("We think you said: ")
    for text in state.text_received:
        st.write(text)
        word.append(text)

if st.button("Convert to Braille"):
    braille_text = ' '.join(word)
    braille_instructions = word_to_braille(braille_text)
    st.write(f"Braille instructions for ''{braille_text}'' are: {braille_instructions}")
