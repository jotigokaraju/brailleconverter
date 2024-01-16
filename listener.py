import requests
import base64
import json
import time
import RPi.GPIO as GPIO

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


#Stepper Motor 1
in1 = 17
in2 = 18
in3 = 27
in4 = 22


step_sleep = 0.002

step_count = 512 # 5.625*(1/64) per step, 4096 steps is 360 Degrees, Octagonal Disc has 8 sides. 512 steps for 45 Degrees.

direction = False 

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )

# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0 ;

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()


values_list1 = [0]
values_list2 = [0]

def calc_move_amount(values_list, instruction_set):
    move_to_position = instruction_set[0]
    values_list.append(move_to_position)
    if values_list[-1] >= values_list1[-2]:
        move_amount = values_list1[-1] - values_list[-2]
    else:
        move_amount = values_list[-1] + (7-values_list[-1]) + values_list[-2]

    return move_amount
        

def handle(values_list1, values_list2, instruction_set):
    move_amount_motor1 = calc_move_amount(values_list1, instruction_set)
    move_amount_motor2 = calc_move_amount(values_list2, instruction_set)
    try:
        index_motor_1 = 0
        for index_motor_1 in range(step_count*move_amount_motor1):
            for pin in range(0, len(motor_pins)):
                GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )

            #motor_step_counter = (motor_step_counter - 1) % 8
            motor_step_counter = (motor_step_counter + 1) % 8
            time.sleep(step_sleep)
    
    except KeyboardInterrupt:
        cleanup()
        exit(1)

    time.sleep(DELAY_DEVICE)
    cleanup()

    
                

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

        for instruction_set in current_content_list:
            handler(instruction_set)
            
        time.sleep(DELAY_LISTENER)
    
