#!/usr/bin/env python

import transfers1.rev1 as transfers
import algorithms.test.ping as ping
from time import sleep
import codec.generic

def backward_flow_ping():     
    ### defining in/out address/mode
    address_rx = ss_com_bwd_flow_ping_entry_addr
    mode_rx = ss_com_bwd_flow_ping_entry_mode
    
    ### initialization
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):
        print "live_server_bwd_ping",time.time()

        ### receive message
        msg = transfers.receive(obj_rx)
        msg = ping.transfer(msg, address_rx) 
    
    transfers.close(obj_tx)


    return
