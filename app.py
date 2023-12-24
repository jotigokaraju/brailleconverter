import streamlit as st
import pybraille
from st_audiorec import st_audiorec

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')
  
'''
def word_to_braille(text):
    converted_phrase = []
    for word in text:
        braille_instructions = pybraille.convertText(word)
        converted_phrase.append(braille_instructions)
    return converted_phrase


if st.button("Speak"):
  text = recognize_speech()
  print("We translated:", text)
  
if st.button("Convert to Braille"):
    text = text.strip()
    braille_instructions = word_to_braille(text)
    print(f"Braille instructions for ''{word}'' are: {braille_instructions}")
    
'''
    
