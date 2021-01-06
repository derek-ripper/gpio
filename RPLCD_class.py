# **********************************************************************
# * Filename      : RPLCD_class.py
# * Purpose       : Using std lib for LCD display with extra functions 
#                 : to extand the class
#
# * Created       : 31 Dec 2021 
# * Author        : Derek
# **********************************************************************
# updates:
# **********************************************************************
'''
usage: 
from  RPLCD_class import Mylcd

lcd = Mylcd(i2c_expander='PCF8574', address=0x27)
    # params i2c_expander and address of display are mandatory
    #
    # optional other  params that are by default as follows:
    
	# cols=20, rows=4, dotsize=8,
	# charmap='A02',
	# auto_linebreaks=True,
	# backlight_enabled=True,
	# port = 1) # port = 0 on older Pi's
'''
from RPLCD.i2c import CharLCD
import time


class Mylcd(CharLCD):
	def __init__(self,   i2c_expander='PCF8574', address=0x27):
		super().__init__(i2c_expander='PCF8574', address=0x27)
		
		# generate special characters
		self.genchars()
				
	def write2pos(self,value, line=1, pos=1):
		#adjust screen origin to 0,0 at Top lefthand corner
		line -= 1
		pos  -= 1 
		self.cursor_pos = (line, pos)
		self.write_string(value)
		
	def cleanup(self):
		self.close(clear=True)
		self.backlight_enabled = False
		
	def on(self):
		self.display_enabled = True
	
	def off(self):
		self.display_enabled = False
		
	def cls(self):
		self.clear()
		
	# create custom characters - allowed id's 0 thru 7

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
		self.create_char(0, degree)
		self.create_char(1, box)	
		self.create_char(2, block)
