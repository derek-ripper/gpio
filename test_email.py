#!/usr/bin/env python3
###############################################################################
# Program   : test_pin
# Created by: Derek Ripper
# Date      : 25 Sep 2023
# Modified  :
# Purpose   : To test setting an unused pin to a known status and using this
#             with GPIO.py to force an email to be sent.
#         
###############################################################################
#         
###############################################################################
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#Needed as using a single GPIO pin as both input & output.
GPIO.setwarnings(False) 

# GPIO pin = 16, Physical pin 36
pin_test = 16
GPIO.setup(pin_test, GPIO.OUT)
print("                  EMAIL Testing Routine")
print("       H= send failure Msg, L= send OK email, S= status")
answer = input("Please input H, L or S: ")
answer = answer.upper()
if answer == "H":    # Forces test email to be sent.
    GPIO.output(pin_test, GPIO.HIGH)

    
elif answer == "L":  # Normal state on program startup.
    GPIO.output(pin_test, GPIO.LOW)
	 
elif answer == "S":  # Shows status 
	state = GPIO.input(pin_test)

	if(state == True):
		print("Pin "+str(pin_test)+"  Force email to be sent")
	else:
		print("Pin "+str(pin_test)+"  Reverted to normal status")
	
else:
    print("ERROR: Not a Valid Option value = "+answer.upper())

