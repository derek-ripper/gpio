'''
**********************************************************************
* Filename      : sensors.py
* Description   : 1- to control a single relay 
*                 2- Read the DHT22 temp/humidity sensor
 *                3- 
* Author        : Derek
* Created       : 24 Dec 2019
**********************************************************************
updates:
20 Jan 2020 - DHTsensor now powered from a GPIO pin. Hence new routine to 
              reaset it. Previously done using spare relay in the 
              2 channel module on a direct power line.
'''
import RPi.GPIO as GPIO   #generic gpio RaspPi support

import Adafruit_DHT       #support of DHT sensor

import time
###########################################################################
class Relay(object):
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
class Humidity(object):
    def __init__(self, sensortype, sensorpin, pwrpin):
        self.DHT_SENSOR  = sensortype
        self.DHT_PIN     = sensorpin
        self.DHT_PWR_PIN = pwrpin
        GPIO.setup(self.DHT_PWR_PIN , GPIO.OUT, initial=GPIO.HIGH)
        
    def read_dht(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        #####
        if humidity != None:
            humidity = round(humidity,2)
        else:
            humidity = 999
            
        #####  
        if temperature != None:
            temperature = round(temperature,2)
        else:
            temperature = 999            
            
        return humidity, temperature
        
    def reset(self, offtime=2):
        GPIO.output(self.DHT_PWR_PIN, GPIO.LOW)
        time.sleep(offtime)
        GPIO.output(self.DHT_PWR_PIN, GPIO.HIGH)
        
