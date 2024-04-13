import streamlit as st
import pybraille
from streamlit_mic_recorder import mic_recorder, speech_to_text
import time
import requests
import base64
from gtts import gTTS
from transformers import pipeline
from PIL import Image

# Load the pipeline outside Streamlit script
caption = None

@st.cache_resource
def load_model():
    return pipeline('image-to-text', model="ydshieh/vit-gpt2-coco-en")



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
if 'text_received' not in state:
    state.text_received = []

word = []
global braille_instructions
braille_instructions = []

braille_mapping = {
    '⠁': [6, 4],  # Braille Letter A
    '⠃': [2, 4],  # Braille Letter B
    '⠉': [6, 5],  # Braille Letter C
    '⠙': [6, 7],  # Braille Letter D
    '⠑': [6, 1],  # Braille Letter E
    '⠋': [2, 5],  # Braille Letter F
    '⠛': [2, 7],  # Braille Letter G
    '⠓': [2, 1],  # Braille Letter H
    '⠊': [1, 5],  # Braille Letter I
    '⠚': [1, 7],  # Braille Letter J
    '⠅': [3, 4],  # Braille Letter K
    '⠇': [0, 4],  # Braille Letter L
    '⠍': [3, 5],  # Braille Letter M
    '⠝': [3, 7],  # Braille Letter N
    '⠕': [3, 1],  # Braille Letter O
    '⠏': [0, 5],  # Braille Letter P
    '⠟': [0, 7],  # Braille Letter Q
    '⠗': [0, 1],  # Braille Letter R
    '⠎': [7, 5],  # Braille Letter S
    '⠞': [7, 7],  # Braille Letter T
    '⠥': [3, 6],  # Braille Letter U
    '⠧': [0, 6],  # Braille Letter V
    '⠺': [1, 0],  # Braille Letter W
    '⠭': [3, 3],  # Braille Letter X
    '⠽': [3, 0],  # Braille Letter Y
    '⠵': [3, 2],  # Braille Letter Z
}


def check_for_items():
    # Get content
    response = requests.get(api_url_commands, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()

    # Extract content
    current_content = response_data["content"]
    current_content_decoded = current_content.encode("utf-8")
    current_content_decoded = base64.b64decode(current_content_decoded).decode("utf-8")

    if current_content_decoded != "Nothing to see here for now!":
        sound_file = BytesIO()
        tts = gTTS(current_content_decoded, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file)

    
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

    return current_content_decoded
    

    
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

st.header("Select Type of Communication")
st.write("Speech-to-Braille or Image-to-Braille")
selected_text = None
tab1, tab2 = st.tabs(["AI Speech Transcription", "AI Image Captioning"])

with tab1:
   # Recorder and Transcriber
    st.header("Speech-to-Text Converter")
    st.write("Record and transcribe your speech.")
    
    # Speech-to-text recorder
    text = speech_to_text(language='en', start_prompt="Start 🔴", stop_prompt="Stop 🟥", use_container_width=True, just_once=True, key='STT')
    
    # Always render the speech_to_text component
    if text is not None:
        state.text_received.append(text)
    
    # Display recognition status and translated text
    st.write("Translated text:")
    for index, translated_text in enumerate(state.text_received):
        st.write(f"{index + 1}. {translated_text}")
        word.append(translated_text)
    
    # Display success message if text is recognized
    if text:
        st.success("Speech recognized successfully!")
    
    
    if state.text_received:
        st.header("Select Recorded Text")
        selected_text = st.selectbox("Select recorded text:", state.text_received)

    st.divider()

with tab2:
    if caption is None:
        caption = load_model()
    # Recorder and Transcriber
    st.header("Image Captioning")
    st.write("Take an Image to Create an AI Generated Caption")
    
    photo = st.camera_input("Take a Photo")
    if photo is not None:
        image = Image.open(photo)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Generate Caption") and image is not None:
            captions = caption(image)
            selected_text = str(captions[0]['generated_text'])
            st.write(captions[0]['generated_text'])
    
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

if st.button("Send", type="primary") and selected_text is not None:
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
