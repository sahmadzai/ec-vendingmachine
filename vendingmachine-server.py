import RPi.GPIO as GPIO
from flask import Flask, request
import time
import signal
import sys

# Global time sleep durations
BUTTON_PRESS_DURATION = 0.5
BUTTON_REST_DURATION = 0.5

# Set up GPIO with 0 as the initial state
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=0)
GPIO.setup(10, GPIO.OUT, initial=0)
GPIO.setup(11, GPIO.OUT, initial=0)

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
        12: (11, 8, 11, 10)
    }
    
    # Check if choice is in the dictionary
    if usr_choice in pin_mapping:
        return pin_mapping[usr_choice]
    else:
        raise ValueError("Invalid choice. Please select a valid option.")
            

# Function to control GPIO pins
def control_gpio(pin1, pin2, pin3, pin4):
    # Trigger first set of pins
    print("\nTriggering first set of GPIO pins " + str(pin1) + " & " + str(pin2)) 
    GPIO.output(pin1, 1)
    GPIO.output(pin2, 1)
    time.sleep(BUTTON_PRESS_DURATION)
    print("\nTurning " + str(pin1) + " & " + str(pin2) + " off")
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 0)
    
    time.sleep(BUTTON_REST_DURATION)
    
    # Trigger second set of pins
    print("\nTriggering second set of GPIO pins " + str(pin3) + " & " + str(pin4)) 
    GPIO.output(pin3, 1)
    GPIO.output(pin4, 1)
    time.sleep(BUTTON_PRESS_DURATION)
    print("\nTurning " + str(pin3) + " & " + str(pin4) + " off")
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 0)
    

# Signal handler for SIGINT (KeyboardInterrupt)
def signal_handler(sig, frame):
    print("KeyboardInterrupt: Cleaning up GPIO...")
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
        
