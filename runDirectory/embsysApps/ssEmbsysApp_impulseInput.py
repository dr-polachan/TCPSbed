#!/usr/bin/env python


import os, sys
lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
sys.path.append(lib_path)

import codec.generic

import transfers1.rev1 as transfers

#import test.ping
import time

from time import sleep

execfile("server_settings.py")

obj_file = open('data.txt', 'w')

### forward flow engine
def function_step_input():    
    ### defining in/out address/mode
    address_rx = (ss_embsys_app_ip, kin_link_3)
    address_tx = (ss_com_ip, hap_link_0)    
    mode_rx = "udp"
    mode_tx = "udp"
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    flag = 0
    while (1):
    #for myvar in range (2):
        print "live_embsys_app_stepinput",time.time()
	k = time.time()
        ### receive message
        msg = transfers.receive(obj_rx)        
        print msg
        
        ### decode the message
        msg_list = codec.generic.decode(msg)
                
        ### apply step input for pressure
	x = float(msg_list[0])
	y = float(msg_list[1])    

	if(x > 25):
		pressure = 225
	else:
		pressure = 0
	
	#if(pressure < 0):
	#	pressure=0

        msg = [pressure, pressure]

	## encode the message        
	msg = codec.generic.code(msg)

	### sleep
	#sleep(.02)
        	
	print "haptic output",msg

        ### send message
        transfers.send(obj_tx,msg)

	### save to file
	if(x > 10):
		flag = 1
		string = str('{0:6f}'.format(time.time()))+","+str(pressure)+"\n"
		obj_file.write(string) #time,pressure
		#print "diff",time.time()-k
  
	## breaking the application
	if((x < 0) and (flag==1)):
		print "limit exceeded, closing applciation"
		break;
    
    obj_file.close()
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


if __name__ == '__main__':
    function_step_input()
