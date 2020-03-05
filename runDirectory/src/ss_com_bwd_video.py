#!/usr/bin/env python

import transfers1.rev1 as transfers


import pickle
import numpy as np
import cv2

import codec.audiovideo

def backward_flow_video():    
    ### defining in/out address/mode
    address_rx = ss_com_bwd_flow_video_entry_addr
    address_tx = ss_com_bwd_flow_video_exit_addr    
    mode_rx = ss_com_bwd_flow_video_entry_mode
    mode_tx = ss_com_bwd_flow_video_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)

    while (1):
    #for myvar in range (2):
        print "live_sscom_bwd_video",time.time()
	
	## receiving data from embsys_app_videocamera
	msg = transfers.receive(obj_rx)                   	
                
	## send the message
    	transfers.send(obj_tx,msg)
	          
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


