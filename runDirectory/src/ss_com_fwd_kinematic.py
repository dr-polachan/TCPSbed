#!/usr/bin/env python

import transfers1.rev1 as transfers
import algorithms.checksum.basic
import codec.generic
import algorithms.test.ping as ping
import time
   
def forward_flow_kinematic():     
    ### defining in/out address/mode
    address_rx = ss_com_fwd_flow_kinematic_entry_addr
    address_tx = ss_com_fwd_flow_kinematic_exit_addr    
    mode_rx = ss_com_fwd_flow_kinematic_entry_mode
    mode_tx = ss_com_fwd_flow_kinematic_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
        print "live_sscom_fwd",time.time()
        
        ### receive message
	msg = transfers.receive(obj_rx)
        ping.echo_back_rev2(msg,"tpf_ss_com_entry",address_rx)        

	### decode message
	msg_list = codec.generic.decode(msg) 
	
	### encode message
        msg = codec.generic.codev2(msg,msg_list)
        
	### send to tactile slave
	transfers.send(obj_tx,msg)
        ping.echo_back_rev2(msg,"tpf_ss_com_exit",address_rx)
    
    transfers.close(obj_tx)
    transfers.close(obj_rx)

    return
