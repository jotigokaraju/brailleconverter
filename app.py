import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder, speech_to_text
import time
import requests
import base64

#Repo Details
repo_owner = "jotigokaraju"
repo_name = "brailleconverter"
file_path_instructions = "instructions.txt"
file_path_reciever = "recieve.txt"

# GitHub API URL
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_instructions}"
api_url_commands = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_reciever}"

#HIDE
access_token = "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"


state = st.session_state
word = []
global braille_instructions
braille_instructions = []

braille_mapping = {
    '⠁': [1, 0],  # Braille Letter A
    '⠃': [2, 0],  # Braille Letter B
    '⠉': [1, 1],  # Braille Letter C
    '⠙': [1, 2],  # Braille Letter D
    '⠑': [1, 7],  # Braille Letter E
    '⠋': [2, 1],  # Braille Letter F
    '⠛': [2, 2],  # Braille Letter G
    '⠓': [2, 7],  # Braille Letter H
    '⠊': [7, 1],  # Braille Letter I
    '⠚': [7, 2],  # Braille Letter J
    '⠅': [5, 0],  # Braille Letter K
    '⠇': [3, 0],  # Braille Letter L
    '⠍': [5, 1],  # Braille Letter M
    '⠝': [5, 2],  # Braille Letter N
    '⠕': [5, 7],  # Braille Letter O
    '⠏': [3, 1],  # Braille Letter P
    '⠟': [3, 2],  # Braille Letter Q
    '⠗': [3, 7],  # Braille Letter R
    '⠎': [4, 1],  # Braille Letter S
    '⠞': [4, 2],  # Braille Letter T
    '⠥': [5, 6],  # Braille Letter U
    '⠧': [3, 6],  # Braille Letter V
    '⠺': [7, 3],  # Braille Letter W
    '⠭': [5, 5],  # Braille Letter X
    '⠽': [5, 3],  # Braille Letter Y
    '⠵': [5, 4],  # Braille Letter Z
}

def check_for_items():
    # Get content
    response = requests.get(api_url_commands, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()

    # Extract content
    current_content = response_data["content"]
    current_content_decoded = current_content.encode("utf-8")
    current_content_decoded = base64.b64decode(current_content_decoded).decode("utf-8")

    if current_content_decoded != "[]":
        st.success(current_content_decoded)
    
        # Update content
        new_content = "[]"
    
        # Encode new content
        new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    
        # Prepare data
        data = {
            "message": "Update instructions.txt with instructions",
            "content": new_content_encoded,
            "sha": response_data["sha"]
        }
    
        # Update
        update_response = requests.put(api_url_commands, headers={"Authorization": f"Bearer {access_token}"}, json=data)
    else:
        st.success("Nothing to see here for now")

# Braille conversion function
def word_to_braille(text):
    converted_phrase = []
    for words in text:
        braille_instruction = pybraille.convertText(words)
        converted_phrase.append(braille_instruction)
    return converted_phrase

# Function to convert braille_instructions to instructions list
def braille_to_instructions(commands):
    instructions_list = []
    for word in commands:
        if word in braille_mapping:
            instructions_list.append(braille_mapping[word])
    return instructions_list
        

# Title Formatting with banner blue background
st.title("TouchTalk")
st.header("A Comprehensive Speech to Braille Platform")
st.divider()
with st.expander("***About***"):
    st.markdown("""
        This app is designed to assist the DeafBlind community, a traditionally underserved demographic. 
        The app translates live speech into Braille instructions that are read out by the TouchTalk device.
        
        **Goals:**
        - Provide a low-cost novel method for traditional communication used by the DeafBlind.
        - Make everyday communication easier, less invasive, and universal.
        - Eliminate cost and knowledge barriers associated with current methods. 

        This innovative approach aims to empower the DeafBlind community, offering a more accessible and inclusive means of communication.
        Made by Joti Gokaraju
    """)

st.divider()

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
    for index, translated_text in enumerate(state.text_received):
        st.write(f"{index + 1}. {translated_text}")
        word.append(translated_text)


if state.text_received:
    st.header("Select Recorded Text")
    selected_text = st.selectbox("Select recorded text:", state.text_received)

st.divider()

# Braille conversion
st.header("Braille Conversion")
st.write("Convert selected text to Braille.")

# Convert to Braille button
if st.button("Convert to Braille") and selected_text:
    with st.spinner('Processing...'):
        braille_instructions = word_to_braille(selected_text)
        time.sleep(1)
    st.success(f"Braille instructions for {selected_text} are: {braille_instructions}")

st.divider()

# Send to Github File
st.header("Send to Device")
st.write("Send Translation Instructions to Device")

if st.button("Send") and selected_text:
    send_braille_commands = word_to_braille(selected_text)
    instructions_list = braille_to_instructions(send_braille_commands)

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
        "message": "Update instructions.txt with instructions",
        "content": new_content_encoded,
        "sha": response_data["sha"]
    }

    # Update
    update_response = requests.put(api_url, headers={"Authorization": f"Bearer {access_token}"}, json=data)

    if update_response.status_code == 200:
        st.success("Sent!")
    else:
        st.error(f"Error updating file. Status code: {update_response.status_code}")


#Divider
st.divider()
st.header("Recieve from Device")
st.write("Any Translations Sent from the Device to the App will be Displayed Here")

if st.button("Check"):
    check_for_items()

# Footer
st.divider()
st.write("All Recordings are Immediately Deleted Upon Refreshing the Page to Prevent Data Leaks")
