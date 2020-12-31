#!/usr/bin/env python3
import Adafruit_DHT

class humidity(object):

    def read_ht(self,DHT_SENSOR,DHT_PIN):
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        return humidity, temperature

#############################################################################
import os
import sys
import time as T

# needed to access my other Pyton std. modules
sys.path.append(os.path.abspath("/home/pi/dev/gpio"))
import DU
from  RPLCD_class import Mylcd


if __name__ == '__main__':

    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN    = 4
    DHT        = humidity()

    lcd = Mylcd(i2c_expander='PCF8574', address=0x27)
    
    logger = DU.c_logger("/home/pi/dev/gpio/humidity/", "logxxx.txt")
    errcnt = 0
    polls  = 0
    
    lcd.write2pos("Bad Read = "+str(errcnt),4,1)   

        
    while True:
        try:
            T.sleep(5)
            polls += 1
            humid, temp = DHT.read_ht(DHT_SENSOR,DHT_PIN)
            if humid != 999:
                lcd.write2pos("Temp     = {0:0.2f}".format(temp)+chr(0)+"C", 1,1)
                lcd.write2pos("HR %     = {0:0.2f}".format(humid),2,1)
                lcd.write2pos("Poll cnt = {0:0.0f}".format(polls),3,1)
                print(humid)
                print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temp, humid))
                logger.write("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temp, humid))
            else:
                errcnt += 1
                logger.write("Read Errors + " +str(errcnt))
                lcd.write2pos("Bad Read = "+str(errcnt),4,1)   
        
        except KeyboardInterrupt:
            print("\nUser abort with CTRL-C\n")
            logger.write("\nUser abort with CTRL-C\n")
            exit()
