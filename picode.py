'''
Joti Gokaraju
2024-01-09
P5 CS20
Mr. Schellenberg
Code for the Raspberry Pi Portion of the Major Project
Sources and Citations Listed on README Document
'''


#Import Neccesary Libraries
import requests
import base64
import json
import time
import RPi.GPIO as GPIO



#Set Delay Times
DELAY_DEVICE = 4
DELAY_LISTENER = 1.5



# GitHub repository details
repo_owner = "jotigokaraju"
repo_name = "brailleconverter"
file_path = "instructions.txt"

# GitHub API URL
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"

#HIDE
access_token = "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"



#Set Basic Variables on Movement Speed and Interval
step_sleep = 0.002 #Recommended Amount
step_count = 512 # 5.625*(1/64) per step, 4096 steps is 360 Degrees, Octagonal Disc has 8 sides. 512 steps for 45 Degrees.

# Defining Stepper Motor Sequence (http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]



#Stepper Motor 1

#Set Up Pins
motor1_in1 = 17
motor1_in2 = 27
motor1_in3 = 22
motor1_in4 = 23

#Set Up Each GPIO Pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1_in1, GPIO.OUT)
GPIO.setup(motor1_in2, GPIO.OUT)
GPIO.setup(motor1_in3, GPIO.OUT)
GPIO.setup(motor1_in4, GPIO.OUT)

#Intialize Each GPIO Pin
GPIO.output(motor1_in1, GPIO.LOW)
GPIO.output(motor1_in2, GPIO.LOW)
GPIO.output(motor1_in3, GPIO.LOW)
GPIO.output(motor1_in4, GPIO.LOW)

#Create Basic Lists and Variables to Store Pin Data
motor_pins = [motor1_in1,motor1_in2,motor1_in3,motor1_in4]
motor1_step_counter = 0 ;



#Stepper Motor 2

#Set Up Pins
motor2_in1 = 19
motor2_in2 = 26
motor2_in3 = 16
motor2_in4 = 20

#Set Up Each GPIO Pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor2_in1, GPIO.OUT)
GPIO.setup(motor2_in2, GPIO.OUT)
GPIO.setup(motor2_in3, GPIO.OUT)
GPIO.setup(motor2_in4, GPIO.OUT)

#Intialize Each GPIO Pin
GPIO.output(motor2_in1, GPIO.LOW)
GPIO.output(motor2_in2, GPIO.LOW)
GPIO.output(motor2_in3, GPIO.LOW)
GPIO.output(motor2_in4, GPIO.LOW)

#Create Basic Lists and Variables to Store Pin Data
motor_pins_2 = [motor2_in1,motor2_in2,motor2_in3,motor2_in4]
motor2_step_counter = 0 ;



#Creating 2 Different Values List for each Motor
values_list_motor1 = [0]
values_list_motor2 = [0]



#Functions

def calc_move_amount(values_list, instruction_set, location):
    '''Calculates Amount the Stepper Motor Needs to Move Based on (Values_List,
    instruction_set, and the location of which instructions the motor is using (0 or 1)'''
    
    move_to_position = 0
    
    #Depending on Which Stepper Motor, Read Either the First Data Point or Second Point
    move_to_position = instruction_set[location]
    
    #Add This to the Values_list for Future Use
    values_list.append(move_to_position)
    
    #Calculate Amount that is needed to be moved
    move_amount = values_list[-1] - values_list[-2]
    return move_amount
        
        

