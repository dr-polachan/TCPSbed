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
def funController(waitTime):    
    ### defining in/out address/mode
    address_rx = (ms_embsys_app_ip, hap_link_3)
    address_tx = (ms_com_ip, kin_link_0)    
    mode_rx = "udp-non-blocking"
    mode_tx = "udp"
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    y=-10
    x=0 
    pressure=0
    flag=0
    while (x < 80):
    #for myvar in range (2):
        print "live_embsys_app_controller",time.time()
	

	### send kinematic data
	msg = [x, y, 0, 0, 0] #(x,y,z,pitch=0,pincher)

	## encode the message        
	msg = codec.generic.code(msg)

	##droping packets
	#if(random.random()<= 1):
		### send message to kinematic link
	transfers.send(obj_tx,msg)
	print "send", msg

	time.sleep(waitTime)
  
  	print "waitTime (in seconds)", waitTime

        ### receive message from haptic link
        msg = transfers.receive(obj_rx)        
        print "received",msg
	if(msg != "NaN"):
        	flag = 1
		### decode the message
		msg_list = codec.generic.decode(msg)
		        
		### controller -algorithm (simple propotional controller)
		#pressure_old = pressure		
		pressure = float(msg_list[0])
		
		#if(pressure != pressure_old) and (flag==1):
		error = 100 - pressure
		error = error*-1 # to account for sign change at remote end
		kp = 0.1

		y = y + kp*error


		

	else:
		if(flag == 1):

			error = 100 - pressure
			error = error*-1 # to account for sign change at remote end
			kp = 0.1

			y = y + kp*error


	### correction

	if(y < -50):
		y=-50
	if(y > 50):
		y=50

			## increment position
	x=x+1
	
    	#time.sleep(10e-3)

    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


if __name__ == '__main__':
    nList = [2.7e-3, 2.8e-3] #, 2.6e-3] #, 2.1e-3, 2.2e-3, 2.3e-3]   
    #nList = [1.8e-3, 1.9e-3, 2e-3, 2.1e-3, 2.2e-3, 2.3e-3] #, 2.4e-3, 2.6e-3, 2.8e-3, 3e-3, 3.2e-3, 3.4e-3, 3.6e-3]	    
    #nList = [.5e-3, 1e-3, 1.5e-3, 2e-3, 2.5e-3, 3e-3, 3.5e-3, 4e-3, 4.5e-3, 5e-3]
    #nList = [1.5e-3]
    #nList = [.25e-3, .5e-3, 1e-3, 1.5e-3, 2e-3, 2.5e-3, 3.5e-3] #10e-3] #, 11e-3]
    m = 1000 # number of times each experiment has to be run
    for n in list (nList):
	for i in range(m):
		print "iteration",i,"nvalue",n
		funController(n)
		time.sleep(800e-3)
    print" DONE !!!"
