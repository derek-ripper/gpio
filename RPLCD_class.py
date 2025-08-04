# **********************************************************************
# * Filename      : RPLCD_class.py
# * Purpose       : Using std lib for LCD display with extra functions 
#                 : to extand the class
#
# * Created       : 31 Dec 2020 
# * Author        : Derek
# **********************************************************************
# updates:
# **********************************************************************
'''
Install module as:
        sudo pip3 install RPLCD
        
If not already installed we will also need:
        sudo apt-get install python-smbus
        
Usage in python:
 
    from  RPLCD_class import Mylcd

    lcd = Mylcd(i2c_expander='PCF8574', address=0x27)
        # params i2c_expander and address of display are mandatory.
        #
        # Other optional arguments with defaults are  as follows:
        
            cols=20, rows=4, dotsize=8,
            charmap='A02',
            auto_linebreaks=True,
            backlight_enabled=True,
            port = 1) # port = 0 on older Pi's
'''

from RPLCD.i2c import CharLCD



class Mylcd(CharLCD):

    def __init__(self,   *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # generate special characters
        self.genchars()
    
    # Use routine to write to screen at an initial start position
    # of Top left as 1,1 (row, col)         
    def write2pos(self,value, line=1, pos=1):
        # user coord system to start  at 1,1 Top lefthand corner
        # adjust screen origin to 0,0 at     Top lefthand corner
        line -= 1
        pos  -= 1 
        self.cursor_pos = (line, pos)
        self.write_string(value)
        
    # Call at end of program to turn off screen
    def cleanup(self):
        self.close(clear=True)
        self.backlight_enabled = False
        
    # turn display ON   
    def on(self):
        self.display_enabled = True
    
    # turn disply OFF
    def off(self):
        self.display_enabled = False
        
    # clear complete screen 
    def cls(self):
        self.clear()
        
    # create custom characters - allowed id's are 0 thru 7

    def genchars(self):
        #char=0 as Degree symbol
        degree = [
        0b00110,
        0b01001,
        0b01001,
        0b00110,
        0b00000,
        0b00000,
        0b00000,
        0b00000,
        ]
        #char=1 as a box
        box = [
        0b11111,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b11111,
        ]
        #char=2 as a block
        block = [
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        0b11111,
        ]
        #char=3 as a Left Pointing Arrow
        lh_arrow = [
        0b00000,
        0b00100,
        0b01000,
        0b11111,
        0b01000,
        0b00100,
        0b00000,
        0b00000,
        ]
        self.create_char(0, degree)
        self.create_char(1, box)    
        self.create_char(2, block)
        self.create_char(3, lh_arrow)
