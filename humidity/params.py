#
#
##
import config as CFG

class Parameters(oject, configfilename):
    def __init__(self):
        o_Config = CFG.readconfig(configfilename)
        PollTime      = int(o_cfg.GetConfigValue('POLLTIME'))
        
        set_param(
        
    def get_param(self):
        print("getting param")
        return self._param
        
        
    def set_param(self,value):
        print("setting param")
        return self._param = value
        
        
    param = property(get_param, set_param)  
    
