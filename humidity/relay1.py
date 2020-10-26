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

logger  = DU.c_logger("/home/pi/dev/gpio/humidity/logs","log1.txt")
logger2 = DU.c_logger("/home/pi/dev/gpio/humidity/logs","log2.txt")

print("\nStarting RELAY!.py ...........\n")

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
    PollTime      = int(o_cfg.GetConfigValue('POLLTIME'))
    RestTime      = int(o_cfg.GetConfigValue('RESTTIME'))
    MaxConRunTime = int(o_cfg.GetConfigValue('MAXCONRUNTIME'))
    
    OffThres = float(o_cfg.GetConfigValue('OFFTHRES')) # % RH - Threshold to turn OFF power
    OnThres  = float(o_cfg.GetConfigValue('ONTHRES'))  # % RH - Threshold to turn ON  power
    
    ### COUNTERS
    OFFcount = 1 # set in the intialisaton process
    ONcount  = 1 # ditto 
    PollCount= 0 #
    errcnt   = 0 # count of errors reading the DHT11 sensor
            
    ### set initial state
    logger.write("***** INITIALISATION *****")
    logger.write("SWITCHing  **ON* at START UP for the length of the first poll")
    logger.write("                 to prove the Dehumidifier starts up OK!")
    o_RL1.switchON()
    sleep(PollTime)
    
    o_RL1.switchOFF()
    ON_FLAG = False
    logger.write("STARTUP   State = SWITCHed  OFF")
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
        logger.write("")
        logger.write("*** Poll # = "+str(PollCount)+" ***")
        sleep(PollTime)
        #
        # check here for config file update
        # if updated reload config values
        
        
        #
        hvalue, tvalue =  o_HT.read_dht()
        if(hvalue == 999):
            errcnt +=1
            logger.write("ERROR: reading DHTT11 values count= "+str(errcnt))
            if(errcnt >5):
                logger.write("ERROR: Maxiumm sensor read errors detected - program halted")
                break
        else:
            pass
        
        etime = o_T.secs2dhms(o_T.elapsedtime()) 
        logger.write ("Humidity : "+str(hvalue)+", Temp: "+str(tvalue)+" Elapased= "+str(etime) )
        logger2.write("Humidity : "+str(hvalue)+", Temp: "+str(tvalue)+" Elapased= "+str(etime) )

        if  hvalue > OnThres: 
            if not ON_FLAG: # 1st time in this section of code
                ON_FLAG = True
                ONcount += 1
                logger.write("Zone_ON   SWITCHing  ON, count= "+str(ONcount))
                o_T.resetstarttime()
                o_RL1.switchON()
            else:          # 2nd or subsequent time in this code section
                logger.write("Zone_ON   State = SWITCHed  ON")
                CheckMaxRunTime(MaxConRunTime, RestTime, PollTime,  ON_FLAG)            
        
        elif hvalue <= OffThres:
            if ON_FLAG : # ie 1st time in this code section
                ON_FLAG = False
                OFFcount += 1                
                logger.write("Zone_OFF   SWITCHing OFF,count= "+str(OFFcount))
                o_T.calctotruntime()
                o_RL1.switchOFF()
                
            else:
                logger.write("Zone_OFF   State = SWITCHed OFF")
    
        else: # Between the Max and Min thresholds
            if ON_FLAG:
                logger.write("Zone_ONorOFF   State = SWITCHed ON  - In the MAX to MIN zone")
                CheckMaxRunTime(MaxConRunTime, RestTime, PollTime, ON_FLAG )
            else:
                logger.write("Zone_ONorOFF   State = SWITCHed OFF")

        logger.write("*** END OF POLLING LOOP")             

        # End of Polling Loop
        
def CheckMaxRunTime(MaxConRunTime, RestTime, PollTime, ON_FLAG):
        # Purpose: Check that maximum continuous run time has not been exceeded and if it has 
        #          been then invoke rest period.
        if  o_T.elapsedtime() > (MaxConRunTime):
            
            logger.write("   MAX Continuous runing time reached. Value = "+str(o_T.secs2dhms(o_T.elapsedtime())) )
            logger.write("   Invoking rest time of: "+str(o_T.secs2dhms(RestTime)))
            
            logger.write("   SWITCHing  OFF")
            o_RL1.switchOFF()
            o_T.calctotruntime()
            ttot = o_T.secs2dhms(o_T.gettotruntime() )
            logger.write("   Continuous running time to date is: "+str(ttot) )
            
            sleep(RestTime)
            o_T.resetstarttime()
            logger.write("   SWITCHing  ON")
            o_RL1.switchON()
        else:
            logger.write("   Max run time NOT exceeded")

def destroy():
    o_RL1.switchOFF()
    GPIO.cleanup()
    print("\nTotal ON time: "+str(o_T.secs2dhms(o_T.gettotruntime()) ))
    print("\nAll done in relay\n")

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        destroy()

