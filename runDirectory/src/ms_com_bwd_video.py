#!/usr/bin/env python

import codec.generic
import transfers1.rev1 as transfers
import algorithms.test.ping
import pickle
import cv2
import time
import codec.audiovideo

def backward_flow_video():

    ### defining in/out address/mode
    address_rx = ms_com_bwd_flow_video_entry_addr
    address_tx = ms_com_bwd_flow_video_exit_addr    
    mode_rx = ms_com_bwd_flow_video_entry_mode
    mode_tx = ms_com_bwd_flow_video_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):

        print "live_mscom_bwd_video",time.time()
                
        ### receive message
        msg = transfers.receive(obj_rx)
	
        ### sending  message        
        transfers.send(obj_tx,msg)
        
        
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


