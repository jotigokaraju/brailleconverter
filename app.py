import speech_recognition as sr
import streamlit as st
import pybraille

TIME = 5


def recognize_speech():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Say something!")
    try:
        audio = r.listen(source, timeout=TIME)
        print("Recording completed.")
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.WaitTimeoutError:
        print("Speech recognition timed out. No speech detected in 5 seconds.")
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


if st.button("Speak"):
  text = recognize_speech()
  print("We translated:", text)
  
if st.button("Convert to Braille"):
    text = text.strip()
    braille_instructions = word_to_braille(text)
    print(f"Braille instructions for ''{word}'' are: {braille_instructions}")
    

