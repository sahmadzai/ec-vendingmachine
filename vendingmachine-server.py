import RPi.GPIO as GPIO
from flask import Flask, request
import time
import signal
import sys

# Global time sleep durations
BUTTON_PRESS_DURATION = 1
BUTTON_REST_DURATION = 0.8

# Set up GPIOs with 0 as the initial state
# We're using GPIO pins 11, 13, 15, 16, 18, 22, 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=0)
GPIO.setup(13, GPIO.OUT, initial=0)
GPIO.setup(15, GPIO.OUT, initial=0)
GPIO.setup(16, GPIO.OUT, initial=0)
GPIO.setup(18, GPIO.OUT, initial=0)
GPIO.setup(22, GPIO.OUT, initial=0)
GPIO.setup(29, GPIO.OUT, initial=0)

# Flask app
app = Flask(__name__)

# API endpoint to receive the request from Power Automate
@app.route('/trigger', methods=['POST'])
def trigger_gpio():
    data = request.get_json(force=True)
    print("Data recieved:", data)
    if data and 'selection' in data:
        PIN_COMBINATION = get_pins(data['selection'])
        print(PIN_COMBINATION)
        
        control_gpio(PIN_COMBINATION[0], PIN_COMBINATION[1], PIN_COMBINATION[2], PIN_COMBINATION[3])
        return ("\n GPIO pins " + str(PIN_COMBINATION[0]) + " , " + str(PIN_COMBINATION[1]) + " & " + str(PIN_COMBINATION[2]) + ", " + str(PIN_COMBINATION[3]) + " were triggered.")
    else:
        return "Invalid request"

# Function to determine which pins based on selection
def get_pins(usr_choice):
    # Dictionary to map choices to pin combinations
    pin_mapping = {
        10: (29, 22, 18, 11),
        12: (29, 22, 29, 18),
        14: (29, 22, 22, 15),
        16: (29, 22, 15, 16),
        18: (29, 22, 18, 13),
        20: (29, 18, 18, 11),
        22: (29, 18, 29, 18),
        24: (29, 18, 22, 15),
        26: (29, 18, 15, 16),
        28: (29, 18, 18, 13),
        30: (29, 16, 18, 11),
        32: (29, 16, 29, 18),
        34: (29, 16, 22, 15),
        36: (29, 16, 15, 16),
        38: (29, 16, 18, 13),
        40: (22, 15, 18, 11),
        42: (22, 15, 29, 18),
        44: (22, 15, 22, 15),
        46: (22, 15, 15, 16),
        48: (22, 15, 18, 13),
        50: (15, 18, 18, 11),
        51: (15, 18, 29, 22),
        52: (15, 18, 29, 18),
        53: (15, 18, 29, 16),
        54: (15, 18, 22, 15),
        55: (15, 18, 15, 18),
        56: (15, 18, 15, 16),
        57: (15, 18, 22, 13),
        58: (15, 18, 18, 13),
        59: (15, 18, 13, 16),
        60: (15, 16, 18, 11),
        62: (15, 16, 29, 18),
        64: (15, 16, 22, 15),
        66: (15, 16, 15, 16),
        68: (15, 16, 18, 13)
    }
    
    # Check if choice is in the dictionary
    if usr_choice in pin_mapping:
        return pin_mapping[usr_choice]
    else:
        raise ValueError("Invalid choice. Please select a valid option.")
            

# Function to control GPIO pins
def control_gpio(pin1, pin2, pin3, pin4):
    # Trigger first set of pins
    # print("\nTriggering first set of GPIO pins " + str(pin1) + " & " + str(pin2)) 
    GPIO.output(pin1, 1)
    GPIO.output(pin2, 1)
    time.sleep(BUTTON_PRESS_DURATION)
    # print("\nTurning " + str(pin1) + " & " + str(pin2) + " off")
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 0)
    
    time.sleep(BUTTON_REST_DURATION)
    
    # Trigger second set of pins
    # print("\nTriggering second set of GPIO pins " + str(pin3) + " & " + str(pin4)) 
    GPIO.output(pin3, 1)
    GPIO.output(pin4, 1)
    time.sleep(BUTTON_PRESS_DURATION)
    # print("\nTurning " + str(pin3) + " & " + str(pin4) + " off")
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 0)
    

# Signal handler for SIGINT (KeyboardInterrupt)
def signal_handler(sig, frame):
    print("KeyboardInterrupt: Cleaning up GPIO...")
    GPIO.cleanup()
    sys.exit(0)
    
# Manually test GPIO combinations for testing purposes
def manual_test():
    while True:
        try:
            usr_input = input("Enter GPIO pin combination: ")
            selection = usr_input.split(" ")
            print(selection)
            print(selection[0])
            GPIO.output(int(selection[0]), 1)
            time.sleep(BUTTON_PRESS_DURATION)
            GPIO.output(int(selection[1]), 0)
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt: Cleaning up GPIO...")
            GPIO.cleanup()
            sys.exit(0)

if __name__ == '__main__':
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Manual test
    # manual_test()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
    
        
