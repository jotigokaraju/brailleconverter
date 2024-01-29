import streamlit as st
import time
import requests
import base64

# GitHub repository details
repo_owner = "jotigokaraju"
repo_name = "brailleconverter"
file_path = "instructions.txt"

# GitHub API URL
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

# HIDE
access_token = "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"

st.title("MineBot")
st.header("A Mini-Robot System to Tackle Clumping in Potash Storage Bins")
st.divider()

st.header("Number of Rotations")
move_count = st.slider('Choose How Many Times You Want the Motor To Hit', 0, 100, 5)
st.write("Move the motor", move_count, 'times')

st.divider()

lister = [[0, 0]]

for _ in range(move_count):
    lister.extend([[7, 7], [0, 0]])

st.header("Activate!")
st.write("Send Precise Instructions to Device")

if st.button("Send"):
    instructions_list = lister

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

# Footer
st.divider()
st.write("Joti Gokaraju, Abhinav Menon, Arbe Chumala")
