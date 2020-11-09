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

if __name__ == '__main__':

    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN    = 4
    DHT        = humidity()

    
    logger = DU.c_logger("/home/pi/dev/gpio/humidity/", "logx.txt")
    
    while True:
        try:
            T.sleep(5)
            humid, temp = DHT.read_ht(DHT_SENSOR,DHT_PIN)
            print(humid)
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temp, humid))
            logger.write("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temp, humid))
        
        except KeyboardInterrupt:
            print("\nUser abort with CTRL-C\n")
            logger.write("\nUser abort with CTRL-C\n")
            exit()
