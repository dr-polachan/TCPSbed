#!/usr/bin/env python


import os, sys
lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
sys.path.append(lib_path)

import codec.generic

import transfers1.rev1 as transfers

#import test.ping
import time

import random

from time import sleep

execfile("./src/server_settings.py")

### forward flow engine
def step_input(i): 
    obj_file = open('./results/StepAnalysis/data%s.txt' %i, 'w')   
    ### defining in/out address/mode
    address_rx = (ss_embsys_app_ip, kin_link_3)
    address_tx = (ss_com_ip, hap_link_0)    
    mode_rx = "udp"#-non-blocking"
    mode_tx = "udp"
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    pressure = 0
    x=0
    while (1):
        print "live_embsys_app_stepinput",time.time()

        ### receive message
        msg = transfers.receive(obj_rx)        
        print msg
        
	if(msg != "NaN"):
		### decode the message
		msg_list = codec.generic.decode(msg)
			
		### apply step input for pressure
		x = float(msg_list[0])
		y = float(msg_list[1])    

		if(x > 50):
			pressure = -1*y*10/1.25
		else:
			pressure = -1*y*10/1.0

        msg = [pressure, pressure]

	## encode the message        
	msg = codec.generic.code(msg)
        	
	print "haptic output",msg

        ## send message
        transfers.send(obj_tx,msg)

	## save to file
	if(x > 1):
		
		string = str('{0:6f}'.format(time.time()))+","+str(pressure)+"\n"
		obj_file.write(string) #time,pressure
  
	## breaking the application
	if(x > 77):
		print "limit exceeded, closing applciation"
		obj_file.close()
    		transfers.close(obj_tx)
    		transfers.close(obj_rx)
		break;
    

    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


if __name__ == '__main__':
	i = 0
	while(1):
		step_input(i)
		print "DEBUG: Iteration Count", i
		i = i+1
		time.sleep(2)



