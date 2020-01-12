#!/usr/bin/env python3
''' 
**********************************************************************
* Filename      : relay1.py
* Description           : a sample script for 2-Channel High trigger Relay 
* Author        : Derek
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

# set Pi pin config to "Board" NOT Physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Relay1_pin = 17
o_RL1 = sensor.relay(Relay1_pin)

DHT_SENSOR = 22
DHT_PIN    = 4

o_HT = sensor.humidity(DHT_SENSOR,DHT_PIN)
o_T  = T.timer()

def main():
    import config   as CFG    
    o_cfg     = CFG.ReadConfig('config.txt')
    
    ### CONSTANTS 
    InitialOnTime = int(o_cfg.GetConfigValue('INITIALONTIME'))
    PollTime      = int(o_cfg.GetConfigValue('POLLTIME'))
    RestTime      = int(o_cfg.GetConfigValue('RESTTIME'))
    MaxConRunTime = int(o_cfg.GetConfigValue('MAXCONRUNTIME'))
    
    OffThres = float(o_cfg.GetConfigValue('OFFTHRES')) # % RH - Threshold to turn OFF power
    OnThres  = float(o_cfg.GetConfigValue('ONTHRES'))  # % RH - Threshold to turn ON  power
    
    ### COUNTERS
    OFFcount = 0
    ONcount  = 0
    PollCount= 0

            
    ### set initial state
    logger.write("SWITCHing  ON at START UP and sleeping for "+str(InitialOnTime)+" secs.")
    o_RL1.switchON()
    ON_FLAG = True
    sleep(InitialOnTime)
    o_T.resetstarttime()
    
    ### write basic data to log file
    logger.write("OFF threshold: "+str(OffThres)+" %RH")
    logger.write("ON  threshold: "+str(OnThres) +" %RH")
    logger.write("Poll interval: "+str(PollTime)+" secs")
    logger.write("Max run tme  : "+str(MaxConRunTime)+" secs")
    logger.write("Rest Time    : "+str(RestTime)+" secs")  
       
    ### THE POLLING LOOP  ###
    while True: 
        PollCount += 1
        logger.write("*")
        logger.write("*** Poll number = "+str(PollCount) )
   
        hvalue, tvalue =  o_HT.read_dht()
        etime = str(round(o_T.elapsedtime(),2)) 
        logger.write("Humidity : "+str(hvalue)+", Temperature: "+str(tvalue)+" Elapased= "+str(etime))

        if  hvalue > OnThres: 
            if not ON_FLAG: # 1st time in this section of code
                ON_FLAG = True
                ONcount += 1
                logger.write("SWITCHing  ON, count= "+str(ONcount))
                o_T.resetstarttime()
                o_RL1.switchON()
            else:          # 2nd or subsequent time in this code section
                logger.write("State = SWITCHed  ON")
                CheckMaxRunTime(MaxConRunTime, RestTime, ON_FLAG)            
        
        elif hvalue <= OffThres:
            if ON_FLAG : # ie 1st time in this code section
                ON_FLAG = False
                OFFcount += 1                
                logger.write("SWITCHing OFF,count= "+str(OFFcount))
                o_T.calctotruntime()
                o_RL1.switchOFF()
                
            else:
                logger.write("State = SWITCHed OFF")
    
        else: # Between the Max and Min thresholds
            if ON_FLAG:
                logger.write("State = SWITCHed ON  - In the MAX to MIN zone")
                CheckMaxRunTime(MaxConRunTime, RestTime,ON_FLAG )
            else:
                logger.write("State = SWITCHed OFF - In the MAX to MIN zone")

        logger.write("END OF POLLING LOOP")             
        sleep(PollTime)
        # End of Polling Loop
        
def CheckMaxRunTime(MaxConRunTime, RestTime, ON_FLAG):
        if  o_T.elapsedtime() > MaxConRunTime:
            logger.write("MAX Continuous runing time reached. Value = "+str(round(o_T.elapsedtime(),2)) )
            logger.write("Invoking rest time of: "+str(RestTime))
            ON_FLAG = False 
            o_RL1.switchOFF()
            o_T.calctotruntime()
            
            sleep(RestTime)
        else:
            logger.write("Max run time NOT exceeded")

def destroy():
    o_RL1.switchOFF()
    GPIO.cleanup()
    print("\nTotal ON time: "+str(round(o_T.gettotruntime(),2) ))
    print("\nAll done in relay\n")

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        destroy()

