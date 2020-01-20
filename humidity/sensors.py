'''
**********************************************************************
* Filename 		: relayclass.py
* Description     	: to control a single relay 
* Author 		: Derek
* Created               : 24 Dec 2019
**********************************************************************
'''
import RPi.GPIO as GPIO   #generic gpio RaspPi support

import Adafruit_DHT       #support of DHT sensor

###########################################################################
class relay(object):
    def __init__(self, PinNum):

        self.gpiopin = PinNum
        GPIO.setup(self.gpiopin, GPIO.OUT, initial=GPIO.HIGH)
	
    def switchON(self):	
        # relay in normal "NO" normally OPEN mode
    	GPIO.output(self.gpiopin, GPIO.LOW)
    
    def switchOFF(self):	  
        # relay in normal "NC" Normally Conected mode
    	GPIO.output(self.gpiopin, GPIO.HIGH)
    	
###########################################################################
class humidity(object):
    def __init__(self, sensortype, sensorpin):
        self.DHT_SENSOR = sensortype
        self.DHT_PIN    = sensorpin
        
    def read_dht(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        ##########################################
        if humidity != None:
            humidity = round(humidity,2)
        else:
            humidity = 999
            
        ##########################################    
        if temperature != None:
            temperature = round(temperature,2)
        else:
            temperature = 999            
            
        return humidity, temperature
        
   