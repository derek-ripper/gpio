#!/usr/bin/env python3
'''
**********************************************************************
* Filename      : FileClass
* Description   : Class defs for file related functions
* Created       : 11 Jan 2020
* Author        : Derek
**********************************************************************
'''

import os, time

class FileMod(object):
    
    def __init__(self, file):
        ## Store modification date of "file"
        self.FileName = file
        #ModDate syntax DoW,Month,Day,time,year 
        self.ModDate  = os.stat(self.FileName)[8]
        
    def Changed(self):
        ## Test if "file" has been modified since object instantiated?
        NewModDate  = os.stat(self.FileName)[8]
        if NewModDate != self.ModDate:
            # file has been updated
            self.ModDate = NewModDate
            rc = True
        else:
            # file has not been updated
            rc = False
        
        return rc
        
        
#if __name__ == '__main__':
    #from time import sleep
    #FC = FileChecks("relay1.py")

    #while True:
        #try:
            #print("File modified? = "+str(FC.Changed()))
            #sleep(5)
        #except KeyboardInterrupt:
            #print("All Done")
