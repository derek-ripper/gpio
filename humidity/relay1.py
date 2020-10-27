#!/usr/bin/env python3
''' 
**********************************************************************
* Filename      : relay1.py
* Purpose       : To control mains power supply to dumb Dehumidfier
* Created       : Dec 2019 fully reworked in Oct 2020 
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

print("\nStarting RELAY1.py ...........\n")

# set Pi pin config to "Board" NOT Physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Relay1_pin = 17
oRL1 = sensor.relay(Relay1_pin)

DHT_SENSOR = 22
DHT_PIN    = 4

oHT = sensor.humidity(DHT_SENSOR,DHT_PIN)
oT  = T.timer()

def main():
    import config   as CFG    
    oCfg     = CFG.ReadConfig('config.txt')
    
    ### CONSTANTS 
    TestTime      = int(oCfg.GetConfigValue('TESTTIME'))
    PollTime      = int(oCfg.GetConfigValue('POLLTIME'))
    RestTime      = int(oCfg.GetConfigValue('RESTTIME'))
    MaxConRunTime = int(oCfg.GetConfigValue('MAXCONRUNTIME'))
    
    OffThres = float(oCfg.GetConfigValue('OFFTHRES')) # % RH - Threshold to turn OFF power
    OnThres  = float(oCfg.GetConfigValue('ONTHRES'))  # % RH - Threshold to turn ON  power
    
    ### COUNTERS
    OFFcount = 0 # set in the intialisaton process
    ONcount  = 0 # ditto 
    PollCount= 0 #
    errcnt   = 0 # count of errors reading the DHT11 sensor
            
    ### set initial state
    logger.write("***** INITIALISATION *****")
    logger.write("Start Up  SWITCHing  ON  for "+str(TestTime)+" secs"+"\n\t\t\t\t\t  to Test Humidfier fires up!")

    oRL1.switchON()
    sleep(TestTime)
    
    oRL1.switchOFF()
    ON_FLAG = False
    logger.write("STARTUP   State = SWITCHed  OFF")
    oT.resetstarttime()
    
    ### write basic data to log file
    logger.write("")
    logger.write("Basic Control Data")
    logger.write("Test Time         : "+str(TestTime)+" secs")
    logger.write("Poll interval     : "+str(PollTime)+" secs")
    logger.write("Max con run time  : "+str(MaxConRunTime)+" secs")
    logger.write("Rest Time         : "+str(RestTime)+" secs")  
    logger.write("")
    logger.write("OFF threshold     : "+str(OffThres)+" %RH")
    logger.write("ON  threshold     : "+str(OnThres) +" %RH")
    logger.write("")
    
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
        hvalue, tvalue =  oHT.read_dht()
        if(hvalue == 999):
            errcnt +=1
            logger.write("ERROR: reading DHT-11 values. Error count= "+str(errcnt))
            if(errcnt >5):
                logger.write("ERROR: Maxiumm sensor read errors detected - program halted")
                break
        else:
            pass
        
        etime = oT.secs2dhms(oT.elapsedtime()) 
        logger.write ("Humidity : "+str(hvalue)+", Temp: "+str(tvalue)+" Elapased= "+str(etime) )
        logger2.write("Humidity : "+str(hvalue)+", Temp: "+str(tvalue)+" Elapased= "+str(etime) )

        if  hvalue > OnThres: 
            if not ON_FLAG: # 1st time in this section of code
                ON_FLAG = True
                ONcount += 1
                logger.write("Zone_ON   SWITCHing  ON, count= "+str(ONcount))
                oT.resetstarttime()
                oRL1.switchON()
            else:          # 2nd or subsequent time in this code section
                logger.write("Zone_ON   State = SWITCHed  ON")
                CheckMaxRunTime(MaxConRunTime, RestTime, PollTime,  ON_FLAG)            
        
        elif hvalue <= OffThres:
            if ON_FLAG : # ie 1st time in this code section
                ON_FLAG = False
                OFFcount += 1                
                logger.write("Zone_OFF   SWITCHing OFF,count= "+str(OFFcount))
                oT.calccumruntime()
                oRL1.switchOFF()
                
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
        if  oT.elapsedtime() > (MaxConRunTime):
            logger.write("   Time since program started up            : "+str(oT.secs2dhms(int(oT.timefromprogramstart()) ))) 
            
            logger.write("   MAX Con. running time exceeded. Value    : "+str(oT.secs2dhms(oT.elapsedtime())) )
            logger.write("   NOW Invoking rest time of                : "+str(oT.secs2dhms(RestTime)))
            
            logger.write("   SWITCHing  OFF")
            oRL1.switchOFF()
            oT.calccumruntime()
            ttot = oT.secs2dhms(oT.getcumruntime() )
            logger.write("   Cum. Continuous running time to date is  : "+str(ttot) )
            
            sleep(RestTime)
            oT.resetstarttime()
            logger.write("   SWITCHing  ON")
            oRL1.switchON()
        else:
            logger.write("   Max run time NOT exceeded")

def destroy():
    oRL1.switchOFF()
    GPIO.cleanup()
    print("\nTime since program start: "+str(oT.secs2dhms(int(oT.timefromprogramstart()) ))) 
    print(  "Total ON time           : "+str(oT.secs2dhms(oT.getcumruntime()) ))
    print("\nAll done in relay\n")

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        destroy()

