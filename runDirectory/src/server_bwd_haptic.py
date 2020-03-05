#!/usr/bin/env python

import transfers1.rev1 as transfers
import codec.generic
import algorithms.test.ping as ping

### forward flow engine
def backward_flow_haptic():  
    ### defining in/out address/mode
    address_rx = server_bwd_flow_haptic_entry_addr
    address_tx = server_bwd_flow_haptic_exit_addr    
    mode_rx = server_bwd_flow_haptic_entry_mode
    mode_tx = server_bwd_flow_haptic_exit_mode
    
    ### initialization
    obj_tx = transfers.init_tx(address_tx,mode_tx)
    obj_rx = transfers.init_rx(address_rx,mode_rx)
    
    while (1):

        print "live_srv_bwd",time.time()

        ### receive message
        msg = transfers.receive(obj_rx)
        
        ### decode the messasge       
        msg_list = codec.generic.decode(msg) # msg_list = [force-sensor-1-data, force-sensor-2-data]
                
        ### encode the message
        msg = codec.generic.codev2(msg,msg_list)
        
        ### send the message
        transfers.send(obj_tx,msg)
        
    transfers.close(obj_tx)
    transfers.close(obj_rx)
    return


