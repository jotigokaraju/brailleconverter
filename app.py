import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder, speech_to_text
import time
import requests
import base64

# GitHub repository details
repo_owner = "jotigokaraju"
repo_name = "brailleconverter"
file_path = "instructions.txt"

# GitHub API URL
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

# Personal access token
access_token = "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"

state = st.session_state
word = []
global braille_instructions
braille_instructions = []

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

# Title Formatting
st.title("Live Speech to Braille")
st.subheader("Joti Gokaraju")
st.divider()

# Braille conversion function
def word_to_braille(text):
    converted_phrase = []
    for words in text:
        braille_instruction = pybraille.convertText(words)
        converted_phrase.append(braille_instruction)
    return converted_phrase

# Function to convert braille_instructions to instructions list
def braille_to_instructions(braille_instruction1):
    instructions_list = []
    for word in braille_instruction1:
        if word in braille_mapping:
            instructions_list.append(braille_mapping[word])
    return instructions_list


# Check if 'text_received' is in the session state
if 'text_received' not in state:
    state.text_received = []

# Recorder and Transcriber
st.header("Speech-to-Text Converter")
st.write("Record and transcribe your speech.")

# Speech-to-text recorder
text = speech_to_text(language='en', start_prompt="Start 🔴", stop_prompt="Stop 🟥", use_container_width=True, just_once=True, key='STT')

# If text is recognized, add it to session state and display translation
if text:
    state.text_received.append(text)
    st.success("Speech recognized successfully!")
    st.write("Translated text:")
    for i, translated_text in enumerate(state.text_received):
        st.write(f"{i + 1}. {translated_text}")
        word.append(translated_text)

st.header("Select Recorded Text")
if state.text_received:
    selected_text = st.selectbox("Select recorded text:", state.text_received)

st.divider()

# Braille conversion
st.header("Braille Conversion")
st.write("Convert selected text to Braille.")

# Convert to Braille button
if st.button("Convert to Braille") and selected_text:
    braille_instructions = word_to_braille(selected_text)

    with st.spinner('Wait for it...'):
        time.sleep(1)
    st.success(f"Braille instructions for {selected_text} are: {braille_instructions}")

st.divider()

# Send to Github File
st.header("Send to Device")
st.write("Send Translation Instructions to Device")

if st.button("Send") and selected_text:
    braille_instructionstext = word_to_braille(selected_text)
    instructions_list = braille_to_instructions(braille_instructionstext)

    # Get content
    response = requests.get(api_url, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()

    # Extract content
    current_content = response_data["content"]
    current_content_decoded = current_content.encode("utf-8")
    current_content_decoded = base64.b64decode(current_content_decoded).decode("utf-8")
    
    # Update content
    new_content = f"{instructions_list}"

    # Encode new content
    new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")

    # Prepare data
    data = {
        "message": "Update instructions.txt",
        "content": new_content_encoded,
        "sha": response_data["sha"]
    }

    # Update
    update_response = requests.put(api_url, headers={"Authorization": f"Bearer {access_token}"}, json=data)

    if update_response.status_code == 200:
        st.success("Sent!")
    else:
        st.error(f"Error updating file. Status code: {update_response.status_code}")

st.divider()

# Footer
st.divider()
st.write("All Recordings are Immediately Deleted Upon Refreshing the Page to Prevent Data Leaks")
