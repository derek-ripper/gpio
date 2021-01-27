#!/usr/bin/env python3
''' 
**********************************************************************
* Filename      : cryptit.py
* Purpose       : ACCESS CONTROL -- hide passwords
* Created       : 27 Nov 2020 onwards!!
* Author        : Derek
**********************************************************************
* 
'''
from  crypt_lib import Acctl

#######################################################################
#######################################################################
if __name__ == "__main__":
    crypt = Acctl("old","/home/pi/dev/gpio/ac/","Test#1")
    ans   = crypt.test()
    print("From File: "+crypt.txtfilename+"\nUnencrypted text is: "+str(ans))
