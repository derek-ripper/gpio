#!/usr/bin/env python3

import os
import sys
from time import sleep


# needed to access my other Pyton std. modules
sys.path.append(os.path.abspath("/home/pi/dev/gpio"))
import DU
from  RPLCD_class import Mylcd


if __name__ == '__main__':

    print("LCD CTRL .....")
    lcd = Mylcd(i2c_expander='PCF8574',address=0x27)
  
    lcd.clear()
    lcd.write2pos("Bingo-line 1!",pos=1,line=1)
    sleep(2)
    lcd.write2pos("Bingo-line 2!",pos=2,line=2)
    sleep(2)
    lcd.write2pos("Bingo-line 3!",pos=3,line=3)
    sleep(2)
    lcd.write2pos("Bingo-line 4!",pos=4,line=4)
    sleep(2)
    lcd.cleanup()

