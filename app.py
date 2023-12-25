import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder, speech_to_text
import time

state = st.session_state
word = []
braille_mapping = {
    '⠁': [1, 0, 0, 0, 0, 0],  # Braille Letter A
    '⠃': [1, 1, 0, 0, 0, 0],  # Braille Letter B
    '⠉': [1, 0, 0, 1, 0, 0],  # Braille Letter C
    '⠙': [1, 0, 0, 1, 1, 0],  # Braille Letter D
    '⠑': [1, 0, 0, 0, 1, 0],  # Braille Letter E
    '⠋': [1, 1, 0, 1, 0, 0],  # Braille Letter F
    '⠛': [1, 1, 0, 1, 1, 0],  # Braille Letter G
    '⠓': [1, 1, 0, 0, 1, 0],  # Braille Letter H
    '⠊': [0, 1, 0, 1, 0, 0],  # Braille Letter I
    '⠚': [0, 1, 0, 1, 1, 0],  # Braille Letter J
    '⠅': [1, 0, 1, 0, 0, 0],  # Braille Letter K
    '⠇': [1, 1, 1, 0, 0, 0],  # Braille Letter L
    '⠍': [1, 0, 1, 1, 0, 0],  # Braille Letter M
    '⠝': [1, 0, 1, 1, 1, 0],  # Braille Letter N
    '⠕': [1, 0, 1, 0, 1, 0],  # Braille Letter O
    '⠏': [1, 1, 1, 1, 0, 0],  # Braille Letter P
    '⠟': [1, 1, 1, 1, 1, 0],  # Braille Letter Q
    '⠗': [1, 1, 1, 0, 1, 0],  # Braille Letter R
    '⠎': [0, 1, 1, 1, 0, 0],  # Braille Letter S
    '⠞': [0, 1, 1, 1, 1, 0],  # Braille Letter T
    '⠥': [1, 0, 1, 0, 0, 1],  # Braille Letter U
    '⠧': [1, 1, 1, 0, 0, 1],  # Braille Letter V
    '⠺': [0, 1, 0, 1, 1, 1],  # Braille Letter W
    '⠭': [1, 0, 1, 1, 0, 1],  # Braille Letter X
    '⠽': [1, 0, 1, 1, 1, 1],  # Braille Letter Y
    '⠵': [1, 0, 1, 0, 1, 1],  # Braille Letter Z
}

#Title Formatting
st.title("Live Speech to Braille Translator")
st.subheader("Joti Gokaraju")
st.divider()

# Braille conversion function
def word_to_braille(text):
    converted_phrase = []
    for words in text:
        braille_instructions = pybraille.convertText(words)
        converted_phrase.append(braille_instructions)
    return converted_phrase

# Check if 'text_received' is in the session state
if 'text_received' not in state:
    state.text_received = []

# Create columns for layout
c1, c2 = st.columns(2)

# Column 1: Display recorder and translation
with c1:
    st.header("Speech-to-Text Converter")
    st.write("Record and transcribe your speech.")
    
    # Speech-to-text recorder
    text = speech_to_text(language='en', start_prompt="⏺️", stop_prompt="⏹️", use_container_width=True, just_once=True, key='STT')

    # If text is recognized, add it to session state and display translation
    if text:
        state.text_received.append(text)
        st.success("Speech recognized successfully!")
        st.write("Translated text:")
    for translated_text in state.text_received:
        st.write(translated_text)
        word.append(translated_text)

# Column 2: Braille conversion
with c2:
    st.header("Braille Conversion")
    st.write("Convert translated text to Braille.")

    # Convert to Braille button
    if st.button("Convert to Braille"):
        braille_instructions = word_to_braille(word)
        with st.spinner('Wait for it...'):
            time.sleep(2)
        st.success(f"Braille instructions for {word} are: {braille_instructions}")


st.markdown("---")  
st.write("All Recordings are Immediately Deleted Upon Refreshing the Page to Prevent Data Leaks")
