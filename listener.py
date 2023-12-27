import requests
import base64
import json
import time
import RPi.GPIO as SERV

DELAY_DEVICE = 3
DELAY_LISTENER = 1.5

# GitHub repository details
repo_owner = "jotigokaraju"
repo_name = "brailleconverter"
file_path = "instructions.txt"

# GitHub API URL
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

# HIDE
access_token = "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"

servo_pins = [1, 2, 3, 4, 5]

#Set Up Servos
SERV.setmode(SERV.BCM)
for pin in servo_pins:
    SERV.setup(pin, SERV.OUT)
    
def servo(character):
    if character == 0:
        #Move Server Number 1
    elif character == 1:
        #Move Server Number 2
    elif character == 2:
        #Move Server Number 3
    elif character == 3:
        #Move Server Number 4
    elif character == 4:
        #Move Server Number 5
    else:
        #Move Server Number 6

def handle(current_content_list):
    for element in current_content_list:
        #Code to Reset all Servo Motors...
        for character in len(element)-1:
            if element[character] == "1":
                servo(character)
        time.sleep(DELAY_DEVICE)
                

while True:

    try:
        
        # Get content
        response = requests.get(api_url, headers={"Authorization": f"Bearer {access_token}"})
        response_data = response.json()
    
        # Extract content
        current_content = response_data["content"]
        current_content_decoded = base64.b64decode(current_content).decode("utf-8")
        current_content_list = json.loads(current_content_decoded)
        if current_content_list != "":
            
            handle(current_content_list)
            
            # Update content
            new_content = ""
    
            # Encode new content
            new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    
            # Prepare data
            data = {
                "message": "Update instructions.txt remove existing instructions",
                "content": new_content_encoded,
                "sha": response_data["sha"]
            }
    
            # Update
            update_response = requests.put(api_url, headers={"Authorization": f"Bearer {access_token}"}, json=data)
    
            if update_response.status_code == 200:
                print("Sent!")
            else:
                print(f"Error updating file. Status code: {update_response.status_code}")
        
        time.sleep(DELAY_LISTENER)
        
    except KeyboardInterrupt:
        SERV.cleanup()
