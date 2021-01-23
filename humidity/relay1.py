#!/usr/bin/env python3
''' 
**********************************************************************
* Filename      : relay1.py
* Purpose       : To control mains power supply to dumb Dehumidfier
* Created       : Dec 2019 fully reworked in Jan 2021 
* Author        : Derek
**********************************************************************
* 16 Nov 2020 - make config data reload if fileexternally changed.
*
**********************************************************************
Updates:
20 Jan 2021 - DHTsensor now powered from a GPIO pin. Hence new routine to 
              reaset it. Previously done using spare relay in the 
              2 channel module on a direct power line. RElay2 left in code 
              but not used. Status set that on board LED is not lit.
22 Jan 2021 - Reworked to add LCD output dispaly.
'''
# needed to access my other Pyton std. modules
import sys, os
sys.path.append(os.path.abspath("/home/pi/dev/gpio"))

import RPi.GPIO as GPIO
from time import sleep
from  RPLCD_class import Mylcd

import sensors   as sensor
import mytimer   as T
import FileClass as FU
import os
import DU
import config   as CFG 

class params(object):
    def __init__(self, File):
        self.InputFile = File
        self.LoadParams(self.InputFile)
        self.wrte2logfile()

        
    def LoadParams(self,configfile):    
        oCfg     = CFG.ReadConfig(configfile)
        self.TestTime      = int(oCfg.GetConfigValue('TESTTIME'))
        self.PollTime      = int(oCfg.GetConfigValue('POLLTIME'))
        self.RestTime      = int(oCfg.GetConfigValue('RESTTIME'))
        self.MaxConRunTime = int(oCfg.GetConfigValue('MAXCONRUNTIME'))
    
        self.OffThres = float(oCfg.GetConfigValue('OFFTHRES')) # % RH - Threshold to turn OFF power
        self.OnThres  = float(oCfg.GetConfigValue('ONTHRES'))  # % RH - Threshold to turn ON  power
    
    def wrte2logfile(self):
        ### write basic data to log file

        logger.write("Basic Control Data")
        logger.write("Test Time         : "+str(self.TestTime)+" secs")
        logger.write("Poll interval     : "+str(self.PollTime)+" secs")
        logger.write("Max con run time  : "+str(self.MaxConRunTime)+" secs")
        logger.write("Rest Time         : "+str(self.RestTime)+" secs")  
        logger.write("")
        logger.write("OFF threshold     : "+str(self.OffThres)+" %RH")
        logger.write("ON  threshold     : "+str(self.OnThres) +" %RH")

        
    def ReLoadParams(self):
        self.LoadParams(self.InputFile)
        self.wrte2logfile()
# set Pi pin config to "Board" NOT Physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

##### Object Defintions
logger  = DU.c_logger("/home/pi/dev/logs","log1.txt")
logger2 = DU.c_logger("/home/pi/dev/logs","log2.txt")

lcd     = Mylcd(i2c_expander='PCF8574', address=0x27, cols=16, rows=2)


# Realy #1 switched mains voltage !| grep re

Relay1_pin = 17
oRL1 = sensor.Relay(Relay1_pin)

## Relay #2 NOT used as at 20 Jan 2020
Relay2_pin = 18
oRL2 = sensor.Relay(Relay2_pin)
oRL2.switchOFF()

DHT_SENSOR  = 22
DHT_PIN     = 4  
DHT_PWR_PIN = 27

oHT = sensor.Humidity(DHT_SENSOR,DHT_PIN, DHT_PWR_PIN)

oT  = T.timer()

oP = params("config.txt")     # run time parameters      

oF = FU.FileMod(oP.InputFile) # check if file updated while prog is Live
#####

