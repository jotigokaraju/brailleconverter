import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder, speech_to_text

# Set up Streamlit session state
TIME = 5
state = st.session_state
word = []

# Check if 'text_received' is in the session state
if 'text_received' not in state:
    state.text_received = []

# Create columns for layout
c1, c2 = st.columns(2)

# Column 1: Display recorder and translation
with c1:
    st.title("Speech-to-Braille Converter")
    st.write("Record your speech and convert it to Braille!")

    # Speech-to-text recorder
    text = speech_to_text(language='en', start_prompt="⏺️", stop_prompt="⏹️", use_container_width=True, just_once=True, key='STT')

    # If text is recognized, add it to session state and display translation
    if text:
        state.text_received.append(text)
        st.success("Speech recognized successfully!")
        st.write("Translated text:")
        for translated_text in state.text_received:
            st.write(translated_text)

# Column 2: Braille conversion
with c2:
    st.title("Braille Conversion")
    st.write("Convert translated text to Braille.")

    # Convert to Braille button
    if st.button("Convert to Braille"):
        # Braille conversion function
        def word_to_braille(text):
            converted_phrase = []
            for word in text:
                braille_instructions = pybraille.convertText(word)
                converted_phrase.append(braille_instructions)
            return converted_phrase

        # Display Braille instructions
        if state.text_received:
            braille_instructions = word_to_braille(state.text_received)
            st.write(f"Braille instructions for {state.text_received} are: {braille_instructions}")

# Additional formatting
st.markdown("---")  # Horizontal divider
st.write("Your custom content or additional information can go here.")
