import speech_recognition as sr
import streamlit as st
import pybraille

TIME = 5

def recognize_speech_from_file(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        print("Processing audio file...")
        try:
            audio = r.record(source)
            print("Audio file processed.")
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        else:
            return r.recognize_google(audio)

def word_to_braille(text):
    converted_phrase = []
    for word in text:
        braille_instructions = pybraille.convertText(word)
        converted_phrase.append(braille_instructions)
    return converted_phrase

if st.button("Recognize from Audio File"):
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])
    if uploaded_file is not None:
        with open("temp_audio_file.wav", "wb") as f:
            f.write(uploaded_file.getvalue())
        text = recognize_speech_from_file("temp_audio_file.wav")
        print("We translated:", text)

if st.button("Convert to Braille"):
    text = text.strip()
    braille_instructions = word_to_braille(text)
    print(f"Braille instructions for ''{text}'' are: {braille_instructions}")
