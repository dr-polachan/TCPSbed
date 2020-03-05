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

execfile("server_settings.py")

obj_file = open('data.txt', 'w')

### forward flow engine
def function_step_input():    
    ### defining in/out address/mode
    address_rx = (ms_embsys_app_ip, hap_link_3)
    address_tx = (ms_com_ip, kin_link_0)    
    mode_rx = "udp-non-blocking"
    mode_tx = "udp"
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)


    ### reset the robot to initial position before commencing test
    #msg = [15, 0 , 15, 0, 0]
    msg = [15, 6 , 10, 0, 0]
    
    msg = codec.generic.code(msg)
    transfers.send(obj_tx,msg)
    time.sleep(1)

    ### start doing test
		
    ### initial values
    x = 16
    y = -6
    z = 10 # here z is the control variable that maintains pressure
    pincher = 0
    
    y = 6		   	
    #while(y < 6):
    for i in range (1, 50):	


	#if(y > 2):
	if(i>0):
		pincher = 50 ## this is to start the slave end to save data


	#y = y+.1
		
	print "live_embsys_app_controller",time.time()
	
	#z=5 #at z=3, pressure=0.70, at z=5, pressure = 0.20

	### send kinematic data
	msg = [x, y, z, 0, pincher] #(x,y,z,pitch=0,pincher)

	## encode the message        
	msg = codec.generic.code(msg)
	
	## send the data	
	transfers.send(obj_tx,msg)
	print "send", msg

	### controller reaction time
	time.sleep(500e-3)

	### receive message from haptic link
        msg = transfers.receive(obj_rx)        
        print "received",msg

	### controller in action
	if(msg != "NaN"):

		print "okay"

        	flag = 1
		### decode the message
		msg_list = codec.generic.decode(msg)
		        
		### controller -algorithm (simple propotional controller)
		#pressure_old = pressure		
		pressure = float(msg_list[0])
		
		#if(pressure != pressure_old) and (flag==1):
		ref = 0.7 #100
		error = ref - pressure
		error = error*-1 # to account for sign change at remote end
		kp = 1*ref #0.1

		z = z + kp*error
	
	else:
		if(flag == 1):
			ref = 0.7
			error = ref - pressure
			error = error*-1 # to account for sign change at remote end
			kp = 1*ref

			z = z + kp*error

	### correction

	if(z < -5):
		z= -5
	if(z > 20):
		z=20

    ### terminate slave end code	
    msg = [x, y, z, 0, 100] # pincher=100 to terminate application at slave side
    msg = codec.generic.code(msg)
    for i in range(5):
    	transfers.send(obj_tx,msg)

    print "DONE !!!"

    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


if __name__ == '__main__':
    function_step_input()
