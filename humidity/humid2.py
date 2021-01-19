#!/usr/bin/env python3
import Adafruit_DHT

class Humidity(object):

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
    dht        = Humidity()

    lcd = Mylcd(i2c_expander='PCF8574', address=0x27)
    
    logger = DU.c_logger("/home/pi/dev/gpio/humidity/", "logyyy.txt")
    errcnt = 0
    polls  = 0
    
    lcd.write2pos("Bad Reads= "+str(errcnt),4,1)   

        
    while True:
        try:
            T.sleep(5)
            polls += 1
            humid, temp = dht.read_ht(DHT_SENSOR,DHT_PIN)
            print("type humid: "+ str(type(humid)))
            print("type temp: " + str(type(temp)))
            # check that a reading was possible
            if type(humid) == float :
            
                if humid != 999:
                    # check for crazy values from DHT22
                    if humid >= 0 and humid <= 100:
                        lcd.write2pos("Temp     = {0:0.2f}".format(temp)+chr(223)+"C", 1,1)
                        lcd.write2pos("RH       = {0:0.2f}".format(humid)+" %",2,1)
                        lcd.write2pos("Poll cnt = {0:0.0f}".format(polls),3,1)

                        print("Temp={0:0.2f}*C  Humidity={1:0.2f}%".format(temp, humid))
                        logger.write("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temp, humid))
                    else:
                        errcnt += 1            
                        logger.write("Humidity out of normal range! value= "+str(humid))
                    
                else:
                    errcnt += 1
                    logger.write("Read Errors + " +str(errcnt))
                    lcd.write2pos("Bad Reads= "+str(errcnt),4,1)   
                    
            else: 
                print("Unable to read sensor dht22")
        
        except KeyboardInterrupt:
            print("\nUser abort with CTRL-C\n")
            logger.write("\nUser abort with CTRL-C\n")
            lcd.cleanup()
            exit()
