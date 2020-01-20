
import time

class timer(object):

    def __init__(self):
        self.resetstarttime()
        self.cumruntime = 0.0

    def elapsedtime(self):
        elasped = self.currenttime() - self.starttime  
        return elasped
        
    def currenttime(self):  
    	ct = time.time()
    	return ct 
    	  
    def resetstarttime(self):	
    	self.starttime = time.time()
    	
    def calctotruntime(self):
        runningtime = self.elapsedtime()  
        self.cumruntime = self.cumruntime  + runningtime
        self.resetstarttime()

    def gettotruntime(self):
        return self.cumruntime

	    	  