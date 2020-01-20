    import config   as CFG    
    
    class param():
        def __init__(self):
            o_cfg     = CFG.ReadConfig('config.txt')
            self.define()
            self.writelog()
            
        def define(self):
            ### CONSTANTS 
            self.PollTime      = int(o_cfg.GetConfigValue('POLLTIME'))
            self.RestTime      = int(o_cfg.GetConfigValue('RESTTIME'))
            self.MaxConRunTime = int(o_cfg.GetConfigValue('MAXCONRUNTIME'))
        
            self.OffThres = float(o_cfg.GetConfigValue('OFFTHRES')) # % RH - Threshold to turn OFF power
            self.OnThres  = float(o_cfg.GetConfigValue('ONTHRES'))  # % RH - Threshold to turn ON  power
        
                

        def writelog(self)
            ### write basic data to log file
            logger.write("OFF threshold: "+str(self.OffThres)+" %RH")
            logger.write("ON  threshold: "+str(self.OnThres) +" %RH")
            logger.write("Poll interval: "+str(self.PollTime)+" secs")
            logger.write("Max run tme  : "+str(self.MaxConRunTime)+" secs")
            logger.write("Rest Time    : "+str(self.RestTime)+" secs")
            
        def reload(self):
            self.define()
            self.writelog()
