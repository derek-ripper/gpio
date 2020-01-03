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
GPIO.setwarnings(False)
Relay1_pin = 17
o_RL1 = sensor.relay(Relay1_pin)

DHT_SENSOR = 22
DHT_PIN    = 4

o_HT = sensor.humidity(DHT_SENSOR,DHT_PIN)
o_T  = T.timer()

def main():
    InitialOnTime = 20   #seconds
    PollTime      =  5*1 #seconds
    RestTime      = 10*1 #seconds
    MaxConRunTime = 20   #seconds
    
    
    OFFcount = 0
    ONcount  = 0
    PollCount= 0
    OffThres = 40      # % RH
    OnThres  = 41      # % RH
    
            
    # set initial state
    logger.write("SWITCHing  ON at START UP and sleeping for "+str(InitialOnTime)+" secs.")
    o_RL1.switchON()
    ON_FLAG = True
    sleep(InitialOnTime)
    
    while True: # The polling Loop
        PollCount += 1
        logger.write("***")
        logger.write("*** Poll number = "+str(PollCount) )

        
        hvalue, tvalue =  o_HT.read_dht()
        etime = str(round(o_T.elapsedtime(),2)) 
        logger.write("Humidity : "+str(hvalue)+", Temperature: "+str(tvalue)+" Elapased= "+str(etime))

        if  hvalue > OnThres:  
            logger.write("Checking if continuous running time exceeded of "+str(MaxConRunTime)+" secs.")  
            logger.write("Elapsed time is: "+str(round(o_T.elapsedtime(),2)) )
            CheckMaxRunTime(MaxConRunTime, RestTime)
                

            logger.write("SWITCHing  ON, count= "+str(ONcount))
            o_T.resetstarttime()
            ON_FLAG = True
            ONcount += 1
            o_RL1.switchON()

	    
        elif hvalue <= OffThres:
            OFFcount += 1
            logger.write("SWITCHing OFF, count= "+str(OFFcount))
            ON_FLAG = False
            o_RL1.switchOFF()
        
        else:
            logger.write("In the MAX to MIN zone ON_FLAG= "+str(ON_FLAG))
            if ON_FLAG:
                 CheckMaxRunTime(MaxConRunTime, RestTime)
                 ONcount += 1
                 o_RL1.switchON()
                    
        sleep(PollTime)
        # End of Polling Loop
        
def CheckMaxRunTime(MaxConRunTime, RestTime):
        if  o_T.elapsedtime() > MaxConRunTime:
            logger.write("MAX Continuous runing time reached. Value = "+str(o_T.elapsedtime()) )
            logger.write("Invoking rest time of: "+str(RestTime)) 
            sleep(RestTime)
            o_T.resetstarttime()




def destroy():
	o_RL1.switchOFF()
	GPIO.cleanup()
	print("\nAll done in relay\n")

if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		destroy()

