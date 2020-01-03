
import time

class timer(object):

    def __init__(self):
        self.resetstarttime()

    def elapsedtime(self):
        elasped = self.currenttime() - self.starttime  
        return elasped
        
    def currenttime(self):  
    	ct = time.time()
    	return ct 
    	  
    def resetstarttime(self):	
    	self.starttime = time.time()

	    	  