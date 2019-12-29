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
import mytimer as T

# needed to access my other Pyton std. modules
import os, sys
sys.path.append(os.path.abspath("/home/pi/dev/gpio"))
import DU

logger = DU.c_logger("/home/pi/dev/gpio/humidity/", "log1.txt")

# set Pi pin config to "Board" not Physical pin numbers
GPIO.setmode(GPIO.BCM)

Relay_pin = 17
o_RC = sensor.relay(Relay_pin)

DHT_SENSOR = 22
DHT_PIN    = 4

o_HT = sensor.humidity(DHT_SENSOR,DHT_PIN)
o_T  = T.timer()

def main():
    PollTime      = 5 *1 #seconds
    RestTime      = 10*1 #seconds
    
    
    OFFcount = 0
    ONcount  = 0
    PollCount= 0
    OffThres = 40
    OnThres  = 41
    
    while True: # polling Loop
        PollCount += 1
        logger.write("*** Poll number = "+str(PollCount) )
        
        hvalue, tvalue =  o_HT.read_dht()
        logger.write("Humidity : "+str(hvalue)+", Temperature: "+str(tvalue))

        if  hvalue > OnThres:  
            logger.write("Checking continuouis running time")  
            if o_T.elapsedtime > MaxConRunTime:
                logger.write("Invoking rest time of: "+str(RestTime)) 
                sleep(RestTime)
                o_T.resetstarttime()
                
            ONcount += 1
            logger.write("SWITCHing  ON, count= "+str(ONcount))
            o_RC.switchON()

	    
        elif hvalue <= OffThres:
            OFFcount += 1
            logger.write("SWITCHing OFF, count= "+str(OFFcount))
            o_RC.switchOFF()	

             
        # End of Polling Loop
        sleep(PollTime)
        
def destroy():
	o_RC.switchON()
	GPIO.cleanup()
	print("\nAll done in relay\n")

if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		destroy()

