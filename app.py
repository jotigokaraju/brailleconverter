import streamlit as st

def english():
    import streamlit as st
    import pybraille
    from streamlit_mic_recorder import mic_recorder, speech_to_text
    import time
    import requests
    import base64
    from gtts import gTTS
    from transformers import pipeline
    from PIL import Image
    import easyocr
    from io import BytesIO
    import os

    # Load the pipeline outside Streamlit script
    caption = None
    sentiment = None
    OCR = None
    
    @st.cache_resource
    def load_model():
        return pipeline(model="ydshieh/vit-gpt2-coco-en")
    
    @st.cache_resource
    def sentiment_model():
        return pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    
    @st.cache_resource
    def ocr_model():
        return easyocr.Reader(['en'])


    
    #Repo Details
    repo_owner = "jotigokaraju"
    repo_name = "brailleconverter"
    file_path_instructions = "instructions.txt"
    file_path_reciever = "recieve.txt"
    
    # GitHub API URL
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_instructions}"
    api_url_commands = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_reciever}"
    
    # Access the secret as an environment variable in streamlit
    access_token = st.secrets["ACCESS_TOKEN"]
    
    state = st.session_state
    
    if 'text_received' not in state:
        state.text_received = []
    
    if 'img_received' not in state:
        state.img_received = []
    
    if 'ocr_received' not in state:
        state.ocr_received = []

    if 'handocr_reveived' not in state:
        state.handocr_received = []
        
    
    state.selected_text = None

    converting_text = None
    
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
        '⠂': [1, 4],  # Braille Comma
        '⠆': [7, 4],  # Braille Semicolon
        '⠒': [1, 1],  # Braille Colon
        '⠲': [1, 2],  # Braille Full Stop
        '⠌': [5, 5],  # Braille Slash
        '⠤': [5, 6],  # Braille Dash
    }
    
    
    def check_for_items():
        sound_file = BytesIO()
        tts = gTTS("Hello!", lang='en')
        tts.write_to_fp(sound_file)
        st.success("Hello")
        st.audio(sound_file)
    

        
    # Braille conversion function
    english_braille_list = {
        'a': '⠁',    # Braille Letter A
        'b': '⠃',    # Braille Letter B
        'c': '⠉',    # Braille Letter C
        'd': '⠙',    # Braille Letter D
        'e': '⠑',    # Braille Letter E
        'f': '⠋',    # Braille Letter F
        'g': '⠛',    # Braille Letter G
        'h': '⠓',    # Braille Letter H
        'i': '⠊',    # Braille Letter I
        'j': '⠚',    # Braille Letter J
        'k': '⠅',    # Braille Letter K
        'l': '⠇',    # Braille Letter L
        'm': '⠍',    # Braille Letter M
        'n': '⠝',    # Braille Letter N
        'o': '⠕',    # Braille Letter O
        'p': '⠏',    # Braille Letter P
        'q': '⠟',    # Braille Letter Q
        'r': '⠗',    # Braille Letter R
        's': '⠎',    # Braille Letter S
        't': '⠞',    # Braille Letter T
        'u': '⠥',    # Braille Letter U
        'v': '⠧',    # Braille Letter V
        'w': '⠺',    # Braille Letter W
        'x': '⠭',    # Braille Letter X
        'y': '⠽',    # Braille Letter Y
        'z': '⠵',    # Braille Letter Z
        '1': '⠼⠁',  # Braille Number 1
        '2': '⠼⠃',  # Braille Number 2
        '3': '⠼⠉',  # Braille Number 3
        '4': '⠼⠙',  # Braille Number 4
        '5': '⠼⠑',  # Braille Number 5
        '6': '⠼⠋',  # Braille Number 6
        '7': '⠼⠛',  # Braille Number 7
        '8': '⠼⠓',  # Braille Number 8
        '9': '⠼⠊',  # Braille Number 9
        '0': '⠼⠚',  # Braille Number 0
        ',': '⠂',    # Braille Comma
        ';': '⠆',    # Braille Semicolon
        ':': '⠒',    # Braille Colon
        '.': '⠲',    # Braille Full Stop
        '/': '⠌',  # Braille Slash
        '!': '⠮',    # Braille Exclamation Mark
        '?': '⠦',    # Braille Question Mark
        "'": '⠄',    # Braille Apostrophe
        '"': '⠐⠄',  # Braille Quotation Mark
        '-': '⠤',    # Braille Dash
        '(': '⠐⠣',  # Braille Opening Parenthesis
        ')': '⠐⠜',  # Braille Closing Parenthesis
        ' ': ' ',    # Space
    }
    
    def word_to_braille(text):
        text = str(text)
        converted_phrase = []
        for char in text:
            if char.lower() in english_braille_list:
                braille_text = english_braille_list[char.lower()]
                converted_phrase.append(braille_text)
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
    st.header("A Comprehensive Speech to Braille Platform for the Deafblind")
    st.divider()
       
    with st.expander("***About***"):
        st.markdown("""
            This app is designed to assist the DeafBlind community, a traditionally underserved demographic. 
            The app translates live speech into Braille instructions that are read out by the TouchTalk device.
            
            **Goals:**
            - Provide a low-cost novel method for traditional communication used by the DeafBlind.
            - Make everyday communication easier, less invasive, and universal.
            - Eliminate cost and knowledge barriers associated with current methods. 
    
            This innovative approach aims to empower the Deafblind community, offering a more accessible and inclusive means of communication.
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
    selected_text = None
    tab1, tab2, tab3 = st.tabs(["AI Speech Transcription", "AI Image Captioning", "Optical Character Recognition"])
    
    with tab1: 
        
        state.selected_text = None
        if sentiment is None:
            classifier = sentiment_model()
        
       # Recorder and Transcriber
        st.header("Speech-to-Text Converter")
        st.write("Record and transcribe your speech.")
        
        # Speech-to-text recorder
        text = speech_to_text(language='en', start_prompt="Start 🔴", stop_prompt="Stop 🟥", use_container_width=True, just_once=True, key='STT')
        
        # Always render the speech_to_text component
        if text is not None:
            state.text_received.append(text)

        # Display success message if text is recognized
        if text:
            st.success("Speech recognized successfully!")
            
        # Display recognition status and translated text
        st.write("Translated text:")
        for index, translated_text in enumerate(state.text_received):
            st.write(f"{index + 1}. {translated_text}")
            word.append(translated_text)

        if state.text_received:
            st.header("Select Text")
            stext = st.selectbox("Select recorded text:", state.text_received)
            
        if st.button("Sentiment Analysis", type="primary"):
            sentences = []
            sentences.append(stext)
            model_outputs = classifier(sentences)
            max_score_label = max(model_outputs[0], key=lambda x: x['score'])
            label = max_score_label['label']
            label_cap = label[0].upper() + label[1:]
            
            state.converting_text = f"{stext} /{label[:2]}"

            st.success(f"Detected Sentiment: {label_cap}")
            st.success(f"Transcribed word: {state.converting_text}")

        # Braille conversion
        st.header("Braille Conversion")
        st.write("Convert selected text to Braille.")
        
        if st.button("Convert to Braille "):
            state.braille_instructions = word_to_braille(state.converting_text)     
            st.success(f"Braille instructions for {state.converting_text} are: {state.braille_instructions}")
    
        st.divider()
        
        # Send to Github File
        st.header("Send to Device")
        st.write("Send Translation Instructions to Device")
        
        if st.button("Send ", type="primary"):
            instructions_list = braille_to_instructions(state.braille_instructions)
        
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
                
    with tab2:
        state.selected_text = None
        caption_of_image = None
        
        if caption is None:
            caption = load_model()
            
        st.header("Image Captioning")
        st.write("Take an Image to Return an AI Generated Caption")
        
        photo = st.camera_input("Capture a Photo")
        
        if photo is not None:
            image = Image.open(photo)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("Generate Caption") and image is not None:
                captions = caption(image) 
                caption_of_image = str(captions[0]['generated_text'])
                st.success(caption_of_image)
    
        if caption_of_image is not None:
            state.img_received.append(caption_of_image)
    
        st.write("Caption text:")
        for index, caption_text in enumerate(state.img_received):
            st.write(f"{index + 1}. {caption_text}")
        
        if state.img_received:
            st.header("Select Caption")
            selected_text = st.selectbox("Select Caption:", state.img_received)
            state.selected_text = f"{selected_text} /c"
            
            
        st.divider()

        # Braille conversion
        st.header("Braille Conversion")
        st.write("Convert selected text to Braille.")
                
        # Convert to Braille button
        
        if st.button("Convert to Braille  ") and state.selected_text:
            with st.spinner('Processing...'):
                selected_text = state.selected_text
                braille_instructions = word_to_braille(selected_text)
                time.sleep(0.5)
                
            st.success(f"Braille instructions for {selected_text} are: {braille_instructions}")
    
        st.divider()
        
        # Send to Github File
        st.header("Send to Device  ")
        st.write("Send Translation Instructions to Device")
        
        if st.button("Send", type="primary") and state.selected_text is not None:
            selected_text = state.selected_text
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
    
    with tab3:
        state.selected_text = None
        done = None
        
        if OCR is None:
            reader = ocr_model()
    
        st.header("OCR")
        st.write("Extract Text from Image")
        
        ocr_photo = st.camera_input("Take a Photo")
        
        if ocr_photo is not None:
            imager = Image.open(ocr_photo)
            st.image(imager, caption="Uploaded Image", use_column_width=True)
            
            if st.button("Extract Text") and imager is not None:
        
                extract_info = reader.readtext(imager)
                extracted_text = ' '.join([text for _, text, _ in extract_info])
                st.success(extracted_text)
                done = extracted_text
    
        if done is not None:
            state.ocr_received.append(done)
    
        st.write("Extracted Text:")
        for index, text in enumerate(state.ocr_received):
            st.write(f"{index + 1}. {text}")
        
        if state.ocr_received:
            st.header("Select OCR Text")
            selected_text = st.selectbox("Select Text:", state.ocr_received)
            state.selected_text = f"{selected_text} /o"       
        
        # Braille conversion
        st.header("Braille Conversion")
        st.write("Convert selected text to Braille.")
                
        # Convert to Braille button
        
        if st.button("Convert to Braille    ") and state.selected_text:
            with st.spinner('Processing...'):
                selected_text = state.selected_text
                braille_instructions = word_to_braille(selected_text)
                time.sleep(0.5)
                
            st.success(f"Braille instructions for {selected_text} are: {braille_instructions}")
    
        st.divider()
        
        # Send to Github File
        st.header("Send to Device")
        st.write("Send Translation Instructions to Device")
        
        if st.button("Send    ", type="primary") and state.selected_text is not None:
            selected_text = state.selected_text
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
    
    
            
        

    st.header("Recieve from Device")
    st.write("Any Translations Sent from the Device to the App will be Displayed Here")
    
    if st.button("Check", type="primary"):
        check_for_items()
    
    
    # Footer
    st.divider()
    st.write("All Recordings are Immediately Deleted Upon Refreshing the Page to Prevent Data Leaks")




























def french():
    
    import streamlit as st
    import pybraille
    from streamlit_mic_recorder import mic_recorder, speech_to_text
    import time
    import requests
    import base64
    from gtts import gTTS
    from transformers import pipeline
    from PIL import Image
    import easyocr
    from io import BytesIO
    import os
    
    # Load the pipeline outside Streamlit script
    caption = None
    OCR = None

    @st.cache_resource
    def translate_fr():
        return pipeline(task="translation", model="google-t5/t5-small")
        
    @st.cache_resource
    def load_modelfr():
        return pipeline('image-to-text')

    @st.cache_resource
    def ocr_modelfr():
        return easyocr.Reader(['fr'])
        
    #Repo Details
    repo_owner = "jotigokaraju"
    repo_name = "brailleconverter"
    file_path_instructions = "instructions.txt"
    file_path_reciever = "recieve.txt"
    
    # GitHub API URL
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_instructions}"
    api_url_commands = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_reciever}"
    
    # Access the secret as an environment variable in streamlit
    access_token = st.secrets["ACCESS_TOKEN"]
    
    
    state = st.session_state
    
    if 'text_received' not in state:
        state.text_received = []
    
    if 'img_received' not in state:
        state.img_received = []
    
    if 'ocr_received' not in state:
        state.ocr_received = []
        
    if 'selected_text' not in state:
        state.selected_text = None
    
    word = []
    global braille_instructions
    braille_instructions = []
    
    braille_mapping = {
        '⠁': [6, 4],  # Braille Letter A
        '⠷': [0, 2],  # Braille Letter À
        '⠡': [6, 6],  # Braille Letter Â
        '⠃': [2, 4],  # Braille Letter B
        '⠉': [6, 5],  # Braille Letter C
        '⠙': [6, 7],  # Braille Letter D
        '⠑': [6, 1],  # Braille Letter E
        '⠿': [0, 0],  # Braille Letter É
        '⠮': [7, 3],  # Braille Letter È
        '⠣': [2, 6],  # Braille Letter Ê
        '⠫': [2, 3],  # Braille Letter Ë
        '⠋': [2, 5],  # Braille Letter F
        '⠛': [2, 7],  # Braille Letter G
        '⠓': [2, 1],  # Braille Letter H
        '⠊': [1, 5],  # Braille Letter I
        '⠩': [6, 3],  # Braille Letter Î
        '⠻': [2, 0],  # Braille Letter Ï
        '⠚': [1, 7],  # Braille Letter J
        '⠅': [3, 4],  # Braille Letter K
        '⠇': [0, 4],  # Braille Letter L
        '⠍': [3, 5],  # Braille Letter M
        '⠝': [3, 7],  # Braille Letter N
        '⠕': [3, 1],  # Braille Letter O
        '⠹': [6, 0],  # Braille Letter Ô
        '⠏': [0, 5],  # Braille Letter P
        '⠟': [0, 7],  # Braille Letter Q
        '⠗': [0, 1],  # Braille Letter R
        '⠎': [7, 5],  # Braille Letter S
        '⠞': [7, 7],  # Braille Letter T
        '⠥': [3, 6],  # Braille Letter U
        '⠧': [0, 6],  # Braille Letter Ù
        '⠺': [1, 0],  # Braille Letter Û
        '⠭': [3, 3],  # Braille Letter Ü
        '⠽': [3, 0],  # Braille Letter V
        '⠵': [3, 2],  # Braille Letter W
        '⠭': [3, 3],  # Braille Letter X
        '⠽': [3, 0],  # Braille Letter Y
        '⠵': [3, 2],  # Braille Letter Z
        '⠪': [1, 3],  # Braille Letter Œ
        '⠂': [1, 4],  # Braille Comma
        '⠆': [7, 4],  # Braille Semicolon
        '⠒': [1, 1],  # Braille Colon
        '⠲': [1, 2],  # Braille Full Stop
        '⠌': [5, 5],  # Braille Slash
        '⠤': [5, 6],  # Braille Dash
    }




    conversion_list = {
        'a': '⠁',    # Braille Letter A
        'à': '⠷',    # Braille Letter À
        'â': '⠡',    # Braille Letter Â
        'b': '⠃',    # Braille Letter B
        'c': '⠉',    # Braille Letter C
        'd': '⠙',    # Braille Letter D
        'e': '⠑',    # Braille Letter E
        'é': '⠿',    # Braille Letter É
        'è': '⠮',    # Braille Letter È
        'ê': '⠣',    # Braille Letter Ê
        'ë': '⠫',    # Braille Letter Ë
        'f': '⠋',    # Braille Letter F
        'g': '⠛',    # Braille Letter G
        'h': '⠓',    # Braille Letter H
        'i': '⠊',    # Braille Letter I
        'î': '⠩',    # Braille Letter Î
        'ï': '⠻',    # Braille Letter Ï
        'j': '⠚',    # Braille Letter J
        'k': '⠅',    # Braille Letter K
        'l': '⠇',    # Braille Letter L
        'm': '⠍',    # Braille Letter M
        'n': '⠝',    # Braille Letter N
        'o': '⠕',    # Braille Letter O
        'ô': '⠹',    # Braille Letter Ô
        'p': '⠏',    # Braille Letter P
        'q': '⠟',    # Braille Letter Q
        'r': '⠗',    # Braille Letter R
        's': '⠎',    # Braille Letter S
        't': '⠞',    # Braille Letter T
        'u': '⠥',    # Braille Letter U
        'ù': '⠾',    # Braille Letter Ù
        'û': '⠱',    # Braille Letter Û
        'ü': '⠳',    # Braille Letter Ü
        'v': '⠧',    # Braille Letter V
        'w': '⠺',    # Braille Letter W
        'x': '⠭',    # Braille Letter X
        'y': '⠽',    # Braille Letter Y
        'z': '⠵',    # Braille Letter Z
        'œ': '⠪',    # Braille Letter Œ
        ',': '⠂',    # Braille Comma
        ';': '⠆',    # Braille Semicolon
        ':': '⠒',    # Braille Colon
        '.': '⠲',    # Braille Full Stop
        '(...) ': '⠦…⠴',    # Braille Ellipsis
        '/': '⠌',    # Braille Slash
        '–': '⠤',    # Braille Dash
        '%': '⠐⠬',    # Braille Percent
        '‰': '⠐⠬⠬',    # Braille Per Mille
        '1': '⠠⠡',    # Braille Number 1
        '2': '⠠⠣',    # Braille Number 2
        '3': '⠠⠩',    # Braille Number 3
        '4': '⠠⠹',    # Braille Number 4
        '5': '⠠⠱',    # Braille Number 5
        '6': '⠠⠫',    # Braille Number 6
        '7': '⠠⠻',    # Braille Number 7
        '8': '⠠⠳',    # Braille Number 8
        '9': '⠠⠪',    # Braille Number 9
        '0': '⠠⠼',    # Braille Number 0
        ' ': ' ', #Space
    }

    def wordbraille(text):
        braille_text = ""
        for char in text:
            if char.lower() in conversion_list:
                braille_text += conversion_list[char.lower()]
        return braille_text
    

    
    def check_for_items():
        # Get content
        response = requests.get(api_url_commands, headers={"Authorization": f"Bearer {access_token}"})
        response_data = response.json()
    
        # Extract content
        current_content = response_data["content"]
        current_content_decoded = current_content.encode("utf-8")
        current_content_decoded = base64.b64decode(current_content_decoded).decode("utf-8")
        current_content_decoded = current_content_decoded.strip()
        
        if current_content_decoded != "Nothing to see here for now!":
            
            if current_content_decoded[-2:] == ' f':
                current_content_decoded = current_content_decoded[:-1]
            else:
                current_content_decoded = current_content_decoded
                
            sound_file = BytesIO() 
            tts = gTTS(current_content_decoded, lang='fr')
            tts.write_to_fp(sound_file)
            st.audio(sound_file)
            st.success(current_content_decoded)
            
        else:
            st.success("Rien à voir ici pour le moment!")
    
        
        
        
        
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
        
    
    # Function to convert braille_instructions to instructions list
    def braille_to_instructions(commands):
        instructions_list = []
        for word in commands:
            if word in braille_mapping:
                instructions_list.append(braille_mapping[word])
        return instructions_list
    
    
    st.title("ToucherParler")
    st.header("Une plateforme complète de communication vocale en braille pour les sourds-aveugles")
    st.divider()
    
    with st.expander("***À propos***"):
        st.markdown("""
            Cette application est conçue pour aider la communauté sourde-aveugle, une population traditionnellement mal desservie.
            L'application traduit la parole en direct en instructions en braille qui sont lues par l'appareil ToucherParler.
            
            **Objectifs :**
            - Fournir une méthode novatrice à faible coût pour la communication traditionnelle utilisée par les sourds-aveugles.
            - Faciliter la communication quotidienne, moins invasive et universelle.
            - Éliminer les barrières de coût et de connaissance associées aux méthodes actuelles. 
    
            Cette approche innovante vise à autonomiser la communauté sourde-aveugle, en offrant un moyen de communication plus accessible et inclusif.
            Fabriqué par Joti Gokaraju
        """)

    with st.expander("***Instructions***"):
        st.markdown("""
            Veuillez consulter les instructions suivantes avant d'essayer d'utiliser l'application. 
            
            **Envoi d'informations à l'appareil.**
    
            1. Appuyez sur Démarrer et commencez à vous enregistrer. Lorsque vous avez terminé, appuyez sur Arrêter. L'application retournera automatiquement une transcription de votre discours 
            2. Sélectionnez le bouton Convertir en braille pour traduire votre discours en lettres braille
            3. Sélectionnez le bouton Envoyer à l'appareil pour que l'application transforme les lettres en instructions et que l'appareil les exécute
        
            **Réception d'informations de l'appareil.**
    
            1. Faites défiler jusqu'au bas de la page
            2. Cliquez sur le bouton Vérifier pour voir s'il y a du texte
            3. S'il y a du texte, il sera affiché dans un cadre vert. S'il n'y a pas de texte, ou aucun nouveau texte, un message d'erreur sera affiché
            4. Répétez le processus si vous êtes sûr que du texte a été envoyé depuis l'appareil
            
        """)


    st.divider()
    
    st.header("Sélectionnez le type de communication")
    st.write("De la parole au braille ou de l'image au braille")

    selected_text = None
    tab1, tab2, tab3 = st.tabs(["Transcription automatique de la parole par IA", "Légende d'image générée par IA", "Reconnaissance optique de caractères"])
    
    with tab1: 

        # Enregistreur et transcripteur
        st.header("Convertisseur de parole en texte")
        st.write("Enregistrez et transcrivez votre discours.")
        
        # Enregistreur de parole en texte
        text = speech_to_text(language='fr', start_prompt="Commencer 🔴", stop_prompt="Arrêter 🟥", use_container_width=True, just_once=True, key='STT')
        
        # Toujours afficher le composant speech_to_text
        if text is not None:
            state.text_received.append(text)
        
        # Afficher l'état de la reconnaissance et le texte traduit
        st.write("Texte traduit:")
        for index, translated_text in enumerate(state.text_received):
            st.write(f"{index + 1}. {translated_text}")
            word.append(translated_text)
        
        # Afficher un message de succès si le texte est reconnu
        if text:
            st.success("Discours reconnu avec succès!")
        
        if state.text_received:
            st.header("Sélectionnez le texte")
            stext = st.selectbox("Sélectionnez le texte enregistré :", state.text_received)
            state.selected_text = stext
            
        st.divider()

        if st.button("Convertir en Braille") and state.selected_text:
            with st.spinner('Traitement...'):
                selected_text = state.selected_text
                words = selected_text  # Split the selected text into words

                braille_instructions = wordbraille(words)  # Pass the list of words to the conversion function
                time.sleep(0.5)
                    
                st.success(f"Les instructions en Braille pour {selected_text} sont : {braille_instructions}")
            
        st.divider()
            
        # Envoyer au fichier Github
        st.header("Envoyer à l'appareil")
        st.write("Envoyer les instructions de traduction à l'appareil")
        
        if st.button("Envoyer", type="primary") and state.selected_text is not None:
            selected_text = state.selected_text
            send_braille_commands = wordbraille(selected_text)

            instructions_list = braille_to_instructions(send_braille_commands)

        
            # Obtenir le contenu
            response = requests.get(api_url, headers={"Authorization": f"Bearer {access_token}"})
            response_data = response.json()
        
            # Extraire le contenu
            current_content = response_data["content"]
            current_content_decoded = current_content.encode("utf-8")
            current_content_decoded = base64.b64decode(current_content_decoded).decode("utf-8")
            
            # Mettre à jour le contenu
            new_content = f"{instructions_list}"
        
            # Encoder le nouveau contenu
            new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
        
            # Préparer les données
            data = {
                "message": "Update instructions.txt",
                "content": new_content_encoded,
                "sha": response_data["sha"]
            }
        
            # Mettre à jour
            update_response = requests.put(api_url, headers={"Authorization": f"Bearer {access_token}"}, json=data)
        
            if update_response.status_code == 200:
                st.success("Envoyé!")
            else:
                st.error(f"Erreur lors de la mise à jour du fichier. Code d'état : {update_response.status_code}")
            
        # Conversion Braill
    
    
    with tab2:
    
        caption_of_image = None
        capin = None
        translating = None
        captionimg = None
        caption = None
        
        if caption is None:
            caption = load_modelfr()
            translator = translate_fr()
            
        st.header("Légende d'image")
        st.write("Prenez une image pour retourner une légende générée par IA")
        
        photo = st.camera_input("Prendre une photo")
        
        if photo is not None:
            image = Image.open(photo)
            st.image(image, caption="Image téléchargée", use_column_width=True)
            
            if st.button("Générer une légende") and image is not None:
                captions = caption(image) 
                captionimg = str(captions[0]['generated_text'])
                capin = f"translate English to French: {captionimg}"
                translating = translator(capin)
                caption_of_image = str(translating[0]['translation_text'])
                st.success(caption_of_image)
    
        if caption_of_image is not None:
            state.img_received.append(caption_of_image)
    
        st.write("Texte de la légende :")
        for index, caption_text in enumerate(state.img_received):
            st.write(f"{index + 1}. {caption_text}")
        
        if state.img_received:
            st.header("Sélectionnez la légende")
            selected_text = st.selectbox("Sélectionnez la légende :", state.img_received)
            state.selected_text = f"{selected_text} /cap"
            
            
        st.divider()

        if st.button("Convertir en Braille  ") and state.selected_text:
            with st.spinner('Traitement...'):
                selected_text = state.selected_text
                words = selected_text  # Split the selected text into words

                braille_instructions = wordbraille(words)  # Pass the list of words to the conversion function
                time.sleep(0.5)
                    
                st.success(f"Les instructions en Braille pour {selected_text} sont : {braille_instructions}")
            
        st.divider()
        
        # Envoyer au fichier Github
        st.header("Envoyer à l'appareil")
        st.write("Envoyer les instructions de traduction à l'appareil")
        
        if st.button("Envoyer  ", type="primary") and state.selected_text is not None:
            selected_text = state.selected_text
            send_braille_commands = wordbraille(selected_text)

            instructions_list = braille_to_instructions(send_braille_commands)
        
            # Obtenir le contenu
            response = requests.get(api_url, headers={"Authorization": f"Bearer {access_token}"})
            response_data = response.json()
        
            # Extraire le contenu
            current_content = response_data["content"]
            current_content_decoded = current_content.encode("utf-8")
            current_content_decoded = base64.b64decode(current_content_decoded).decode("utf-8")
            
            # Mettre à jour le contenu
            new_content = f"{instructions_list}"
        
            # Encoder le nouveau contenu
            new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
        
            # Préparer les données
            data = {
                "message": "Update instructions.txt",
                "content": new_content_encoded,
                "sha": response_data["sha"]
            }
        
            # Mettre à jour
            update_response = requests.put(api_url, headers={"Authorization": f"Bearer {access_token}"}, json=data)
        
            if update_response.status_code == 200:
                st.success("Envoyé!")
            else:
                st.error(f"Erreur lors de la mise à jour du fichier. Code d'état : {update_response.status_code}")
            
        # Conversion Braill
    
    with tab3:
        
        done = None
        
        if OCR is None:
            reader = ocr_modelfr()
    
        st.header("Reconnaissance optique de caractères")
        st.write("Extraire du texte à partir d'une image")
        
        ocr_photo = st.camera_input("Prendre une Photo")
        
        if ocr_photo is not None:
            imager = Image.open(ocr_photo)
            st.image(imager, caption="Image téléchargée", use_column_width=True)
            
            if st.button("Extraire le texte") and imager is not None:
        
                extract_info = reader.readtext(imager)
                extracted_text = ' '.join([text for _, text, _ in extract_info])
                st.success(extracted_text)
                done = extracted_text
    
        if done is not None:
            state.ocr_received.append(done)
    
        st.write("Texte extrait :")
        for index, text in enumerate(state.ocr_received):
            st.write(f"{index + 1}. {text}")
        
        if state.ocr_received:
            st.header("Sélectionnez le texte OCR")
            selected_text = st.selectbox("Sélectionnez le texte :", state.ocr_received)
            state.selected_text = f"{selected_text} /ocr"
            # Bouton Convertir en Braille
    
        if st.button("Convertir en Braille    ") and state.selected_text:
            
            with st.spinner('Traitement...'):
                selected_text = state.selected_text
                words = selected_text  # Split the selected text into words

                braille_instructions = wordbraille(words)  # Pass the list of words to the conversion function
                time.sleep(0.5)
                
            st.success(f"Les instructions en Braille pour {selected_text} sont : {braille_instructions}")
        
        st.divider()
        
        # Envoyer au fichier Github
        st.header("Envoyer à l'appareil")
        st.write("Envoyer les instructions de traduction à l'appareil")
        
        if st.button("Envoyer    ", type="primary") and state.selected_text is not None:
            selected_text = state.selected_text
            send_braille_commands = wordbraille(selected_text)

            instructions_list = braille_to_instructions(send_braille_commands)
        
            # Obtenir le contenu
            response = requests.get(api_url, headers={"Authorization": f"Bearer {access_token}"})
            response_data = response.json()
        
            # Extraire le contenu
            current_content = response_data["content"]
            current_content_decoded = current_content.encode("utf-8")
            current_content_decoded = base64.b64decode(current_content_decoded).decode("utf-8")
            
            # Mettre à jour le contenu
            new_content = f"{instructions_list}"
        
            # Encoder le nouveau contenu
            new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
        
            # Préparer les données
            data = {
                "message": "Update instructions.txt",
                "content": new_content_encoded,
                "sha": response_data["sha"]
            }
        
            # Mettre à jour
            update_response = requests.put(api_url, headers={"Authorization": f"Bearer {access_token}"}, json=data)
        
            if update_response.status_code == 200:
                st.success("Envoyé!")
            else:
                st.error(f"Erreur lors de la mise à jour du fichier. Code d'état : {update_response.status_code}")
            
        # Conversion Braill
    
        

    

    st.header("Recevoir de l'appareil")
    st.write("Toutes les traductions envoyées de l'appareil à l'application seront affichées ici")
    
    if st.button("Examiner", type="primary"):
        check_for_items()
    
    
    # Pied de page
    st.divider()
    st.write("Toutes les enregistrements sont immédiatement supprimés dès le rafraîchissement de la page pour éviter les fuites de données")
    





page_names_to_funcs = {
    "English": english,
    "Français": french
}

demo_name = st.sidebar.selectbox("Select Language \n Choisir la langue", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
