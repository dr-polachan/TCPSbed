#!/usr/bin/env python

import os, sys

lib_path = os.path.abspath(os.path.join(__file__,'..','..'))	
print lib_path
sys.path.append(lib_path)

import codec.generic
import codec.audiovideo

import transfers1.rev1 as transfers

import time
import cv2



execfile("./src/server_settings.py")

### embsys input devices
embsys_ss_webcam = 0 # 0 => first camera connected to system

### forward flow engine
def videocamera(): 
    ### defining in/out address/mode 
    address_rx = (embsys_ss_webcam, "NaN") 
    address_tx = (ss_com_ip, video_link_0)
    mode_rx = "webcam"
    mode_tx = "udp4pkts"
    
    ### initialization    
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
    #for myvar in range (2):        
        print "live_embsys_videocamera",time.time()
        
        ### receive message
        msg = transfers.receive(obj_rx)        
        
   	## encode the message
    	msg = codec.audiovideo.code(msg) 

        ## send the message
    	transfers.send(obj_tx,msg)
	          
    transfers.close(obj_tx)
    transfers.close(obj_rx)

    return

if __name__ == '__main__':
    videocamera()
