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

move_count = st.slider('How old are you?', 0, 100, 5)
st.write("Move the robot", move_count, 'times')

list = []

for _ in range(move_count):
  list.append([7, 7], [0, 0])

st.header("Send to Device")
st.write("Send Instructions to Device")

if st.button("Send"):
    instructions_list = list

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
st.write("All Recordings are Immediately Deleted Upon Refreshing the Page to Prevent Data Leaks")
