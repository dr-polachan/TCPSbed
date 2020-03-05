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




execfile("server_settings.py")

### forward flow engine
def deskcamera(): 
    ### defining in/out address/mode 
    address_rx = ("NaN", "NaN") 
    address_tx = (ss_com_ip, video_link_0)
    mode_rx = "deskcam"
    mode_tx = "udp4pkts"
    
    ### initialization    
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
    #for myvar in range (2):        
        print "live_embsys_desktopcamera",time.time()
        
        ### receive message
        msg = transfers.receive(obj_rx)        
        
   	## encode the message
    	msg = codec.audiovideo.code(msg) 
	print "length", len(msg)
        
        ## send the message
    	transfers.send(obj_tx,msg)
	          
    transfers.close(obj_tx)
    transfers.close(obj_rx)

    return

if __name__ == '__main__':
    deskcamera()