def main():
    print("\nStarting RELAY1.py ...........\n")
    lcd.write2pos("Starting .")
    ### COUNTERS
    OFFcount = 0 # set in the intialisaton process
    ONcount  = 0 # ditto 
    PollCount= 0 #
    errcnt   = 0 # count of errors reading the DHT22 sensor
            
    ### set initial state
    logger.write("***** INITIALISATION *****")
    logger.write("Start Up  SWITCHing  ON  for "+str(oP.TestTime)+" secs"+"\n\t\t\t\t\t  to Test Humidfier fires up!")

    oRL1.switchON()
    sleep(oP.TestTime)
    
    oRL1.switchOFF()
    ON_FLAG = False
    logger.write("STARTUP   State = SWITCHed  OFF")
    oT.resetstarttime()
    

    
    ##### Start Infinte Polling Loop
    lcd.clear()
    while True: 


        
        # Check if config.txt has been updated while program is running?
        if oF.Changed():
            logger.write("")  
            logger.write("*** START  - Run Data ReLoaded ***")
            oP.ReLoadParams()
            logger.write("*** FINISH - Run Data ReLoaded ***")
            logger.write("")  
        else:
            pass
         
         
        
        # READ DHT22 sensor values 
        hvalue, tvalue =  oHT.read_dht()
        etime = oT.secs2dhms(oT.elapsedtime()) 
        logger.write ("Humidity : "+str(hvalue)+", Temp: "+str(tvalue)+" Elapased= "+str(etime) )
        logger2.write("Humidity : "+str(hvalue)+", Temp: "+str(tvalue)+" Elapased= "+str(etime) )

        lcd.write2pos("RH%={0:0.1f}".format(hvalue),1,1)
        lcd.write2pos(" "+chr(0)+"C={0:0.1f}".format(tvalue), 1,9)
       
        lcd.write2pos("{0:0.1f}{1}{2}{3:0.1f}".format(oP.OffThres, chr(126), chr(126), oP.OnThres), 2,1)
        PollCount += 1
        logger.write("")
        logger.write("*** Poll # = "+str(PollCount)+"  Time frm Start : "+str(oT.secs2dhms(int(oT.timefromprogramstart()) )))

        
        if(hvalue == 999):
            errcnt +=1
            if(errcnt >1000):
                logger.write("ERROR: Maxiumm sensor read Errors/Resets exceeded - program halted")
                destroy()
                break
            else: # take corrective action and rseet DHT22 by repowering it
                logger.write("ERROR: Reading DHT22 values -- Power OFF DHT-22, count: "+str(errcnt))
                oHT.reset()
                logger.write("ERROR: Reading DHT22 values -- Power ON  DHT-22")


        if  hvalue > oP.OnThres: 
            if not ON_FLAG: # 1st time in this section of code
                ON_FLAG = True
                ONcount += 1
                logger.write("Zone_ON   SWITCHing  ON, count= "+str(ONcount))
                oT.resetstarttime()
                oRL1.switchON()
                lcd.write2pos("ON  ",2,13)
            else:          # 2nd or subsequent time in this code section
                logger.write("Zone_ON   State = SWITCHed  ON")
                CheckMaxRunTime(oP.MaxConRunTime, oP.RestTime, oP.PollTime,  ON_FLAG,ONcount,OFFcount)            
        
        elif hvalue <= oP.OffThres:
            if ON_FLAG : # ie 1st time in this code section
                ON_FLAG = False
                OFFcount += 1                
                logger.write("Zone_OFF   SWITCHing OFF,count= "+str(OFFcount))
                oT.calccumruntime()
                oRL1.switchOFF()
                lcd.write2pos("OFF ",2,13)
                
            else:
                logger.write("Zone_OFF   State = SWITCHed OFF")
                lcd.write2pos("OFF ",2,13)
    
        else: # Between the Max and Min thresholds
            if ON_FLAG:
                logger.write("Zone_ONorOFF   State = SWITCHed ON")
                CheckMaxRunTime(oP.MaxConRunTime, oP.RestTime, oP.PollTime, ON_FLAG, ONcount,OFFcount )
            else:
                logger.write("Zone_ONorOFF   State = SWITCHed OFF")
                
        sleep(oP.PollTime)
        logger.write("*** END OF POLLING LOOP")             

    ##### End of Polling Loop
        
def CheckMaxRunTime(MaxConRunTime, RestTime, PollTime, ON_FLAG,ONcount,OFFcount):
        # Purpose: Check that maximum continuous run time has not been exceeded and if it has 
        #          been then invoke rest period.
        if  oT.elapsedtime() > (MaxConRunTime):

            
            logger.write("   MAX Con. running time exceeded. Value    : "+str(oT.secs2dhms(oT.elapsedtime())) )
            logger.write("   NOW Invoking rest time of                : "+str(oT.secs2dhms(RestTime)))
          
            OFFcount += 1
            logger.write("   SWITCHing  OFF, count: "+str(OFFcount))
            oRL1.switchOFF()

            oT.calccumruntime()
            ttot = oT.secs2dhms(oT.getcumruntime() )
            logger.write("   Cum. Continuous running time to date is  : "+str(ttot) )
            
            lcd.write2pos("REST",2,13)
            sleep(RestTime)
            oT.resetstarttime()
            ONcount +=1
            logger.write("   SWITCHing  ON. count: "+str(OFFcount))

            oRL1.switchON()
            lcd.write2pos("ON  ",2,13)
        else:
            logger.write("   Max run time NOT exceeded.  On count: "+str(ONcount)+", OFF count: "+str(OFFcount))

def destroy():
    oRL1.switchOFF()
    lcd.cleanup()
    GPIO.cleanup()
    print("\nTime since program start: "+str(oT.secs2dhms(int(oT.timefromprogramstart()) ))) 
    print(  "Total ON time           : "+str(oT.secs2dhms(oT.getcumruntime()) ))
    print("\nAll done in relay\n")

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        destroy()

