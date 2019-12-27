#!/usr/bin/env python3
'''
**********************************************************************
* Filename 		: relay1.py
* Description 	        : a sample script for 2-Channel High trigger Relay 
* Author 		: Derek
**********************************************************************
'''
import RPi.GPIO as GPIO
from time import sleep

import sensors as sensor
import Adafruit_DHT       #support of DHT sensor

GPIO.setmode(GPIO.BCM)

Relay_pin = 17
o_RC = sensor.relay(Relay_pin)

DHT_SENSOR = Adafruit_DHT.DHT22
print("DHT="+str(DHT_SENSOR))

DHT_PIN    = 4
o_HT = sensor.humidity(DHT_SENSOR,DHT_PIN)

def main():
    
    while True:
        print("pre hvalue")
        hvalue =  o_HT.read_h()
        print("hvalue: "+str(hvalue))
        sleep(2)
        o_RC.switchON()
        sleep(2)
        o_RC.switchOFF()	

def destroy():
	o_RC.switchON()
	GPIO.cleanup()
	print("\nAll done in relay\n")

if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		destroy()