def move_motors(values_list_motor1, values_list_motor2, instruction_set, motor1_step_counter, motor2_step_counter):
    '''Main Function to Move Stepper Motors. Takes in 2 Value Lists, Instruction Sets, and 2 Motor_Step_Counters to Process and Move Motor Accordingly'''
    
    #Call the calc_move_amount function and return the result untouched
    generic_move_amount_motor1 = calc_move_amount(values_list_motor1, instruction_set, 0)
    generic_move_amount_motor2 = calc_move_amount(values_list_motor2, instruction_set, 1)
    
    #Convert the move_amount value from calc_move_amount into positive numbers for analysis
    move_amount_motor1 = abs(generic_move_amount_motor1)
    move_amount_motor2 = abs(generic_move_amount_motor2)
    
    try:
        
        #Set basic local variables
        index_motor_counter = 0
        counter_motor_1 = 0
        counter_motor_2 = 0
        
        #Count upto the maximum number of steps needed for both motors
        for index_motor_counter in range(max(step_count*move_amount_motor1, step_count*move_amount_motor2)):
            
            #Subsection to process motor 1. Only activate if it has not completed all the required steps
            if counter_motor_1 < step_count*move_amount_motor1:
                for pin_1 in range(0, len(motor_pins)):
                    
                    #Main Code to Output Value and Move Stepper Motor
                    GPIO.output( motor_pins[pin_1], step_sequence[motor1_step_counter][pin_1] )
                
                #Depending on if the generic_move_amount is positive or negative, move backwards or forwards
                if generic_move_amount_motor1 >= 0:
                    motor1_step_counter = (motor1_step_counter + 1) % 8
                else:
                    motor1_step_counter = (motor1_step_counter - 1) % 8
                
                #Record 1 full step as completed
                counter_motor_1 += 1
                
                time.sleep(step_sleep/2)
            
            
            #Subsection to process motor 1. Only activate if it has not completed all the required steps
            if counter_motor_2 < step_count*move_amount_motor2:
                for pins_motor2 in range(0, len(motor_pins_2)):
                    
                    #Main Code to Output Value and Move Stepper Motor
                    GPIO.output( motor_pins_2[pins_motor2], step_sequence[motor2_step_counter][pins_motor2] )
                
                #Depending on if the generic_move_amount is positive or negative, move backwards or forwards
                if generic_move_amount_motor2 >= 0:
                    motor2_step_counter = (motor2_step_counter + 1) % 8
                else:
                    motor2_step_counter = (motor2_step_counter - 1) % 8
                
                #Record 1 full step as completed
                counter_motor_2 += 1
                
                time.sleep(step_sleep/2)
    
    
    #To Handle Kill Commands by Keyboard or Accidental Disconnect
    except KeyboardInterrupt:
        exit(1)
    
    #Delay to Let the User Feel the Braille Displayed Before It Moves On
    time.sleep(DELAY_DEVICE)

    
                
#The Listener Function to Constently Check if There Is New Characters to Display
while True: 
    
    #Open Up the Github File
    response = requests.get(api_url, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()

    # Extract content from the Github File
    current_content = response_data["content"]
    current_content_decoded = base64.b64decode(current_content).decode("utf-8")
    
    #Extract content as a python object, not just a string
    current_content_list = json.loads(current_content_decoded)
    
    #If there is any new material checker statement
    if current_content_list != [0]:
        
        #For each individual set of instructions for a braille character within the word, print the set and call the move_motors function
        for instruction_set in current_content_list:
            print(instruction_set)
            move_motors(values_list_motor1, values_list_motor2, instruction_set, motor1_step_counter, motor2_step_counter)
        
        
        #Write to the Github File
            
        #Add Filler/Stock Content
        new_content = "[0]"

        #Encode New Content
        new_content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")

        #Process Data
        data = {
            "message": "Update instructions.txt remove existing instructions",
            "content": new_content_encoded,
            "sha": response_data["sha"]
        }

        #Upload to Github File
        update_response = requests.put(api_url, headers={"Authorization": f"Bearer {access_token}"}, json=data)
        
        #Handle Error and Success Messages for Debugging
        if update_response.status_code == 200:
            print("Sent!")
        else:
            print(f"Error updating file. Status code: {update_response.status_code}")

    
    #Print 'None' While There is No New Data, and Wait Every DELAY_LISTENER Seconds Before Checking Again
    print("None")
    time.sleep(DELAY_LISTENER)

