######################################################################
# Title  : Class to read a config file for  cottage GPIO routine
# Created: 04 Apr 2018
# Author : Derek Ripper
#
######################################################################
from pathlib import Path

class ReadConfig(object):

    def __init__(self,file):
        self.filein     = file  # fully pathed config file name
        self.delim      = '='   # config file deliminter
        self.ConfigDict = {}    # empty dictionary for config values

        self.readfile()

    def readfile(self):
        # scheck that file exists
        my_file = Path(self.filein)
        if not my_file.is_file():
            print("\n***** ERROR config file : "+str(my_file)+" : NOT found.")
            raise SystemExit
            
        with open(self.filein) as fh:
            for line in fh:
                line = line.strip()
                if len(line) ==   0:        # skip over blank   lines
                    pass
                elif line[0] == '#':        # skip over comment lines
                    pass
                elif self.delim not in line:# skip lines without a "="
                    pass
                else:                       # store key/value pair in Dictionary
                    key, value           = line.strip().split(self.delim, 1)
                    self.ConfigDict[key.strip()] = value.strip()
    
    def keyindict(self,key):
        if key in self.ConfigDict:
            return True
        else:
            return False

    def GetConfigValue(self,key):
        if self.keyindict(key):
            return self.ConfigDict[key]
        else:
            print("\n***** ERROR config key : "+key+" : NOT found.")
            raise SystemExit

    def printconfig(self):
        for key,value in self.ConfigDict.items():
            print( ">"+ key+"< = >"+value+"<")
################################################################################
################################################################################

