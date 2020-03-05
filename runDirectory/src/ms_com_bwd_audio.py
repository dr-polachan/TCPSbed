#!/usr/bin/env python

import codec.generic
import transfers1.rev1 as transfers
import pickle
import cv2
import time
import codec.audiovideo
import codec.audio


def backward_flow_audio():  
    ### defining in/out address/mode
    address_rx = ms_com_bwd_flow_audio_entry_addr
    address_tx = ms_com_bwd_flow_audio_exit_addr    
    mode_rx = ms_com_bwd_flow_audio_entry_mode
    mode_tx = ms_com_bwd_flow_audio_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
    #for myvar in range (50):        
        print "live_mscom_bwd",time.time()
                
        ### receive message
        msg = transfers.receive(obj_rx)
	
	### decoding message
	msg = codec.audio.decode(msg)             
        
	### encoding message        
	msg = codec.audio.code(msg)

        ### sending  message        
        transfers.send(obj_tx,msg)
        
        
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


