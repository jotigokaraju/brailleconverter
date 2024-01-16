# TouchTalk Live Speech to Braille Converter

## Used Libraries
Google Speech-to-Text API
PyBraille Text-to-Braille Converter
Streamlit-Speech-Recognition

## App Process
1. Use Streamlit-Speech-Recognition to capture audio as a streamlit state
2. Use Google Speech-to-Text API to Convert .wav audio recording into text and return the text
3. Functionality for user to decide if the text is accurate or if they want to rerecord and then select the most accurate transcription
4. Run the text through PyBraille to return a series of braille for each character in the text
5. Let the user press a button to send the braille to the device to display
6. Convert the braille into a series of instructions in a list with the numbers 0 to 7 representing a different configuration on each column.
7. Write the list instructions to a private Github txt file
