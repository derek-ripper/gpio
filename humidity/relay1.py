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

# needed to access my other Pyton std. modules
import os, sys
sys.path.append(os.path.abspath("/home/pi/dev/gpio"))
import DU

logger = DU.c_logger("/home/pi/dev/gpio/humidity/", "log1.txt")

GPIO.setmode(GPIO.BCM)

Relay_pin = 17
o_RC = sensor.relay(Relay_pin)

DHT_SENSOR = Adafruit_DHT.DHT22
print("DHT="+str(DHT_SENSOR))

DHT_PIN    = 4
o_HT = sensor.humidity(DHT_SENSOR,DHT_PIN)

def main():
    wait = 10 # seconds
    OFFcount = 0
    ONcount  = 0
    while True:
        print("pre read hvalue")
        hvalue, tvalue =  o_HT.read_dht()
        logger.write("Humidity : "+str(hvalue)+", Temperature: "+str(tvalue))
        print("hvalue: "+str(hvalue))
        print("tvalue: "+str(tvalue))
        sleep(5)
        
        ONcount += 1
        logger.write("SWITCH  ON, count= "+str(ONcount))
        print("** pre switch ON  count= "+str(ONcount))
        o_RC.switchON()
        sleep(wait)
        
        OFFcount += 1
        logger.write("SWITCH OFF, count= "+str(OFFcount))
        print("** pre switch OFF count= "+str(OFFcount))        
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

