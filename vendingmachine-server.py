import RPi.GPIO as GPIO
from flask import Flask, request
import time
import signal
import sys

# Temp URL (changes every run): 

# Global time sleep durations
BUTTON_PRESS_DURATION = 3
BUTTON_REST_DURATION = 0.8

# Set GPIO mode to BOARD, which means we are referring to the physical pin numbers.
GPIO.setmode(GPIO.BOARD)

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
        
        control_gpio(PIN_COMBINATION[0], PIN_COMBINATION[1])
        return ("\n GPIO pins " + str(PIN_COMBINATION[0]) + " , " + str(PIN_COMBINATION[1]) + " were triggered.")
    else:
        return "Invalid request"

# Function to determine which pins based on selection
def get_pins(usr_choice):
    # Dictionary to map choices to pin combinations
    pin_mapping = {
        10: (31, 3),
        12: (31, 7),
        14: (31, 13),
        16: (31, 19),
        18: (31, 23),
        20: (33, 3),
        22: (33, 7),
        24: (33, 13),
        26: (33, 19),
        28: (33, 23),
        30: (35, 3),
        31: (35, 5),
        32: (35, 7),
        33: (35, 11),
        34: (35, 13),
        35: (35, 15),
        36: (35, 19),
        37: (35, 21),
        38: (35, 23),
        39: (35, 29),
        40: (37, 3),
        42: (37, 7),
        44: (37, 13),
        46: (37, 19),
        48: (37, 23),
        50: (26, 3),
        51: (26, 5),
        52: (26, 7),
        53: (26, 11),
        54: (26, 13),
        55: (26, 15),
        56: (26, 19),
        57: (26, 21),
        58: (26, 23),
        59: (26, 29),
        60: (32, 3),
        62: (32, 7),
        64: (32, 13),
        66: (32, 19),
        68: (32, 23),
    }
    
    # Check if choice is in the dictionary
    if usr_choice in pin_mapping:
        return pin_mapping[usr_choice]
    else:
        raise ValueError("Invalid choice. Please select a valid option.")
            

# Function to control GPIO pins
def control_gpio(pin1, pin2):
    # Trigger first set of pins
    # print("\nTriggering first set of GPIO pins " + str(pin1) + " & " + str(pin2))
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, 0)

    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin2, 0)
    time.sleep(BUTTON_PRESS_DURATION)

    # print("\nTurning " + str(pin1) + " & " + str(pin2) + " off")
    GPIO.setup(pin1, GPIO.IN)
    GPIO.setup(pin2, GPIO.IN)
    

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
    
        
