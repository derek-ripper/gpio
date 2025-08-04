#!/usr/bin/env python3
import Adafruit_DHT

# class Humidity(object):

    # def read_ht(self,DHT_SENSOR,DHT_PIN):
        # humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        # return humidity, temperature

#############################################################################
import os
import sys
import time as T
import RPi.GPIO as GPIO

# needed to access my other Pyton std. modules
sys.path.append(os.path.abspath("/home/pi/dev/gpio"))
import DU
import sensors as sensor
from  RPLCD_class import Mylcd

# set Pi pin config to "Board" NOT Physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

if __name__ == '__main__':

    DHT_SENSOR  = Adafruit_DHT.DHT22
    DHT_PIN     = 4
    DHT_PWR_PIN = 27
    oht = sensor.Humidity(DHT_SENSOR, DHT_PIN, DHT_PWR_PIN)
    print("RESET")
    oht.reset(offtime=10)
    lcd = Mylcd(i2c_expander='PCF8574', address=0x27, charmap='A02')
    
    logger = DU.c_logger("/home/pi/dev/gpio/humidity/", "logyyy.txt")
    errcnt = 0
    polls  = 0
    errdht11 = 0
    
    lcd.write2pos("Bad Reads= "+str(errcnt),4,1)   

        
    while True:
        try:
            T.sleep(5)
            polls += 1
            humid, temp = oht.read_dht()
            print("type humid: "+ str(type(humid)))
            print("type temp: " + str(type(temp)))
            # check that a reading was possible
            if type(humid) == float :
            
                if humid != 999:
                    # check for crazy values from DHT22
                    if humid >= 0 and humid <= 100:
                        lcd.write2pos("Temp     = {0:0.2f}".format(temp)+chr(0)+"C", 1,1)
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
                errdht11 = errdht11 + 1
                logger.write("Read Errors + " +str(errdht11))
                print("Unable to read sensor dht22 count=" +str(errdht11))
        
        except KeyboardInterrupt:
            print("\nUser abort with CTRL-C\n")
            logger.write("\nUser abort with CTRL-C\n")
            lcd.cleanup()
            exit()
