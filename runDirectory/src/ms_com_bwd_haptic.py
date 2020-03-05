#!/usr/bin/env python

import codec.generic
import codec.cyber_glove
import algorithms
import transfers1.rev1 as transfers
import algorithms.checksum.basic
import algorithms.test.ping as ping

### forward flow engine
def backward_flow_haptic():     
    ### defining in/out address/mode
    address_rx = ms_com_bwd_flow_haptic_entry_addr
    address_tx = ms_com_bwd_flow_haptic_exit_addr    
    mode_rx = ms_com_bwd_flow_haptic_entry_mode
    mode_tx = ms_com_bwd_flow_haptic_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
    #for myvar in range (2):
        
        print "live_mscom_bwd",time.time()
        ### receive message
	msg = transfers.receive(obj_rx)
        
        ### decode the message
        msg_list = codec.generic.decode(msg)
                
        ### encode the message for cyber_glove haptic actuators
        #msg = codec.cyber_glove.code_vMtech(msg_list) 

	### add checksum
	msg_list = algorithms.checksum.basic.rev1(msg_list)
    
	### code message        
	msg = codec.generic.codev2(msg,msg_list)
        
        ### send message
	transfers.send(obj_tx,msg)
	        
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


