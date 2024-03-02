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

braille_mapping_swapped = {
    '⠁': [4, 5],  # Braille Letter A
    '⠃': [4, 7],  # Braille Letter B
    '⠉': [3, 5],  # Braille Letter C
    '⠙': [1, 5],  # Braille Letter D
    '⠑': [7, 5],  # Braille Letter E
    '⠋': [3, 7],  # Braille Letter F
    '⠛': [1, 7],  # Braille Letter G
    '⠓': [7, 7],  # Braille Letter H
    '⠊': [3, 1],  # Braille Letter I
    '⠚': [1, 1],  # Braille Letter J
    '⠅': [4, 3],  # Braille Letter K
    '⠇': [4, 0],  # Braille Letter L
    '⠍': [3, 3],  # Braille Letter M
    '⠝': [1, 3],  # Braille Letter N
    '⠕': [7, 3],  # Braille Letter O
    '⠏': [3, 0],  # Braille Letter P
    '⠟': [1, 0],  # Braille Letter Q
    '⠗': [7, 0],  # Braille Letter R
    '⠎': [3, 2],  # Braille Letter S
    '⠞': [1, 2],  # Braille Letter T
    '⠥': [2, 3],  # Braille Letter U
    '⠧': [2, 0],  # Braille Letter V
    '⠺': [0, 1],  # Braille Letter W
    '⠭': [5, 3],  # Braille Letter X
    '⠽': [0, 3],  # Braille Letter Y
    '⠵': [6, 3],  # Braille Letter Z
}


def check_for_items():
    # Get content
    response = requests.get(api_url_commands, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()

    # Extract content
    current_content = response_data["content"]
    current_content_decoded = current_content.encode("utf-8")
    current_content_decoded = base64.b64decode(current_content_decoded).decode("utf-8")


    st.success(current_content_decoded)
    
    # Update content
    new_content = "Nothing to see here for now!"
    
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
st.header("A Comprehensive Speech to Braille Platform for the DeafBlind")
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
    
with st.expander("***Instructions***"):
    st.markdown("""
        Please view the following instructions before you attempt to use the app. 
        
        **Sending information to the device.**

        1. Press Start and Begin Recording Yourself. When You Finish, Press Stop. The App Will Automatically Return a Transcription of Your Speech 
        2. Select the Convert to Braille Button to Translate Your Speech into Braille Letters
        3. Select the Send to Device Button to Have the App Turn the Letters into Instructions and Have the Device Execute

        **Receiving information from the device.**

        1. Scroll to the Bottom of the Page
        2. Click on the Check Button to See If There Is Any Text
        3. If There is Any Text, It Will be Displayed in a Greenbox. If There is No Text, or No New Text, it Will Display An Error Message
        4. Repeat the Process If You Are Confident That Text Has Been Sent from the Device
        
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

if st.button("Send", type="primary") and selected_text:
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

if st.button("Check", type="primary"):
    check_for_items()

# Footer
st.divider()
st.write("All Recordings are Immediately Deleted Upon Refreshing the Page to Prevent Data Leaks")
