### Importing Modules
from __future__ import division
import math
import time


def rev1(msg_list):

    try:        
	if(msg_list[0] == "NaN"):
		msg_list = [4095, 4095]
	if(msg_list[1] == "NaN"):
		msg_list = [4095, 4095]			
	msg_list[0] = msg_list[0].replace('\0', '')
	msg_list[1] = msg_list[1].replace('\0', '')
	vibrator1 = int(msg_list[1])
	vibrator2 = int(msg_list[1])
    except:
	vibrator1 = 4095
	vibrator2 = 4095

    try:
    	if(vibrator1 > 4095):
		vibrator1 = 4095
    	if(vibrator1 < 0):
		vibrator1 = 0
    	if(vibrator2 > 4095):
 		vibrator1 = 4095
    	if(vibrator2 < 0):
		vibrator1 = 0	
    	vibrator1 = 4095 - vibrator1;
    	vibrator2 = 4095 - vibrator2;        
    	vibrator1 = int(vibrator1*0.048) #make the return value less than 200
    	vibrator2 = int(vibrator2*0.048)
    	msg_list = [vibrator1, vibrator2]
    except:
	msg_lsit = [0, 0]
     
    return(msg_list)

