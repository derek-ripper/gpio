#!/usr/bin/env python3
import Adafruit_DHT




class humidity(object):

    def read_ht(self,DHT_SENSOR,DHT_PIN):
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        return humidity, temperature













if __name__ == '__main__':

    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN    = 4
    DHT        = humidity()
    
    while True:
    	try:
	     humid, temp = DHT.read_ht(DHT_SENSOR,DHT_PIN)
	     print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temp, humid))

    	except KeyboardInterrupt:
      	    print("\nUser abort with CTRL-C\n")
      	    exit()
        
        
        
# while True:
    # humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    # if humidity is not None and temperature is not None:
        # print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    # else:
        # print("Failed to retrieve data from humidity sensor")
