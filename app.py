import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder, speech_to_text

# Set up Streamlit session state
TIME = 5
state = st.session_state
word = []

#Title Formatting
st.title("Live Speech to Braille Translator")
st.subheader("Joti Gokaraju")
st.divider()

# Braille conversion function
def word_to_braille(text):
    converted_phrase = []
    for word in text:
        braille_instructions = pybraille.convertText(word)
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
            time.sleep(3)
        st.success(f"Braille instructions for {word} are: {braille_instructions}")


st.markdown("---")  
st.write("All Recordings are Immediately Deleted Upon Refreshing the Page to Prevent Data Leaks")
