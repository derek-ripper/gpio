
import time

class timerx(object):

    def __init__(self):
        self.starttime = time.time()

    def elapsedtime(self):
        elasped = self.currenttime() - self.starttime  
        return elasped
        
    def currenttime(self):  
    	ct = time.time()
    	return ct 
    	  
    def waitforme(self,waittime):	
    	nowtime = self.currenttime()
    	while (self.currenttime() - nowtime) < waittime :
    		pass
	    	  