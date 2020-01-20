#!/usr/bin/env python3

import time

import mytimer as tt

o_T = tt.timerx()

while True:
 
	o_T.waitforme(5)
	print("now;"+str(o_T.currenttime()))