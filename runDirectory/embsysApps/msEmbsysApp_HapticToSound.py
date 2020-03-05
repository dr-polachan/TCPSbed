#!/usr/bin/env python

#### Not working !!!

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
def function_hapticToSound():    

    ### defining in/out address/mode
    address_rx = (ms_embsys_app_ip, hap_link_3)
    mode_rx = "udp"
    
    ### initialization
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while(1):
	    ### receive message from haptic link
	    msg = transfers.receive(obj_rx)        
	    print "received",msg


	    ### decode the message
	    msg_list = codec.generic.decode(msg)
	    pressure = float(msg_list[0])

	    ### pressure to sound
	    pressure = pressure / 100.0
	    pressure = 1
	    pressure = int(pressure)
	    pressure = str(pressure)
	    stringCommand = "play -n synth 0.1 sine 1e3 vol "+pressure+" repeat 1"
	    os.system(stringCommand)

    transfers.close(obj_rx)
    return


if __name__ == '__main__':
    function_hapticToSound()
