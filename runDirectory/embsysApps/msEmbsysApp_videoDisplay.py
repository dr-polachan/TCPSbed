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

### forward flow engine
def display(): 
    ### defining in/out address/mode
    address_rx = (ms_embsys_app_ip, video_link_3)
    mode_rx = "udp4pkts"
    
    ### initialization    
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
        print "live_embsys_display",time.time()
        
        ### receive message
        msg = transfers.receive(obj_rx)        
        
        ### decode
        msg = codec.audiovideo.decode(msg)
        
	try:
        ### display on screen using opencv, press keyboard key q to quit
		cv2.imshow('slave-side: video',msg)
	except:
		# do nothing
		print "issue"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    transfers.close(obj_rx)
    return

if __name__ == '__main__':
    display()
