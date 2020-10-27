
import time

class timer(object):

    def __init__(self):
        self.startingtime=self.currenttime()
        self.resetstarttime()
        self.cumruntime = 0.0
        
    def timefromprogramstart(self):
        rc = self.currenttime() - self.startingtime 
        return rc
        
    def elapsedtime(self):
        elasped = self.currenttime() - self.starttime  
        return elasped
        
    def currenttime(self):  
      ct = time.time()
      return ct 
        
    def resetstarttime(self): 
      self.starttime = time.time()
      
    def calccumruntime(self):
        runningtime = self.elapsedtime()  
        self.cumruntime = self.cumruntime  + runningtime
        self.resetstarttime()

    def getcumruntime(self):
        return self.cumruntime

    def secs2dhms(self,seconds):
        time = seconds
        day  = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        rc = "d:h:m:s-> %d:%d:%d:%d" % (day, hour, minutes, seconds)
     
        return rc    
