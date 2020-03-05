#!/usr/bin/env python

import transfers1.rev1 as transfers

import codec.generic
import codec.audiovideo



### forward flow engine
#def test():
#    while(1):
#        print "ping"

def backward_flow_video(): 
    print "hedfdad" 
    ### defining in/out address/mode
    address_rx = server_bwd_flow_video_entry_addr
    address_tx = server_bwd_flow_video_exit_addr    
    mode_rx = server_bwd_flow_video_entry_mode
    mode_tx = server_bwd_flow_video_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
    #for myvar in range (2):
        print "live_srv_bwd_video",time.time()
        
        ### receive
        msg = transfers.receive(obj_rx)
	
        ### decode
        #msg = codec.audiovideo.decode(msg)             
        
        ### encode
        #msg = codec.audiovideo.code(msg)

        ### send
        transfers.send(obj_tx,msg)
        
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


